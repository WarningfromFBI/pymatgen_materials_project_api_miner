import matplotlib.pyplot as plt
import pandas as pd
from sympy import *
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
plt.rcParams.update({'font.size': 32})
import pylab


def formulaUnitsperCell(datSci):
    numAtomsFormula = datsci['nsites']
    structure = mpr.get_structure_by_material_id(datSci['material_id']);
    totalAtoms = len(structure.as_dict()['sites'])
    formulaUnitsPerCell = totalAtoms / numAtomsFormula;
    return formulaUnitsPerCell;

def LiProportion(datSci):
    numLi = 0; numAtomsFormula = 0;
    for k in datSci['unit_cell_formula']:
        if (k == 'Li'):
            numLi = datSci['unit_cell_formula'][k];
        numAtomsFormula+=1;
    proportionLi = numLi/numAtomsFormula;
    return proportionLi;

MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);

#need a list of all the elements...
fieldnames = ['Electronegativity', ' Calculated Radius', ' First Ionization', ' Core Configuration',
              ' Heat of Vapor', ' Covalent Radius', ' Heat of Fusion', ' Bulk Modulus', ' Boiling Point',
              ' Brinell Hardness', ' Melting Point', ' Symbol', ' STP Density', ' Young Modulus', ' Shear Modulus',
              ' Vickers Hardness', ' Name', ' Common Ions', ' Second Ionization', ' Mass', ' Van der Waals Radius',
              ' Specific Heat', ' Thermal Cond.', ' Third Ionization', ' Series', ' Electron Affinity', ' Atomic Number',
              ' Mohs Hardness', ' Empirical Radius', '']

PeriodicTable = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\MaterialsProject\ElementDatabase\PeriodicTable.csv';
saveDirectory = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\Results\ExpansionsForBinaryLiCompounds';
elementSymbols = list();
with open(PeriodicTable, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    counter = 0;
    for row in reader:
        Symbol = row[11];
        elementSymbols.append(Symbol);
        counter+=1;

for i in elementSymbols:
    query = 'Li-'+i;
    try:
        data = mpr.get_data(query);
        print('element: '+i+', length:'+str(len(data)))
        if(len(data) < 3):
            continue;
        expansionData = list();
        for j in range(len(data)):
            datsci = data[j];
            Lithiumprop = LiProportion(datsci);
            normalization = formulaUnitsperCell(datsci);
            vol = datsci['volume']/normalization;
            expansionData.append([Lithiumprop, vol]);
        expansionData = np.array(expansionData)
        plt.figure();
        plt.scatter(expansionData[:,0], expansionData[:,1], s = 300)
        plt.title(i);
        pylab.savefig(saveDirectory+'\\'+'Li'+i+'.png')
    except Exception as e:
        print(e);
        continue;
    #this should list a bunch of lithium compounds paired with the element of interest