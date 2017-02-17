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
plt.close("all")
f = open('D:\\Nathan\Documents\StanfordYearOne\Reed Group\MachineLearningPractice\Datasets\PeriodicTable.txt', 'r')
array = list();
for line in f:
    x = line.rstrip();
    x = line.split('\t');
    print(x)

    print(featureVec)
    array.append(x[1]);
    array.append(x[3].rstrip());
si = mg.Element("Si");

comp = mg.Composition("Fe2O3");
LiMCO2 = mg.Composition("LiCoO2")

ionicRad = list(); features = list();

group = list(); #categorical
atomicWeights = list();
for i in array:
    elem = mg.Element(i);
    ionicRad.append(elem.average_ionic_radius);
    atomicWeights.append(elem.number);
    featureVec = np.zeros(3);

    if (elem.is_metalloid == True):
        featureVec[0] = 1
    elif (elem.is_noble_gas == True):
        featureVec[1] = 1
    elif (elem.is_alkali == True):
        featureVec[2] = 1;

    features.append(featureVec);

plt.figure()
plt.plot(ionicRad, atomicWeights, '.')

#using mprester
MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);
QUERY = "Li-Co-O"
structures = mpr.get_structures(QUERY);
volumes = list();
avgAtNum = list();
for s in structures:
    print(s)
    volumes.append(s.lattice.volume);
    avgAtNum.append(np.mean(s.atomic_numbers))
plt.figure();
plt.plot(volumes)
plt.figure();
plt.scatter(volumes, avgAtNum);
#plot a bandstructure
# my_bs = mpr.get_bandstructure_by_material_id(MP_ID);
# BSPlotter(my_bs).show(); #this is a time consuming operation

entries = mpr.get_entries_in_chemsys(['Li','Co','O'])
for i in entries:
    print(i)

#Access battery data
def get_battery_data(formula_or_batt_id):
    """Returns batteries from a batt id or formula.

    Examples:
        get_battery("mp-300585433")
        get_battery("LiFePO4")
    """
    return mpr._make_request('/battery/%s' % formula_or_batt_id)

results = mpr.get_battery_data = get_battery_data("LiFePO4")
results2 = mpr.get_battery_data = get_battery_data("LiCoO2")
compoundList = ['']
#extract all max_delta_volume data
deltaVol = list();
for item in results:
    deltaVol.append(item['adj_pairs'][0]['max_delta_volume'])
for item in results2:
    deltaVol.append(item['adj_pairs'][0]['max_delta_volume'])
plt.figure()
plt.plot(deltaVol, '.')

url = 'https://www.materialsproject.org/rest/v1/materials/mp-24972/vasp/?API_KEY=kT08xPXKwuvhfBdb';
url = 'https://www.materialsproject.org/rest/v1/battery/mp-24972/?API_KEY=kT08xPXKwuvhfBdb';

response = requests.get(url)

f = open('D:\\Nathan\Documents\StanfordYearOne\Reed Group\MachineLearningPractice\Datasets\LiFePO4.txt', 'w')
for item in results:
    for elem in item:
        f.write(item[elem]);
        f.write('\n')

f.close()



























