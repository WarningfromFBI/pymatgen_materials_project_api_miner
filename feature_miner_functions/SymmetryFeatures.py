import pymatgen as mg
import numpy as np
from sympy import *
import settings
import feature_miner_functions.FeatureMinerHelper.CalculationHelpers as ch
import pymatgen.analysis.bond_valence as pabv;
import pymatgen.symmetry.analyzer as psa
import label_miner_functions.ClassifierCreation.CrystalSystem as cs
import pymatgen.analysis.elasticity.strain as paes
import copy
import time
import pymatgen.analysis.structure_analyzer as pasa
import json
import pymatgen.analysis.energy_models as paem
import os
ShannonBase = os.path.join(settings.ROOT_DIR,'Shannon_Radii')
ShannonData = json.load(open(os.path.join(ShannonBase,'ShannonRadiiDictionary.json'), 'r'));
elemental_valence_data = pabv.all_data;
#elementalValenceData contains two pieces of information, a bvsum and a 'occurence'
bond_valences = elemental_valence_data['bvsum']; #process the bond valences to get averages for each element
average_bond_valences = dict();
for key in bond_valences:
    if(key[0:2] not in average_bond_valences.keys()):
        average_bond_valences[key[0:2]] = list();
    average_bond_valences[key[0:2]].append([bond_valences[key]['mean'], bond_valences[key]['std'], \
                                            elemental_valence_data['occurrence'][key]])
for key in average_bond_valences:
    data = np.array(average_bond_valences[key]);
    average_bond_valences[key] = np.mean(data, axis = 0)

def getCrystalSystem(picklestruct):
    symmetry = psa.SpacegroupAnalyzer(picklestruct);
    numeric = cs.CrystalSysClassFeat(symmetry.get_crystal_system());
    return numeric;

def getCellSymmetryOps(picklestruct):
    symmetry = psa.SpacegroupAnalyzer(picklestruct);
    numSGOps = len(symmetry.get_symmetry_operations());
    return numSGOps;

def avgDistanceOfNearestNeighbors(picklestruct): #WE NEED TO CALCULATE WITH A SUPERCELL, and CANNOT USE FRACCOORDS
    #also should take the ratio against the Li radius
    #we may need the pymatgen spacegroup analyzer
    #make a copy or else when we make supercell, we overwrite originalcell too
    initialvol = picklestruct.volume;
    originalcell = copy.copy(picklestruct); #we need to displace the origiinal cell so it is in the center of the supercell!!!!
    radius = 4 #4 angstroms is well motivated bond length, no scaling needed because we use physical dist to get nearest neighbors
    avgNNdist = list();
    print(len(originalcell))
    for site in originalcell: #could be on the order of 100
        time1 = time.time();
        distances = list();
        neighborsArray = originalcell.get_neighbors(site, radius); #radius should be nearest neighbors
        #print(len(neighborsArray))
        sitecoord = site.coords;
        for siteneighbor in neighborsArray: #order of 10, let's say
            neighborcoord = siteneighbor[0].coords; #we should use fractional coordinates here...
            dist = ch.getDist(neighborcoord, sitecoord);
            distances.append(dist);
        avgNNdist.append(np.mean(distances))
        time2 = time.time()
        #print(time2-time1)
    return [np.mean(avgNNdist), np.std(avgNNdist), np.max(avgNNdist), np.min(avgNNdist)]/initialvol**(1/3);

def getShannonChargeStrength(picklestruct):
    #the shannon charge state assigns an 'oxidation' to every atom...let's treat this
    #as a charge and then calculate the bond forces using the oxidation number
    #using coulomb's law
    try:
        BV = pabv.BVAnalyzer();
        oxistateStructure = BV.get_oxi_state_decorated_structure(picklestruct);
        radius =np.mean(picklestruct.lattice.abc);
        ShannonForces = list();
        for site in oxistateStructure.sites:
            oxistate = site.specie._oxi_state #this is the charge
            d1 = site.frac_coords; #use fractional coords as it is more comparable
            neighborsites = oxistateStructure.get_neighbors(site, radius);
            for site2 in neighborsites:
                oxistate2 = site2[0].specie._oxi_state;
                d2 = site2[0].frac_coords; #we have to use frac_coords as it normalizes all materials
                F = oxistate2*oxistate/(np.dot(d1-d2, d1-d2))
                ShannonForces.append(F);
        return np.mean(ShannonForces);
    except ValueError as e:
        return 0

