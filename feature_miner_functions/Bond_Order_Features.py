import pymatgen as mg
import numpy as np
from sympy import *
import settings
import feature_miner_functions.FeatureMinerHelper.CalculationHelpers as ch
import pymatgen.analysis.bond_valence as pabv;
import label_miner_functions.ClassifierCreation.CrystalSystem as cs
import copy
import time
import pymatgen.analysis.structure_analyzer as pasa
import json
import os
ShannonBase = os.path.join(settings.ROOT_DIR,'Shannon_Radii')
ShannonData = json.load(open(os.path.join(ShannonBase,'ShannonRadiiDictionary.json'), 'r'));
elemental_valence_data = pabv.all_data;
#elementalValenceData contains two pieces of information, a bvsum and a 'occurence'
bond_valences = elemental_valence_data['bvsum']; #process the bond valences to get averages for each element
average_bond_valences = dict();

'''
These are the single most expensive features to mine, which is why they get their own separate little script
'''

for key in bond_valences:
    if(key[0:2] not in average_bond_valences.keys()):
        average_bond_valences[key[0:2]] = list();
    average_bond_valences[key[0:2]].append([bond_valences[key]['mean'], bond_valences[key]['std'], \
                                            elemental_valence_data['occurrence'][key]])
for key in average_bond_valences:
    data = np.array(average_bond_valences[key]);
    average_bond_valences[key] = np.mean(data, axis = 0)


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
        data = { 'meanbv':np.mean(bvmean), 'stdbv': np.mean(bvstd), 'meanValenceOcc': np.mean(occurrences)}
        return data
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
        data = {'meanbv': np.mean(bvmean), 'stdbv': np.mean(bvstd), 'meanValenceOcc': np.mean(occurrences)}
        return data

def bondValenceProbabilities(picklestruct):
    '''
    for some reason, this got excluded
    :param picklestruct:
    :return:
    '''
    BV = pabv.BVAnalyzer();
    netCharges = list();
    for site in picklestruct.sites:
        try:
            ans = BV._calc_site_probabilities(site, picklestruct.get_neighbors(site,4))
            netCharge = 0;
            for key in ans:
                netCharge += key*ans[key];
            netCharges.append(netCharge)
        except Exception as e:
            continue;
    if(len(netCharges) == 0):
        netCharges = [0];
    data = {'bv_prob_mean': np.mean(netCharges), 'bv_prob_std': np.std(netCharges)};
    return data;


def bondOrderParameters(picklestruct):
    #this is super slow, which seems odd, #other order parameters, cn = coordination number
    '''
    :param picklestruct:
    :return:
    '''
    labels = ["bcc", "oct", "q4","q6","q2","cn", "tet", "bent", "reg_tri","sq","sq_pyr"]
    structureBonds = pasa.OrderParameters(labels);
    Data = list();
    for i in range(len(picklestruct.sites)):
        orderparams = structureBonds.get_order_parameters(picklestruct, i);
        Data.append(orderparams);
    Data = np.array(Data); #rows represent each site in the atom, columsn represent each order param
    avgedAns = np.mean(Data, axis = 1)
    #convert to dictionary
    data = dict(zip(labels, avgedAns))
    return data;




