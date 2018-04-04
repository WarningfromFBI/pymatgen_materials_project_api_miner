import pymatgen as mg
import numpy as np
from sympy import *
import settings
import json
import feature_miner_functions.FeatureMinerHelper.CalculationHelpers as ch
import feature_miner_functions.FeatureMinerHelper.ShannonHelpers as sh
import copy
import pymatgen.analysis.bond_valence as pabv;
import pymatgen.symmetry.analyzer as psa
import os

structureDir = os.path.join(settings.ROOT_DIR, 'structure_database')
ShannonBase = os.path.join(settings.ROOT_DIR, 'Shannon_Radii')
ShannonData = json.load(open(ShannonBase+'\\ShannonRadiiDictionary.json', 'r'));

def Forces(sitesDat):#input is the sites datastructure from the structures_asdict from structures_query
    Fmax = 0; Ftot =0;
    for i in range(len(sitesDat)):
        elem = sitesDat[i];
        atom = mg.Element(elem['label']);
        forces = elem['properties']['forces']
        F = 0; #we need to calculate magnitude
        for j in range(3):
            F += forces[j] ** 2
        F = F ** .5;
        if (F > Fmax):
            Fmax = F;
        Ftot+=F;
    return [F/len(sitesDat), Fmax];

def coordinationNumber(sitesDat): #this data point is a little bit too discrete
    totcoordinNum = 0; coordinNumList = list();
    for i in range(len(sitesDat)):
        elem = sitesDat[i];
        coordinNum = elem['properties']['coordination_no'];
        coordinNumList.append(coordinNum)
        totcoordinNum += coordinNum;
    avgcoordinNum = totcoordinNum/len(sitesDat);
    return [np.mean(coordinNum), np.std(coordinNum)];
1
def numberDensity(structure): #number density of the entire lattice of the unlithiated compound
    volume = structure['lattice']['volume'];
    return len(structure['sites'])/volume;

def avgDistancefromCoM(picklestruct):
    #lattice is the datastructure from
    RCM = CenterofMass(picklestruct)
    totalR = list();
    for i in range(len(picklestruct.sites)):
        latticesite = picklestruct.sites[i];
        # extract element and calculate mass
        #atom = mg.Element(latticesite.specie.value);
        R = latticesite.frac_coords; #this has to be in fractional coordinates
        dr = 0;
        for j in range(3):
            dx = R[j] - RCM[j];
            dr += dx **2;
        dr = dr**0.5;
        totalR.append(dr);
    return [np.mean(totalR), np.std(totalR)];

def unlithanisotropy(picklestruct): #I feel like we need to do this with a reduced cell, vs just the lattice
    cuberootvol = (picklestruct.volume)**(1/3)
    latticeParams = picklestruct.lattice.abc;
    latticeParamsNorm = latticeParams/(np.max(latticeParams)); #scale theunit cell lengths against the largest length
    diffs = list(); diffs2 = list()
    for i in range(3):
        for j in range(i+1,3): #there are only 3 distinct differences we need to compare
            diff = (latticeParamsNorm[i]-latticeParamsNorm[j]); #normalize against V^1/3
            diff2 = (latticeParams[i] - latticeParams[j])/cuberootvol
            diffs.append(diff); diffs2.append(diff2);
    diffs = np.array(diffs);
    return [np.mean(diffs), np.std(diffs), np.mean(diffs2), np.std(diffs2)];

def IonRadVsLattice(picklestruct, ion): #attempts to account for how rectangular the cell is by taking the smallest
    #unit cell length, and seeing how much larger or smaller than it is compared to the lithium atom volume
    initialvol = picklestruct.volume
    unitcelllengths = picklestruct.lattice.abc #we sould not scal ehere as we are comparing lattice to lithium ion radius, which is fixed
    minlength = np.min(unitcelllengths);
    Lirad = mg.Element(ion).average_ionic_radius
    diff = minlength/Lirad;
    return diff/initialvol**(1/3);

#get the nearest neighbors to every element in the lattice, calculate average distances

#Li always has a +1 oxidation state in an atom, which means upon lithiation, materials should reduce
#their oxidation state... get a sense of how willing the constituents are to decrease their oxidation state
def oxidationStateFlexibility(picklestruct):
    #if we normalize against the cell volume, it gives a sense of what the oxidation difference can do per unit volume
    #at the same time, the unnormalized version of this data is already a top feature
    initialvol = picklestruct.volume
    diffs = list();
    for site in picklestruct.sites:
        minox = site.specie.min_oxidation_state
        maxox = site.specie.max_oxidation_state;
        diff = maxox-minox; diffs.append(diff);
    return [np.mean(diffs)/(len(picklestruct.sites)), np.std(diffs)/(len(picklestruct.sites)),
            np.max(diffs)/(len(picklestruct.sites)), np.min(diffs)/(len(picklestruct.sites))];

