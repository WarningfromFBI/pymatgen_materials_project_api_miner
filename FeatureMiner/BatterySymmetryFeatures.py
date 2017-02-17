import pymatgen as mg
import numpy as np
from sympy import *
import settings
import json
import FeatureMiner.FeatureMinerHelper.CalculationHelpers as ch
import FeatureMiner.FeatureMinerHelper.ShannonHelpers as sh
import LabelMiner.ClassifierCreation.CrystalSystem as cs
import pymatgen.analysis.bond_valence as pabv;
import pymatgen.symmetry.analyzer as psa
import LabelMiner.ClassifierCreation.CrystalSystem as cs

elementalValenceData = pabv.all_data;
#elementalValenceData contains two pieces of information, a bvsum and a 'occurence'

def getCrystalSystem(picklestruct):
    symmetry = psa.SpacegroupAnalyzer(picklestruct);
    numeric = cs.CrystalSysClassFeat(symmetry.get_crystal_system());
    return numeric;

def getCellSymmetryOps(picklestruct):
    symmetry = psa.SpacegroupAnalyzer(picklestruct);
    numSGOps = len(symmetry.get_symmetry_operations());
    return numSGOps;

def getShannonChargeStateStrength(picklestruct):
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
            d1 = site.frac_coords;
            neighborsites = oxistateStructure.get_neighbors(site, radius);
            for site2 in neighborsites:
                oxistate2 = site2[0].specie._oxi_state;
                d2 = site2[0].frac_coords; #we have to use frac_coords as it normalizes all materials
                F = oxistate2*oxistate/(np.dot(d1-d2, d1-d2))
                ShannonForces.append(F);
        return np.mean(ShannonForces);
    except ValueError as e:
        return 0

#got to fix this
def bondValenceData(picklestruct):
    BV = pabv.BVAnalyzer();
    try:
        oxistateStructure = BV.get_oxi_state_decorated_structure(picklestruct);
        bvmean = list(); bvstd = list(); occurrences = list();
        for site in oxistateStructure:
            key = site.species_string;
            bvdata = elementalValenceData['bvsum'][key]
            occurrencedata = elementalValenceData['occurrence'][key]
            bvmean.append(bvdata['mean'])
            bvstd.append(bvdata['std']); occurrences.append(occurrencedata);
        return [np.mean(bvmean), np.mean(bvstd), np.mean(occurrences)]
    except ValueError as e:
        bvmean = list();
        bvstd = list();
        occurrences = list();
        for site in picklestruct:
            key = site.species_string+'0+';
            bvdata = elementalValenceData['bvsum'][key]
            occurrencedata = elementalValenceData['occurrence'][key]
            bvmean.append(bvdata['mean'])
            bvstd.append(bvdata['std']);
            occurrences.append(occurrencedata);
        return [np.mean(bvmean), np.mean(bvstd), np.mean(occurrences)]


def GetAllSymmetries(picklestruct):
    a1 = getCrystalSystem(picklestruct)
    a2 = getCellSymmetryOps(picklestruct);
    a3 = getShannonChargeStateStrength(picklestruct);
    [a4, a5, a6] = bondValenceData(picklestruct);
    data = [a1, a2, a3, a4, a5, a6];
    labels = ['Crystal System', 'symmetry ops', 'ShannonForce', 'meanbv', 'stdbv', 'meanValenceOcc'];
    return [data, labels]

