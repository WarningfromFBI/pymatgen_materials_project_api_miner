
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

#general script to extract all battery statistics in one pass into a single data structure
BatteryMatrix = list();
for compound in lithComp:
    if(compound == "Battid"):
        continue;
    results = mpr.get_battery_data = get_battery_data(compound)
    print(compound)
    l1 = list();
    for i in results[0]:
        l1.append(results[0][i]);
    BatteryMatrix.append(l1)

S = np.array(BatteryMatrix);
lithstruct = dict();

counter = 0;

UnitCellParams = list(); Forces = list(); Fmaxes = list(); CMR = list(); Coordination = list();
UnitCellParamsLith = list(); #this is so we can get the change in the unit cell parameters
#calculate distance from CenterofMass
for comp in compoundNames:
    print(comp+", "+str(counter));
    unlithstruct = mpr.get_structures(unlithId[comp]);
    lithstruct = mpr.get_structures(lithId[comp]);
    dictstruct = unlithstruct[0].as_dict();
    dictstructlith = lithstruct[0].as_dict();
    latticeDatlith = dictstructlith['lattice'];
    latticeDat = dictstruct['lattice'];
    sitesDat = dictstruct['sites'];
    AvgForces = 0;
    Fmax = np.array([0.0,0.0,0.0]);
    Rcm = np.zeros(3);
    Mtot = 0; maxcoordinNum = 0;
    for i in range(len(sitesDat)):
        F = 0;
        elem = sitesDat[i];
        #extract element and calculate mass
        atom = mg.Element(elem['label']); mass = atom.number; Mtot += mass;
        forces = elem['properties']['forces']
        coordinNum = elem['properties']['coordination_no'];
        if(coordinNum > maxcoordinNum): maxcoordinNum = coordinNum;
        coordinates = elem['xyz'];
        for j in range(3):
            Rcm[j]+=coordinates[j]*mass;
            F+=forces[j]**2
            if(abs(forces[j]) > Fmax[j]):
                Fmax[j] = abs(forces[j]);
        F = F**.5;
    Coordination.append(maxcoordinNum);
    Rcm = Rcm/Mtot;
    Rcenter = np.array([latticeDat['a']/2, latticeDat['b']/2, latticeDat['c']/2])
    Rcm -= Rcenter;
    CMR.append(Rcm);
    AvgForces += F/(i+1); Forces.append(AvgForces)
    Fmaxes.append(Fmax);
    UnitCellParamsLith.append([latticeDatlith['a'], latticeDatlith['b'], latticeDatlith['c'],
                               latticeDatlith['alpha'], latticeDatlith['beta'], latticeDatlith['gamma']])
    UnitCellParams.append([latticeDat['a'], latticeDat['b'], latticeDat['c'],
                           latticeDat['alpha'], latticeDat['beta'], latticeDat['gamma']])
    counter += 1;
    # if(counter > 20):
    #     break;

#calculate differences in unit cell parameters
DifferenceCellParam = list(); predDeltaVol = list()
for i in range(len(UnitCellParams)):
    rlith = UnitCellParamsLith[i];
    runlith = UnitCellParams[i];
    diff = np.array(rlith) - np.array(runlith);
    print(len(DifferenceCellParam));
    DifferenceCellParam.append(diff);
    predDeltaVol.append(np.prod(diff))
DifferenceCellParam = np.array(DifferenceCellParam)
## extract structure data
unitCellParams = np.array(UnitCellParams)
NetVolume= list();
for i in range(len(UnitCellParams)):
    product = unitCellParams[i,0]*unitCellParams[i,1]*unitCellParams[i,2];
    NetVolume.append(product)

Fmaxl = np.array(Fmaxes); cmr = np.array(CMR)
plt.figure();
plt.scatter(NetVolume[:291], Coordination[:291], s = 400, c = classifiers) #lattice forces doesn't correlate well with volume chan=ge

# 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(cmr[:,0], cmr[:,1], cmr[:,2])
# 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.scatter(cmr[:291,0], cmr[:291,1], cmr[:291,2], s = 200, c = classifiers)
ax.scatter(DifferenceCellParam[:291, 0], DifferenceCellParam[:291,1], DifferenceCellParam[:291,2],
           s = 200, c = classif21, cmap = 'viridis')

#Collect all predictors into a single Matrix;
Matrix = np.concatenate((cmr, UnitCellParams, DifferenceCellParam,
                         np.reshape(np.array(Forces), (340,1))), axis = 1);

#get all pearson correlation coefficients for features used
for i in range(12):
    a = np.corrcoef(Matrix[:291, i], deltaVolCalc) #almost no correlation
    print(a[0][1]);
    #All of the variables we have investigated here are very shitty predictors
    #Coordination Number has the highest Pearson correlation...