#get bond valence sum for all sites in the cell, average
def bondValenceData(picklestruct):
    BV = pabv.BVAnalyzer();
    try:
        oxistateStructure = BV.get_oxi_state_decorated_structure(picklestruct);
        #the oxistate structure is required as the bvsum data keys are oxidated state data;
        bvmean = list(); bvstd = list(); occurrences = list();
        for site in oxistateStructure:
            key = site.species_string;
            bvdata = elemental_valence_data['bvsum'][key]
            occurrencedata = elemental_valence_data['occurrence'][key]
            bvmean.append(bvdata['mean'])
            bvstd.append(bvdata['std']); occurrences.append(occurrencedata);
        return [np.mean(bvmean), np.mean(bvstd), np.mean(occurrences)]
    #value error is thrown whenever valences cannot be assigned to the compound
    except ValueError as e: #this is not good as compounds such as Li17Nb20O60 get zero valence but really aren't
                            #zero valence compounds
        # in such a case, what we will do is to calculate a heuristic elemental valence
        bvmean = list();
        bvstd = list();
        occurrences = list();
        for site in picklestruct:
            key = site.species_string;
            if(key not in average_bond_valences.keys()):
                continue;
            else:
                bvdata = average_bond_valences[key][0:2]
                occurrencedata = average_bond_valences[key][2]
                bvmean.append(bvdata[0])
                bvstd.append(bvdata[1]);
                occurrences.append(occurrencedata);
        return [np.mean(bvmean), np.mean(bvstd), np.mean(occurrences)]

def bondValenceProbabilities(picklestruct):
    BV = pabv.BVAnalyzer();
    netCharges = list();
    for site in picklestruct.sites:
        ans = BV._calc_site_probabilities(site, picklestruct.get_neighbors(site,4))
        netCharge = 0;
        for key in ans:
            netCharge += key*ans[key];
        netCharges.append(netCharge)
    return [np.mean(netCharges), np.std(netCharges)];

#our attempt to do a simple first principles approximation of the vegard coefficients
def VegardCoefficientsApprox(picklestruct):
    latticeParams = picklestruct.lattice.abc;
    a = latticeParams[0]; b = latticeParams[1]; c = latticeParams[2]
    volumeinit = picklestruct.volume;
    LiLatt = [2.9, 2.9, 2.9] #units of angstroms
    #we'll lithiate to 10% of the composition
    predx = LiLatt[0]*0.1 + 0.9*latticeParams[0];
    predy = LiLatt[1]*0.1 + 0.9*latticeParams[1];
    predz = LiLatt[2]*0.1 + 0.9*latticeParams[2];
    #predx, predy, predz by themselves aren't that meaningful
    return [predx*predy*predz/volumeinit]; #predx, predy, predz don't seem particularly useful

def Hall_Number(picklestruct): #return hall_number, which is just another way of listing a spacegroup number
    symmetryDat = psa.SpacegroupAnalyzer(picklestruct);
    return symmetryDat.get_symmetry_dataset()['hall_number'];

# def StrainLattice(picklestruct): #Might be able to produce a first order estimate of poisson's ratio from here
#     initialvol = picklestruct.volume;
#     initiallattice = np.array(picklestruct.lattice.abc);
#     strainedLatt = paes.DeformedStructureSet(picklestruct, norm_strains= [0.1, 0.1, 0.1] \
#                                              , shear_strains = [0.1, 0.1, 0.1])
#     strainedDict = strainedLatt.deformations;
#     volumeChanges = list();
#     for deformation in strainedDict:
#         newVol = (deformation.volume) #we should normalize this against the 'magnitude' of the strain
#         newlattice = np.array(deformation.lattice.abc);
#         volDiff = newVol-initialvol;
#         latticeDiff = newlattice-initiallattice;
#         volumeChanges.append(volDiff/(np.dot((latticeDiff), (latticeDiff)))**0.5)
#     #now quantify how flexible the lattice is given the stain dict...
#     return [np.mean(volumeChanges), np.std(volumeChanges)]

def ionicityOfLattice(picklestruct):
    #AS a general rule, ionic bonds are stronger than covalent bonds
    #perhaps materials with more ionic bonds tend to resist lithium intercalation more
    r = 4; #four angstroms is a very good motivation for bond length (though this will overestimate small bonds)
    #we have to scale r as we play with fractional coordinates
    initialvol = picklestruct.volume;
    originalcell = copy.copy(picklestruct);
    ionicCount = list();
    for site in originalcell.sites:
        elementElectroneg = site.specie.X;
        sitecoord = site.coords;
        subcount = list(); subionicity = list();
        neighborsArray = originalcell.get_neighbors(site, r)
        ionic = 0;
        for siteneighbor in neighborsArray:
            neighborElectroneg = siteneighbor[0].specie.X;
            neighborcoord = siteneighbor[0].frac_coords; #we should use fractional coordinates here...
            dist = ch.getDist(neighborcoord, sitecoord);
            if(abs(elementElectroneg-neighborElectroneg) >2):
                ionic+=1;
            subionicity.append(abs(elementElectroneg-neighborElectroneg))
        ionicCount.append(ionic)
    return [np.mean(ionicCount)/len(picklestruct.sites), np.mean(subionicity)];