def oxidationStateVolumeFlexibility(pickleStruct):
    #how much does atomic volume change when charge state changes
    #we can use physical volumes as we normalize to teh volume of the unit cell
    volume = pickleStruct.volume;
    VolChange = 0;
    for site in pickleStruct.sites:
        elem = site.specie.value;
        ShannonPoint = ShannonData[elem]
        maxrad = 0; minrad = float('inf');
        for i in ShannonPoint:
            rad = i['ionic_radius'];
            if(rad > maxrad):
                maxrad = rad;
            if(rad<minrad):
                minrad = rad;
        volDiff = ch.sphereVol(maxrad)-ch.sphereVol(minrad);
    VolChange += volDiff;
    return VolChange/volume; #does this need a normalization to the unit cell?

def VolumeByAvgIonicRadius(pickleStruct):
    volume = pickleStruct.volume;
    Vtot = 0;
    for site in pickleStruct.sites:
        elem = site.specie;
        avgionicrad = elem.average_ionic_radius
        Vtot += ch.sphereVol(avgionicrad);
    return (volume - Vtot)/volume;

#SHANNON RADII MINING...all features should be normalized so they can be comparable between compounds
def VolumeByShannonRadii(pickleStruct):
    volume = pickleStruct.volume;
    Vtot = 0;
    for site in pickleStruct.sites:
        elem = site.specie.value;
        coordin_no = site.coordination_no;
        ShannonPoint = ShannonData[elem];
        v = 0; rad = 0;
        for i in ShannonPoint: #only positive shannon point data in our data set.
            if(i['coordination_no'] == coordin_no):
                rad= i['ionic_radius'];
                break; #we've found the correct ionic radius, so stop searching Shannon points
        if(rad == 0): #if rad is still zero, that means we didn't find the shannon point, so just use the avg ionic radius
            #as a suitable proxy for the average ionic radius
            rad = site.specie.average_ionic_radius;
        v = ch.sphereVol(rad);
        Vtot += v;
    return (volume - Vtot)/volume;

def VolumeFlexibilityByShannonRadii(pickleStruct): #change in volume when anion charge state is modified
    startVol = VolumeByShannonRadii(pickleStruct);
    TotDeltaVol = 0;
    for site in pickleStruct.sites:
        elem = site.specie.value;
        coordin_no = site.coordination_no;
        ShannonPoint = ShannonData[elem];
        deltaVol = 0;
        if(sh.isAnion(ShannonPoint) == True):
            originalRad = sh.getIonicRadiusWithCoordination(ShannonPoint, coordin_no);
            originalOx = sh.getOxNumbGivenCoordination(ShannonPoint, coordin_no);
            newRad = sh.getIonicRadGivenOx(ShannonPoint, originalOx - 1);
            if(newRad == None):
                newRad = originalRad
            deltaVol = ch.sphereVol(originalRad) - ch.sphereVol(newRad);
        TotDeltaVol+=deltaVol
    return TotDeltaVol/startVol;

def ShannonRatio(picklestruct):
    rads = list();
    for site in picklestruct.sites:
        elem = site.specie.value;
        coordin_no = site.coordination_no;
        ShannonPoint = ShannonData[elem];
        rad = 0; charge = np.mean(site.specie.common_oxidation_states)
        for i in ShannonPoint:
            if(i['coordination_no'] == coordin_no):
                rad= i['Z/IR'];
                rads.append(rad);
                break; #we've found the correct ionic radius, so stop searching Shannon points
        if(rad == 0): #if rad is still zero, that means we didn't find the shannon point, so just use the avg ionic radius
            #as a suitable proxy for the average ionic radius
            rads.append(charge/site.specie.average_ionic_radius);
    return np.mean(rads)

def ElectronegativitySolid(picklestruct): #taken from Davies and Butler using a geometric mean
    chi_total = 1; root = 0;
    for site in picklestruct.sites:
        elemElectroneg = site.specie.X;
        chi_total = chi_total*elemElectroneg;
        root+=1;
    return elemElectroneg**(1/root)

