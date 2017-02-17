import pymatgen as mg
import numpy as np
from sympy import *
import settings
import json
import FeatureMiner.FeatureMinerHelper.CalculationHelpers as ch
import FeatureMiner.FeatureMinerHelper.ShannonHelpers as sh
import LabelMiner.ClassifierCreation.CrystalSystem as cs
import pymatgen.symmetry.analyzer as psa

structureDir = settings.MaterialsProject+'\\StructureBase'
ShannonBase = settings.MaterialsProject+'\\ShannonRadii'
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
    totcoordinNum = 0;
    for i in range(len(sitesDat)):
        elem = sitesDat[i];
        coordinNum = elem['properties']['coordination_no'];
        totcoordinNum += coordinNum;
    avgcoordinNum = totcoordinNum/len(sitesDat);
    return avgcoordinNum;

def numberDensity(structure): #number density of the entire lattice of the unlithiated compound
    volume = structure['lattice']['volume'];
    return len(structure['sites'])/volume;

def avgDistancefromOrigin(sitesDat):
    #lattice is the datastructure from
    RCM = np.array([0, 0, 0]);
    totalR = 0;
    for i in range(len(sitesDat)):
        elem = sitesDat[i];
        # extract element and calculate mass
        atom = mg.Element(elem['label']);
        R = elem['xyz']; dr = 0;
        for j in range(3):
            dx = R[j] - RCM[j];
            dr += dx **2;
        dr = dr**0.5;
    totalR += dr;
    return totalR/len(sitesDat);


    avgcoordinNum = totcoordinNum / len(sitesDat);
    return avgcoordinNum;

def unlithanisotropy(picklestruct):
    unitcelllengths = picklestruct.lattice.abc;
    diffs = list();
    for i in range(3):
        for j in range(i,3):
            diff = unitcelllengths[i]-unitcelllengths[j];
            diffs.append(diff);
    diffs = np.array(diffs);
    return np.mean(diffs);

def celltosphereRatio(picklestruct): #attempts to account for how rectangular the cell is by taking the smallest
    #unit cell length, and seeing how much larger or smaller than it is compared to the lithium atom volume
    unitcelllengths = picklestruct.lattice.abc
    minlength = np.min(unitcelllengths);
    Lirad = mg.Element('Li').average_ionic_radius
    diff = ch.sphereVol(minlength/2) - ch.sphereVol(Lirad);
    return diff;

#get the nearest neighbors to every element in the lattice, calculate average distances
def avgDistanceOfNearestNeighbors(picklestruct):
    #also should take the ratio against the Li radius
    radius = np.min(picklestruct.lattice.abc);
    avgNNdist = list();
    for site in picklestruct:
        distances = list();
        neighborsArray = picklestruct.get_neighbors(site, radius); #radius should be nearest neighbors
        sitecoord = site.coords;
        for siteneighbor in neighborsArray:
            neighborcoord = siteneighbor[0].coords;
            dist = ch.getDist(neighborcoord, sitecoord);
            distances.append(dist);
    avgNNdist.append(np.mean(distances))
    return np.mean(avgNNdist);

#Li always has a +1 oxidation state in an atom, which means upon lithiation, materials should reduce
#their oxidation state... get a sense of how willing the constituents are to decrease their oxidation state
def oxidationStateFlexibility(pickleStruct):
    diffs = list();
    for site in pickleStruct.sites:
        minox = site.specie.min_oxidation_state
        maxox = site.specie.max_oxidation_state;
        diff = maxox-minox; diffs.append(diff);
    return np.mean(diffs);

def oxidationStateVolumeFlexibility(pickleStruct):
    #how much does atomic volume change when charge state changes
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
    return VolChange;

def VolumeByAvgIonicRadius(pickleStruct):
    volume = pickleStruct.volume;
    Vtot = 0;
    for site in pickleStruct.sites:
        elem = site.specie;
        avgionicrad = elem.average_ionic_radius
        Vtot += ch.sphereVol(avgionicrad);
    return volume - Vtot;

#SHANNON RADII MINING
def VolumeByShannonRadii(pickleStruct):
    volume = pickleStruct.volume;
    Vtot = 0;
    for site in pickleStruct.sites:
        elem = site.specie.value;
        coordin_no = site.coordination_no;
        ShannonPoint = ShannonData[elem];
        v = 0;
        for i in ShannonPoint:
            if(i['coordination_no'] == coordin_no):
                rad = i['ionic_radius'];
            else:
                rad = site.specie.average_ionic_radius
            v = ch.sphereVol(rad);
        Vtot += v;
    return volume - Vtot;

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
    return TotDeltaVol;

