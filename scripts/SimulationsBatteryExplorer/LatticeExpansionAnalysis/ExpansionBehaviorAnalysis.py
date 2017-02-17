import matplotlib.pyplot as plt
import pandas as pd
from sympy import *
import pylab;
import os
import string
from pymatgen.matproj.rest import MPRester
from pymatgen.phasediagram.maker import PhaseDiagram
from pymatgen.electronic_structure.plotter import BSPlotter;
from pymatgen import core
from mpl_toolkits.mplot3d import Axes3D;
import requests;
import math
import re; import csv
import json
import pymatgen as mg
#analysis packages
import numpy as np
plt.close("all")
# A basic analysis of how the volume changes with different levels of lithiation
MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);

Silicon = 'Li-Ni-O'
LiCoO2 = 'Li-Co-O'
LiAl = 'Li-In-Sb'
LiGe = 'Li-Nb-O'
LiFePO4 = 'Li-Fe-P-O'
Si = mg.Element('Si').data;
queries = [Silicon, LiAl, LiGe, LiFePO4, LiCoO2];
LayeredFile = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\MinedFeatureSets\CoO2Layered.csv';
results = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\Results\ExpansionBehavior'
layeredCoO2Dict = dict();
with open(LayeredFile, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        x = (row[0].split(','))
        if(x[0] in layeredCoO2Dict.keys()):
            continue;
        layeredCoO2Dict[x[0]] = x[1];
CoO2Layered = list(); CoO2prop = list();

for i in queries:
    datSci = mpr.get_data(i);
    propLi = list(); volumes = list();
    for j in range(len(datSci)):
        compound = datSci[j];
        if(compound['e_above_hull']> 0.1):
            continue;
        print(compound['pretty_formula'])
        numAtomsFormula = compound['nsites']
        #get amount of Li
        numLi = 0; numAtomsUnitCell = 0;
        for k in datSci[j]['unit_cell_formula']:
            if(k == 'Li'):
                numLi = datSci[j]['unit_cell_formula'][k];
            # numAtomsUnitCell+=1; #this yields good looking data
            numAtomsUnitCell+=datSci[j]['unit_cell_formula'][k];
        proportionLi = numLi/numAtomsUnitCell;
        propLi.append(proportionLi);
        #NEED TO NORMALIZE VOLUME
        structure = mpr.get_structure_by_material_id(datSci[j]['material_id']);
        totalAtoms = len(structure.as_dict()['sites'])
        formulaUnitsPerCell = totalAtoms/numAtomsFormula;

        if(i=='Li-Co-O'): #CoO2 analysis
            if(datSci[j]['material_id'] in layeredCoO2Dict.keys()):
                CoO2prop.append(proportionLi);
                CoO2Layered.append(datSci[j]['volume']/formulaUnitsPerCell)
        volumes.append(datSci[j]['volume']/formulaUnitsPerCell);
    plt.figure(figsize=(20,10));
    plt.scatter(propLi, volumes, s = 200)
    plt.title(i);
    plt.xlabel('proportion of Lithium (fractional)')
    plt.ylabel('Volume of Compound (Angstroms cubed)')
    plt.rcParams.update({'font.size': 30})
    file = results+'\\'+i+'.png';
    pylab.savefig(file)
plt.scatter(CoO2prop, CoO2Layered, s = 300, c = 'r')
plt.show()