def deltaShannonRadii(pickleStruct):
    initialVol = pickleStruct.volume;
    deltaVolList = list();
    for site in pickleStruct.sites:
        elem = site.specie.value;
        coordin_no = site.coordination_no;
        ShannonPoint = ShannonData[elem];
        maxSeen = 0; minSeen = float('Inf');
        for dictionary in ShannonPoint:
            rad = dictionary['ionic_radius'];
            if(rad > maxSeen): maxSeen = rad;
            if(rad < minSeen): minSeen = rad;
        deltaVol = ch.sphereVol(maxSeen) - ch.sphereVol(minSeen);
        deltaVolList.append(deltaVol);
    return [np.mean(deltaVolList), np.std(deltaVolList), np.min(deltaVolList), np.max(deltaVolList)]/(initialVol)**(1/3);

def deltaShannonCrystalRadii(pickleStruct):
    initialVol = pickleStruct.volume;
    deltaVolList = list();
    for site in pickleStruct.sites:
        elem = site.specie.value;
        coordin_no = site.coordination_no;
        ShannonPoint = ShannonData[elem];
        maxSeen = 0; minSeen = float('Inf');
        for dictionary in ShannonPoint:
            rad = dictionary['crystal_radius'];
            if(rad > maxSeen): maxSeen = rad;
            if(rad < minSeen): minSeen = rad;
        deltaVol = ch.sphereVol(maxSeen) - ch.sphereVol(minSeen);
        deltaVolList.append(deltaVol);
    return [np.mean(deltaVolList), np.std(deltaVolList), np.min(deltaVolList), np.max(deltaVolList)]/(initialVol)**(1/3);

#if the unit cell atoms consist of mostly positive oxidation state elements, then why would it let lithium come in?
def CellOxidationStateDensity(pickleStruct): #normalize against the total number of elements...
    numElements = len(pickleStruct.sites); initialVol = pickleStruct.volume;
    positiveOxPop = 0; negativeOxPop = 0;
    for site in pickleStruct.sites:
        elem = site.specie.value;
        ShannonPoint = ShannonData[elem]; #Shannon Radii contains ONLY POSITIVE OXidation STATE MATERIALS!!!
        check = True; counter = 0;
        for i in ShannonPoint:
            if(i['oxidation_num'] < 0): #so this is a little superfluous
                check = False;
                break;
            else: counter+=1;
        if(check == True):
            positiveOxPop+=1;
        elif(counter == len(ShannonPoint)-1):
            continue; #no valence
        else:
            negativeOxPop+=1;
    return [positiveOxPop/numElements, positiveOxPop/initialVol, negativeOxPop/initialVol];

def SpaceGroup(picklestruct): #numbers ranging from 1 to 230, would be nice to find a way to weight these
    return picklestruct.get_space_group_info()[1];

def detLatticeVectors(picklestruct): #not a physically meaningful feature, convert to some other property of the lattice vector
    latticeVec = picklestruct.lattice.matrix;
    determinant = np.linalg.det(latticeVec);
    return determinant;

def CenterofMass(picklestruct):
    symmetryfinder = psa.SpacegroupAnalyzer(picklestruct)
    numerator = np.array([0.0, 0.0, 0.0])
    denominator = list();
    for sites in picklestruct.sites:
        elem = sites.specie.name;
        mass = sites.specie.data['Atomic mass']
        cellPosition = sites.frac_coords; #normalized
        numerator += cellPosition*mass
        denominator.append(mass);
    return numerator/(np.mean(denominator));

def AtomicNumberDensity(picklestruct): #gives a rough idea of the 'electron density'
    #this may be weird as a lot of electrons in heavy elements are tightly bound to the nucleus
    total = 0; initialVol = picklestruct.volume;
    for sites in picklestruct.sites:
        elem = sites.specie
        atmNum = sites.specie.data['Atomic no']
        total+=atmNum;
    return [total/initialVol];

#apply strains and see how much the volume changes
def volumeChangeUponStrain(picklestruct): #this is sort of a redundant feature, try to make it better
    initialVol = picklestruct.volume;
    picklestruct.apply_strain(0.01);
    finalVol = picklestruct.volume;
    return (finalVol-initialVol)/initialVol; #this isn't that great...all it can really differentiate is what kind of crystal structure the thing has

def angleAnisotropy(picklestruct):
    latticeAng = picklestruct.lattice.angles
    return np.std(latticeAng)

def changeinForceUponStrain(picklestruct):
    picklestruct.apply_strain(0.01);
    for site in picklestruct:
        r = site.coords;
    return None

def ChargeMomentOfInertia(picklestruct):
    SPA = psa.SpacegroupAnalyzer(picklestruct);
    picklestruct = SPA.get_conventional_standard_structure();
    Rcm = CenterofMass(picklestruct); #fractional coords
    I = 0;
    for site in picklestruct.sites:
        elemCharge = site.specie.max_oxidation_state;
        coords = site._fcoords;
        dist = coords-Rcm;
        I += elemCharge*np.dot(dist,dist);
    return I;

