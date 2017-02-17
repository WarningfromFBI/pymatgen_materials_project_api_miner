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
import json
import sys
from sklearn import preprocessing


## ATTEMPTING TO GENERATE VIABLE BATTERY COMPOUNDS USING JUST THE LIST OF LITHIUM CONTAINING MATERIALS
## EXTRACTED INTO THE LITHIUM BATTERY KEYS
plt.close("all")
currentdir = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataStructureExtractors\LithiumBatteryKeys\\';
megabase = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataStructureExtractors\MegaBase'
counter = 0;

MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);

f = open(currentdir+'PotentialLiBattCompoundsII.txt');
#compound, lithiated, unlithiated
def getDat(file):
    d1 = ""; d2 = "";
    counter = 0;
    for line in file:
        if (counter == 0):  # BASE MATERIAL DATA
            d1 = json.loads(line);
        if (counter == 1):  # STRUCTURE
            d2 = json.loads(line);

        counter+=1
    return [d1, d2];


deltaVols = list(); atomisticMatrix = list();
for line in f:
    data = line.rstrip().split(', ');
    #print(data);
    lithiated = data[1];
    unlithiated = data[2];
    if('Si' in unlithiated):
        print(lithiated)
    search1 = megabase+'\\'+lithiated+'.txt';
    search2 = megabase+'\\'+unlithiated+'.txt';
    print(search1 +', '+search2);
    try:
        dat1 = open(search1, 'r');
        dat2 = open(search2, 'r');
        DataLith = getDat(dat1); DataUnlith = getDat(dat2);
        unitcelldictLith = DataLith[0]['unit_cell_formula']
        unitcelldictUnlith = DataUnlith[0]['unit_cell_formula']
        [features, label] = waf.getAllSummaryStats(unitcelldictUnlith);
        deltaVol = (DataLith[0]['volume']-DataUnlith[0]['volume'])/DataUnlith[0]['volume'];
        deltaVols.append(deltaVol);
        atomisticMatrix.append(features);
        #check if the lithiated version is in the batterydatabase
        counter+=1;
    except Exception as e:
        print(e)
        #mine the compound into the megabase: where the code for that?
        continue

atomisticMatrix = np.array(atomisticMatrix);
classifiers = list()
for i in range(len(deltaVols)):
    if(deltaVols[i] > np.mean(deltaVols)):
        classifiers.append(1);
    else:
        classifiers.append(0)

X = atomisticMatrix;
X_scaled = preprocessing.scale(X)


pca = PCA(n_components = 2);
ans = pca.fit(X_scaled[:,:-1]);
Projection = pca.fit_transform(X_scaled[:,:-1])
plt.figure()
plt.scatter(Projection[:,0], Projection[:,1], s = 400, c = classifiers, cmap = 'viridis')
pca3d = PCA(n_components = 3)
ans2 = pca3d.fit(X_scaled);
Projection3D = pca3d.fit_transform(X_scaled);
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(Projection3D[:,0], Projection3D[:,1], Projection3D[:,2], s = 400, c =classifiers, cmap = 'viridis')

plt.figure()
font = {'fontname':'Arial', 'size':'50'}
plt.hist(deltaVols, 100)
plt.xlabel('% expansion per unit cell/# formula units per cell',**font )
plt.ylabel('counts', **font)
plt.title('Histogram of Battery Expansion Data from Materials Explorer', **font)
plt.xticks(fontsize = 40);
plt.yticks(fontsize = 40);
plt.show()