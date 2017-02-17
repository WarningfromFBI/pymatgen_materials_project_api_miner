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

elementList = ['O', 'Ti', 'Ge', 'P', 'O', 'V', 'Fe', 'S', 'Bi', 'Nb', 'Zr', 'Ta', 'Al', 'H'];

def nchoosec(elementList, N):
    combos = list();
    firstElem = 'Li';
    for j in range(len(elementList)):
        secondElem = elementList[j];
        for k in range(j+1, len(elementList)):
            thirdElem = elementList[k];
            combos.append([firstElem, secondElem, thirdElem]);
    return combos

MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);

ternaries = nchoosec(elementList, 3);
volumes = list(); avgAtNum = list();
maxinteratDist = list(); numSites = list();

density = list();

counter = 0;
#access battery data:
for comp in ternaries:
    query = comp[0] + "-" + comp[1] + "-" + comp[2];
    battery = mpr.get_battery_data = get_battery_data(query);
    for i in battery:
        print(i);

for comp in ternaries:
    query = comp[0]+"-"+comp[1]+"-"+comp[2];
    generalData = mpr.get_data(query);
    for i in generalData:
        density.append(i['density'])

for comp in ternaries:
    query = comp[0]+"-"+comp[1]+"-"+comp[2];
    structures = mpr.get_structures(query)
    generalData = mpr.get_data(query);
    #print(structures)
    for i in structures:
        volumes.append(i.lattice.volume)
        avgAtNum.append(np.mean(i.atomic_numbers))
        maxinteratDist.append(np.max(i.distance_matrix));
        numSites.append(i.num_sites)
        if(counter%10 == 0):
            print(counter)
    counter+=1

#plotting
plt.scatter(maxinteratDist, volumes)

QUERY = "Li-Co-O"
structures = mpr.get_structures(QUERY);