def MassMomentOfInertia(picklestruct):
    SPA = psa.SpacegroupAnalyzer(picklestruct);
    picklestruct = SPA.get_conventional_standard_structure();
    Rcm = CenterofMass(picklestruct); #fractional coords
    I = 0;
    for site in picklestruct.sites:
        Mass = site.specie.data['Atomic mass'];
        coords = site._fcoords;
        dist = coords-Rcm;
        I += Mass*np.dot(dist,dist);
    return I;

def AvgNumberNN(picklestruct): #can use voronoi connectivity as well
    NNCount = list()
    for site in picklestruct:
        neighbors = picklestruct.get_neighbors(site, 4);
        NNCount.append(len(neighbors));
    return [np.mean(NNCount), np.std(NNCount)]


##=================FUNCTION TO APPLY ALL THESE FUNCTIONS AT ONCE ==============================#


def GetAllStructureFeatures(structure, picklestruct):
    sitesDat = structure['sites']

    [a1, a7] = Forces(sitesDat)
    [a2, b2] = avgDistancefromCoM(picklestruct)
    [a3, b3] = coordinationNumber(sitesDat); #not all data points contain coordination numbers
    a4 = numberDensity(structure)
    [a5, b5, c5, d5] = unlithanisotropy(picklestruct)
    a6 = IonRadVsLattice(picklestruct, 'Li'); #change this if we test against other tyes of intercalation compounds
    [a8, b8, c8, d8] = oxidationStateFlexibility(picklestruct);
    a9 = VolumeByShannonRadii(picklestruct);
    [a11, b11, c11] = CellOxidationStateDensity(picklestruct)
    a12 = VolumeByAvgIonicRadius(picklestruct)
    a13 = SpaceGroup(picklestruct);
    a14 = volumeChangeUponStrain(picklestruct)
    [a15, a16, a17] = CenterofMass(picklestruct)
    a18 = oxidationStateVolumeFlexibility(picklestruct)
    [b19] = AtomicNumberDensity(picklestruct)
    [a20, b20, c20, d20] = deltaShannonRadii(picklestruct)
    a21 = VolumeFlexibilityByShannonRadii(picklestruct);
    a22 = detLatticeVectors(picklestruct)
    a23 = angleAnisotropy(picklestruct);
    #a24 = CellNegativeOxidationState(picklestruct)

    [a25, b25, c25, d25] =  deltaShannonCrystalRadii(picklestruct);
    a26 = ShannonRatio(picklestruct)
    a27 = ElectronegativitySolid(picklestruct)
    a28 = ChargeMomentOfInertia(picklestruct);
    a29 = MassMomentOfInertia(picklestruct);
    a30 = AvgNumberNN(picklestruct)
    adata = [a1, a2, a3, a4, a5, a6, a7, a8, a9,a11, a12, a13, a14, a15, a16, a17, a18, a20, a21, a22, a23, a26]; #a24];
    bdata = [b2, b5, b8, b20, c20, d20, b19, b11, c8, d8, c5, d5, a25, b25, c25, d25, b3]
    cdata = [a27, a28, a29, c11, a30];

    labelsa = ['Forces', 'avgCentralDistance', 'Coordination', 'numberDensity', 'initialAnisotropy',
              'li-ion fittability', 'maxForce', 'oxidation flexibility', 'ShannonRadii',
              'positiveoxidationpop', 'avgIonicRadVol', 'SpaceGroup', 'strainvolumeflexibility', 'Xcm', 'Ycm', 'Zcm',
              'volume flexibility of cell', 'deltaShannon', 'volumeshannonflex', 'detLatticeVec',
              'angle anisotropy', 'ShannonRatio']

    labelsb = ['avgCentralDistance Std', 'initialAnisotropy Std', 'oxidation flexibility Std', 'deltaShannonstd',
               'deltashannonmin', 'deltashannonmax', 'chargedensityvoldens', 'positiveoxpopdens', 'oxstateflexmin',
               'oxstateflexmax', 'anisotropynormcubevolmean', 'anisotropynormcubevolstd', 'deltacrystal1',
               'deltacrystal2','deltacrystal3','deltacrystal4', 'coordination std']

    labelsc = ['solid electronegativity', 'charge moment of inertia', 'mass moment of inertia', 'negativeoxdensity',
               'averageNumNN'];

    labels = labelsa + labelsb + labelsc
    data = adata + bdata + cdata;
    return [data, labels]







