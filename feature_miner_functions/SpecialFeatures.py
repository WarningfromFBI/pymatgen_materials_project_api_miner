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

'''
Mine features which we missed in the previous feature miners
 'maxCentralDistance', 'minCentralDistance', 
 'ENMax', 'ENMin', 'ENStd', 
 'STDnumNN', 
  'Voronoi Coord Mean', 'Voronoi Coord STD', 'VoronoiPoly1', 'VoronoiPoly2', 
  'ShannonMaxForceSTD', 'ShannonForceMinMean', 'ShannonForceMinStd',

## going to get rid of the voronoi features

'''

def electronegativity(picklestruct):
    '''
        calculates cumulative statistic giving the atomic electronegativities
    '''
    #iterate through all the atoms in the picklestruct, get electronegativities for them
    EN = list();
    for sites in picklestruct.sites:
        elem = sites.specie
        pauling_electronegativity = elem.X; #0 assigned to those without one
        EN.append(pauling_electronegativity);
    #for tracking, it is probably easier to design the features
    #so that the return object is a dictionary
    data = {'EN_mean': np.mean(EN), 'ENmax': np.max(EN), 'ENmin': np.min(EN), \
            'ENStd': np.std(EN)}
    return data;



def DistancefromCoM(picklestruct):
    '''
    :param picklestruct:
    :return: average distance of sites in structure from the COM
    '''

    def CenterofMass(picklestruct):
        '''
        centerofmass in terms of fractional coordinates
        :param picklestruct:
        :return:
        '''
        symmetryfinder = psa.SpacegroupAnalyzer(picklestruct)
        numerator = np.array([0.0, 0.0, 0.0])
        denominator = list();
        for sites in picklestruct.sites:
            mass = sites.specie.data['Atomic mass']
            cellPosition = sites.frac_coords;  # normalized
            numerator += cellPosition * mass
            denominator.append(mass);
        return numerator / (np.mean(denominator));
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
    data = { 'maxCentralDistance': np.max(R), 'minCentralDistance': np.min(R), \
             'avgCentralDistance': np.mean(R), 'avgCentralDistance Std': np.std(R)}
    return data

# def Voronoi(picklestruct):
#     '''
#     :param picklestruct:
#     :return: average distance of sites in structure from the COM
#     '''
#     pasa.VoronoiAnalyzer.

