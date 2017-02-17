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
import json;
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
from pandas.tools.plotting import scatter_matrix
import matplotlib
from sympy import *
import sys
sys.path.append('D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataStructureExtractors')
import MegaBaseReader as mbr;
#Analyze Some aspects of the voltage discharge curves and the state of lithiation at each step

plt.close("all")

directory2 = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\MaterialsProject\LithiumBatteryBase'; #contains data from BATTERY EXPLORER

materialsdirectory = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\MaterialsProject\MP_data\converted_mpadata';
megabase = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataStructureExtractors\MegaBase'
def AggregatedVolChange(data):
    start = 100;
    for i in data:
        start += start*i;
    aggregatedChange = (start - 100)/100;
    return aggregatedChange;

maxVolChange = list(); phasesPerCycle = list();
for filename in os.listdir(directory2):
    file = open(directory2+"\\"+filename, 'r')
    data = "";
    for line in file:
        data = json.loads(line);

    maxDeltaVol = 0; volList = list();
    phaseList = list();
    for i in range(len(data['adj_pairs'])):
        dischargeStep = data['adj_pairs'][i];
        if(data['adj_pairs'][i]['max_delta_volume'] == 0):
            print(data['battid']);
            continue;
        if(dischargeStep['max_delta_volume']> maxDeltaVol):
            maxDeltaVol = dischargeStep['max_delta_volume'];
        volList.append(dischargeStep['max_delta_volume'])
        #Now we can perform whatever analysis we want
        # now we can extract all the dat
        unlithiatedmpid = dischargeStep['id_charge'];
        lithiatedmpid = dischargeStep['id_discharge'];
        mpfile1 = lithiatedmpid+'.txt'; mpfile2 = unlithiatedmpid+'.txt';
        filepathmega = megabase+'\\'+mpfile2; filepathmega2 = megabase+'\\'+mpfile1;
        try:
            [matdata, structuredata] = mbr.readCompound(filepathmega);
            [matdata1, structuredata2] = mbr.readCompound(filepathmega2)
            phaseList.append(matdata['spacegroup']['crystal_system'])
            phaseList.append(matdata['spacegroup']['crystal_system']) #Some battery discharge cycles do involve phase changes
        except Exception as e:
            print(e)
            continue;

    print(phaseList);
    if (len(phaseList) > 0): phasesPerCycle.append(len(set(phaseList)));
    aggregatedChange = AggregatedVolChange(volList);
    plt.plot(volList);
    maxVolChange.append(aggregatedChange);

plt.figure();
plt.hist(maxVolChange, 100);
plt.figure();
plt.rcParams['font.size'] = 20
plt.hist(phasesPerCycle)
plt.title('Count of Number of Distinct Phases in Li-Battery Cycles')
plt.xlabel('Phases Counted');
plt.ylabel('Counts')







