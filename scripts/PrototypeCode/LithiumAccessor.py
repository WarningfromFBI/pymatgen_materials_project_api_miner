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
from sklearn.preprocessing import StandardScaler
from pymatgen.matproj.rest import MPRester
from pymatgen.phasediagram.maker import PhaseDiagram
from pymatgen.electronic_structure.plotter import BSPlotter;
from pymatgen import core
import requests;

def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

f = open('D:\\Nathan\Documents\StanfordYearOne\Reed Group\MachineLearningPractice\Datasets\LithiumBattery.csv', 'r')
lithComp = list();
for line in f:
    data = line.split(",")
    print(data)
    lithComp.append(data[0].strip("\""));
#Access battery data
def get_battery_data(formula_or_batt_id):
    """Returns batteries from a batt id or formula.

    Examples:
        get_battery("mp-300585433")
        get_battery("LiFePO4")
    """
    return mpr._make_request('/battery/%s' % formula_or_batt_id)

MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);
deltaVol = list(); energy = list(); frac = list();
for compound in lithComp:
    if(compound == "Battid"):
        continue;
    results = mpr.get_battery_data = get_battery_data(compound)
    print(compound)
    #print(results)
    deltaVol.append(results[0]['adj_pairs'][0]['max_delta_volume']);
    frac.append(results[0]['max_frac'])

#deltaVol...visualization
plt.hist(deltaVol, 100);
plt.title('Volume Change for Lithium Intercalation Compounds')
plt.xlabel('proportion expansion')
plt.ylabel('counts')

classifiers = list();
for i in range(len(deltaVol)):
    if(deltaVol[i] > 0.07):
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

Dat = list();
CompoundNames = list();
for i in range(len(BatteryMatrix)):
    data = BatteryMatrix[i];
    l2 = list();
    ind = 16;
    l2.append(data[ind][0]['max_instability'])
    l2.append(data[ind][0]['max_voltage'])
    l2.append(data[ind][0]['stability_charge'])
    l2.append(data[ind][0]['average_voltage'])
    l2.append(data[ind][0]['capacity_grav'])
    l2.append(data[ind][0]['capacity_vol'])
    l2.append(data[ind][0]['energy_vol'])
    l2.append(data[ind][0]['min_instability'])
    CompoundNames.append(data[ind][0]['formula_discharge'])

    Dat.append(l2);
Dat = np.array(Dat);

pca = PCA(n_components = 2);
pca.fit(Dat)
transK = pca.fit_transform(Dat);
plt.scatter(transK[:,0], transK[:,1], s = 400, c = classifiers)

Dat2 = list();
elements = list();
for compound in CompoundNames:
    l3 = list();
    print(compound)
    # if(compound.find('(')!=-1):
    #     continue;
    results = mpr.get_data(compound);
    #print(results)
    l3.append(results[0]['volume'])
    l3.append(results[0]['band_gap'])
    l3.append(results[0]['energy'])
    l3.append(results[0]['density'])
    l3.append(results[0]['e_above_hull'])
    elements.append(results[0]['elements']);
    Dat2.append(l3)

Dat2 = np.array(Dat2)
#interesting data point
plt.figure()
plt.scatter(frac, Dat[:,1], s = 500, c = classifiers)

#we need to access data points from the chem-sys databas
#plot all possible combos
for i in range(5):
    for j in range(8):
        title = 'i = '+str(i)+' j= '+str(j);
        plt.figure();
        plt.scatter(Dat2[:,i], Dat[:,j], c = classifiers, s = 200)
        plt.title(title)
        #Notes: Volume vs volumetric capacity looks interesting
BigDat = np.hstack((Dat, Dat2));

#Analyze the elemental composition of the materials dataset
transMetal = list();
nontransMetal = list();
for i in range(len(elements)):
    elems = elements[i];
    check = False;
    for i in elems:
        if(i == 'Li'):
            continue;
        elem = mg.Element(i);
        if(elem.is_transition_metal):
            transMetal.append(elems);
            check = True;
            break;
        if(elem.is_halogen): #large contingent of halogen containing compounds
            print(elems)
    if(check == False):
        nontransMetal.append(elems); #most of these are transition metal oxides

plt.figure()
plt.hist(deltaVol,100)

#let's attempt a very simple logistic regression fit on the data
#Divide Data into training set and test set:

Training = BigDat[:150, :];
Test = BigDat[150:,:]
logreg = linear_model.LogisticRegression();
logreg.fit(Training, classifiers[:150])
pred = logreg.predict(Test);
missclass = pred-classifiers[150:]
print(np.count_nonzero(missclass)/190) # 38% error in the test set with the model of 13 attributes
predTrain = logreg.predict(Training) # 24% error in the training set

#Compare it to an SVM fit on the same data; WORSE
clf = svm.SVC(kernel = 'linear'); #seems to be worse than a simple logistic regression
clf.fit(Training, classifiers[:150])
pred1 = clf.predict(Test)