def deltaShannonRadii(pickleStruct):
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
    return np.mean(deltaVolList);

#if the unit cell atoms consist of mostly positive oxidation state elements, then why would it let lithium come in?
def CellPositiveOxidationState(pickleStruct):
    positiveOxPop = 0;
    for site in pickleStruct.sites:
        elem = site.specie.value;
        coordin_no = site.coordination_no;
        ShannonPoint = ShannonData[elem];
        check = True;
        for i in ShannonPoint:
            if(i['oxidation_num'] < 0):
                check = False;
        if(check == True):
            positiveOxPop+=1;
    return positiveOxPop;

def SpaceGroup(picklestruct):
    return picklestruct.get_space_group_info()[1];

def detLatticeVectors(picklestruct):
    latticeVec = picklestruct.lattice.matrix;
    determinant = np.linalg.det(latticeVec);
    return determinant;

def CenterofMass(picklestruct):
    numerator = np.array([0.0, 0.0, 0.0])
    denominator = list();
    for sites in picklestruct.sites:
        elem = sites.specie.name;
        mass = sites.specie.data['Atomic mass']
        # get the element from the wolverton
        cellPosition = sites.frac_coords;
        numerator += cellPosition*mass
        denominator.append(mass);
    return numerator/(np.mean(denominator));

def AtomicNumberDensity(picklestruct): #gives a rough idea of the 'electron density'
    #this may be weird as a lot of electrons in heavy elements are tightly bound to the nucleus
    total = 0;
    for sites in picklestruct.sites:
        elem = sites.specie
        atmNum = sites.specie.data['Atomic no']
        total+=atmNum;
    return total/len(picklestruct.sites);

#apply strains and see how much the volume changes
def volumeChangeUponStrain(picklestruct):
    initialVol = picklestruct.volume;
    picklestruct.apply_strain(0.01);
    finalVol = picklestruct.volume;
    return (finalVol-initialVol); #this isn't that great...all it can really differentiate is what kind of crystal structure the thing has

def angleAnisotropy(picklestruct):
    latticeAng = picklestruct.lattice.angles
    return np.std(latticeAng)

def changeinForceUponStrain(picklestruct):

    picklestruct.apply_strain(0.01);
    for site in picklestruct:
        r = site.coords;
    return None

def latticeStrainability():
    return None;

##=================FUNCTION TO APPLY ALL THESE FUNCTIONS AT ONCE ==============================#


def GetAllStructureFeatures(structure, picklestruct):
    sitesDat = structure['sites']
    try:
        [a1, a7] = Forces(sitesDat)
        a2 = avgDistancefromOrigin(sitesDat)
        a3 = coordinationNumber(sitesDat); #not all data points contain coordination numbers
        a4 = numberDensity(structure)
        a5 = unlithanisotropy(picklestruct)
        a6 = celltosphereRatio(picklestruct);
        a8 = oxidationStateFlexibility(picklestruct);
        a9 = VolumeByShannonRadii(picklestruct);
        a10 = avgDistanceOfNearestNeighbors(picklestruct);
        a11 = CellPositiveOxidationState(picklestruct)
        a12 = VolumeByAvgIonicRadius(picklestruct)
        a13 = SpaceGroup(picklestruct);
        a14 = volumeChangeUponStrain(picklestruct)
        [a15, a16, a17] = CenterofMass(picklestruct)
        a18 = oxidationStateVolumeFlexibility(picklestruct)
        a19  = AtomicNumberDensity(picklestruct)
        a20 = deltaShannonRadii(picklestruct)
        a21 = VolumeFlexibilityByShannonRadii(picklestruct);
        a22 = detLatticeVectors(picklestruct)
        a23 = angleAnisotropy(picklestruct);
        data = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10,a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22,a23];
        labels = ['Forces', 'avgCentralDistance', 'numberDensity', 'Coordination', 'initialAnisotropy',
                  'li-ion fittability', 'maxForce', 'oxidation flexibility', 'ShannonRadii', 'NNDist',
                  'positiveoxidationpop', 'avgIonicRadVol', 'SpaceGroup', 'strainvolumeflexibility', 'Xcm', 'Ycm', 'Zcm',
                  'volume flexibility of cell', 'AtomicNum Density', 'deltaShannon', 'volumeshannonflex', 'detLatticeVec',
                  'angle anisotropy']

        return [data, labels]
    except Exception as e:
        print(e)






