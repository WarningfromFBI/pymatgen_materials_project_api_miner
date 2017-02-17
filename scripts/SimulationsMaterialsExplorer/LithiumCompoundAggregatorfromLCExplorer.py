import pymatgen as mg
import numpy as np
import scipy
from sklearn.datasets import load_digits
from sklearn.datasets import load_iris
from sklearn.datasets import load_breast_cancer;
from sklearn.datasets import load_boston;
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn.linear_model import Ridge;
from sklearn import svm;
import matplotlib.pyplot as plt
import pandas as pd
from sympy import *
import os
import string
from sklearn import preprocessing
from sklearn import model_selection;
from sklearn.preprocessing import StandardScaler
from pymatgen.matproj.rest import MPRester
from pymatgen.phasediagram.maker import PhaseDiagram
from pymatgen.electronic_structure.plotter import BSPlotter;
from pymatgen import core
from mpl_toolkits.mplot3d import Axes3D;
import requests;
import math
import re;

## ANOTHER ATTEMPT TO SEARCH THROUGH THE LITHIUMMPIDS and GENERATE VIABLE BATTERY COMPOUND PAIRS

MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);

def get_battery_data(formula_or_batt_id):
    """Returns batteries from a batt id or formula
    Examples:
        get_battery("mp-300585433")
        get_battery("LiFePO4")
    """
    return mpr._make_request('/battery/%s' % formula_or_batt_id)

def BatterySearchGenerator(elements):
    counter = 0; hyphenIndices = list();
    for i in range(len(elements)-1):
        if(elements[i].islower()):
            hyphenIndices.append(counter);
        elif(elements[i+1].isupper()):
            hyphenIndices.append(counter);
        counter+=1;
    c2 = 0; #this accounts for the fact that the string grows every time we put in a '-'
    for i in hyphenIndices:
        elements = elements[:i+c2+1]+'-'+elements[i+c2+1:]
        c2 +=1;
    return elements;

#Iterate through all lithium compounds and search by formula for batteries
f = open('D:\\Nathan\Documents\StanfordYearOne\Reed Group\MaterialsProject\MP_data\LithiumMPIdsDict.txt', 'r')
counter = 0;
BatteryBase = list();
for i in f:
    BatteryIDs = dict();
    compoundDat = (i.rstrip().split(', '))
    formula = compoundDat[0];
    elemSymbols = " ".join(re.findall("[a-zA-Z]+", formula));
    #print(elemSymbols)
    elemSymbols = elemSymbols.replace(' ','');
    elements = BatterySearchGenerator(elemSymbols);
    print(formula)
    battery = mpr.get_battery_data = get_battery_data(formula);
    print(battery)
    if(len(battery) == 0):
        continue;
    BatteryIDs['battid'] = battery[0]['battid'];
    BatteryIDs['components'] = battery[0]['adj_pairs'][0]['material_ids']
    BatteryBase.append(BatteryIDs);
    counter+=1;


g = open('D:\\Nathan\Documents\StanfordYearOne\Reed Group\MaterialsProject\MP_data\LithiumBatteryData.txt', 'w')
for i in BatteryBase:
    for keys in i:
        g.write(keys+"," + "".join(i[keys])+ " ");
    g.write('\n')
g.close();