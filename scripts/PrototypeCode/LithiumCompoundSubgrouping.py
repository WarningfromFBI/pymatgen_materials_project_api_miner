
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
import pickle

## GOAL: Calculate Center of Mass per Unit Cell
file2 = open(r'D:\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataSets\unitcelldict.pkl', 'rb')
unitcelldict = pickle.load(file2)
file2.close()

f = open('D:\\Nathan\Documents\StanfordYearOne\Reed Group\MachineLearningPractice\Datasets\LithiumBattery.csv', 'r')
lithComp = list();
for line in f:
    data = line.split(",")
    print(data)
    lithComp.append(data[0].strip("\""));
#Access battery data
def get_battery_data(formula_or_batt_id):
    """Returns batteries from a batt id or formula
    Examples:
        get_battery("mp-300585433")
        get_battery("LiFePO4")
    """
    return mpr._make_request('/battery/%s' % formula_or_batt_id)

MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);
deltaVol = dict(); energy = list(); frac = list();
compoundNames = list(); lithId = dict(); unlithId = dict();
cin = 0;
for compound in lithComp:
    if(compound == "Battid"): #there are often several entries for a given material composition
        continue;
    results = mpr.get_battery_data = get_battery_data(compound)
    print(compound)
    name = results[0]['adj_pairs'][0]['formula_discharge']
    deltaVol[name] = (results[0]['adj_pairs'][0]['max_delta_volume'])
    compoundNames.append(name)
    lithId[name] = (results[0]['adj_pairs'][0]['id_discharge'])
    unlithId[name] = (results[0]['adj_pairs'][0]['id_charge']) #id-discharge does not corresond
    cin += 1;
    # if(cin > 20): #data extraction is slow
    #     break;

#deltaVol...visualization
# convert dictionary to list
deltaVolList = list();
for i in deltaVol:
    deltaVolList.append(deltaVol[i])
plt.hist(deltaVolList, 100);
plt.title('Volume Change for Lithium Intercalation Compounds')
plt.xlabel('proportion expansion')
plt.ylabel('counts')

classifiers = list();
for i in range(len(deltaVolList)):
    if(deltaVolList[i] > 0.1):
        classifiers.append(1)
    else:
        classifiers.append(0)

## Let's group data by compound type (or crystal type)
ElementGroups = dict();
counter = 0; GroupMappings = dict(); CompoundLabels = dict(); cmplab = list();
for comp in compoundNames:
    print(comp+", "+str(counter));
    unlithstruct = mpr.get_data(unlithId[comp]);
    spaceG = unlithstruct[0]['spacegroup']['crystal_system']
    if(spaceG in ElementGroups.keys()):
        ElementGroups[spaceG] += 1;
    else:
        ElementGroups[spaceG] = 1;
        counter += 1;
        GroupMappings[spaceG] = counter
    CompoundLabels[comp] = GroupMappings[spaceG]
    cmplab.append(GroupMappings[spaceG])


# Grouping by bilayer phase