def AtomicPackingFraction(picklestruct): #we'll use Austin's version of this,
    #which is like what we calculated, but he uses a statistical sampling method to account for potential
    #overlap of the hard spheres
    return None

def getBravaisLattice(picklestruct): #there are fourteen bravais lattices, so to some extent, this seems more differentiating than crystal system
    #need the conventional standard cell
    return None;

def bondOrderParameters(picklestruct):#this is super slow, #other order parameters, cn = coordination number
    labels = ["bcc", "oct", "q4","q6","q2","cn", "tet", "bent", "reg_tri","sq","sq_pyr"]
    structureBonds = pasa.OrderParameters(labels);
    Data = list();
    for i in range(len(picklestruct.sites)):
        orderparams = structureBonds.get_order_parameters(picklestruct, i);
        Data.append(orderparams);

    Data = np.array(Data); #rows represent each site in the atom, columsn represent each order param
    d = Data.shape;
    avgedAns = list();
    for i in range(d[1]): #we want average over all columns
        avgedAns.append(np.mean(Data[:,i]));
    return avgedAns;

def EwaldEnergetics(picklestruct):
    BV = pabv.BVAnalyzer();
    Ewald = paem.EwaldElectrostaticModel();
    try:
        oxi_struct = BV.get_oxi_state_decorated_structure(picklestruct);
        #what's the exception case if we cannot decorate the structure with oxidation numbers?
        energy = Ewald.get_energy(oxi_struct);
        return energy;
    except Exception as e:
        #this is problematic...for anything for which we can't assign a valence structure
        #we just give every state the maximum possible oxidation state.
        #Ewald calculator does not like charged structures.
        oxDict = dict();
        Ewald = paem.EwaldElectrostaticModel();
        for site in picklestruct.sites:
            elem = site.specie.value;
            ShannonPoint = ShannonData[elem];
            rad = 0;
            charge = np.mean(site.specie.common_oxidation_states)
            maxOx = -float('Inf');
            for i in ShannonPoint:
                if(i['oxidation_num'] > maxOx):
                    maxOx = i['oxidation_num']
            oxDict[elem] = maxOx;
        picklestruct.add_oxidation_state_by_element(oxDict);
        energy = Ewald.get_energy(picklestruct)
        return energy;

def IsingEnergetics(picklestruct):
    radius = 4; J = 1; #this interaction parameter should depend on something, not be uniform
    Ising = paem.IsingModel(J, radius);
    return Ising.get_energy(picklestruct);



def GetAllSymmetries(picklestruct):
    print(picklestruct.composition)
    a1 = getCrystalSystem(picklestruct)
    a2 = getCellSymmetryOps(picklestruct);
    a3 = getShannonChargeStrength(picklestruct);
    [a4, a5, a6] = bondValenceData(picklestruct);
    a10 = VegardCoefficientsApprox(picklestruct);
    a11 = Hall_Number(picklestruct)
    #[a12, a13] = StrainLattice(picklestruct)
    [a14, a15] = ionicityOfLattice(picklestruct) #putting picklestruct here changes picklestruct
    t0 = time.time();
    [a16, b16, c16, d16] = avgDistanceOfNearestNeighbors(picklestruct)
    #[a17, b17] = bondValenceProbabilities(picklestruct);
    #a18 = EwaldEnergetics(picklestruct)
    bondParams = bondOrderParameters(picklestruct)
    t1 = time.time();
    print(t1 - t0);

    adata = [a1, a2, a3, a4, a5, a6, a10, a11,  a14, a15, a16, b16, c16, d16] + bondParams;
    labelsa = ['Crystal System', 'symmetry ops', 'ShannonForce', 'meanbv', 'stdbv', 'meanValenceOcc',
              'VegardVolume', 'Hall Number', 'ioniccount', 'ionicitymean', 'NNdist',
              'NNdiststd', 'nndistmax', 'nndistmin'] + ["bcc", "oct", "q4","q6","q2","cn", "tet", "bent", "reg_tri","sq","sq_pyr"];

    #labelsb = ['EwaldApprox'];

    labels = labelsa;
    data = adata

    return [data, labels]


