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

lithiumdictionary = "D:\\Nathan\Documents\StanfordYearOne\Reed Group\MaterialsProject\LithiumBatteryCompoundPairs\PotentialLiBattCompoundsII.txt";
MegaBase = "D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataStructureExtractors\MegaBase"

sys.path.append('D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataStructureExtractors');
import MegaBaseReader as mbf;

MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);
def get_battery_data(formula_or_batt_id):
    return mpr._make_request('/battery/%s' % formula_or_batt_id)


f = open(lithiumdictionary, 'r')
counter = 0;
volumeLithFamily = list();
for line in f:
    try:
        unlithvol = list();
        lithvol = list();
        if(counter == 0):
            counter+=1
            continue;
        print(line)
        data = line.rstrip().split(", ");
        lithId = data[1];
        unlithId = data[2];
        #[mat, structure] = mbf.readCompound(MegaBase+'\\'+lithId+'.txt');
        #[mat2, structure2] = mbf.readCompound(MegaBase+'\\'+unlithId+'.txt');
        #do a search of the api to see what compound families exist
        lithiated = mpr.get_data(lithId);
        unlithiated = mpr.get_data(unlithId);
        lithform = lithiated[0]['full_formula'];
        unlithform = unlithiated[0]['full_formula'];
        if(len(unlithiated) == 0):
            continue;

        unlithfamily = mpr.get_data(unlithform);
        lithfamily = mpr.get_data(lithform);
        print(unlithfamily)
        #so we have a set of lithiated and unlithiated compounds...lithium proportion is fixed
        #get max and min volumes
        maxlith = maxunlith = 0; minlith = minunlith = 1e32;
        candidatelithmax = ""; candidateunlithmin = "";
        for i in unlithfamily:
            vol = i['volume']
            if(vol > maxunlith): maxunlith = vol;
            if(vol < minunlith): minunlith = vol; candidateunlithmin = i;
            unlithvol.append(i['volume'])
        for i in lithfamily:
            vol = i['volume']
            if (vol > maxlith): maxlith = vol; candidatelithmax = i;
            if (vol < minlith): minlith = vol;
            lithvol.append(i['volume']);

        volumeDifferenceLith = maxunlith-minunlith;
        lithvol.append(volumeDifferenceLith)
        volumeLithFamily.append([candidateunlithmin, candidatelithmax]);
        counter+=1;
        if(counter > 1500):
            break;
    except Exception as e:
        print(e)
        continue;

plt.figure()
plt.hist(lithvol)
plt.show()

f.close()
#second analysis (#grouping by compounds with same composition of  non-Li elements


