import os;
import pickle
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import *

import APIMining.MaterialsAPIMiner.AddMPIDToManifest as manifest
import settings
from FeatureMiner import BatteryMatDataFeatures as BAF;
from FeatureMiner import BatteryShannonFeatures as BSF;
from FeatureMiner import WolvertonAtomisticFeatures as waf;
from MaterialsProjectReader import BatteryBaseReader as bbr
from MaterialsProjectReader import MegaBaseReader as mbf;
from FeatureMiner import BatterySymmetryFeatures as BsymF

#this is the shannon feature miner for specific pairing with the pymatgen ionvalence analyzer...Problem is that not all
#compounds have known valences, which makes computation here problematic to say the last...

plt.close("all")

directory = settings.basedirectory + '\\MaterialsProject\LithiumBatteryExplorer';
structureDir = settings.MaterialsProject+'\\StructureBase'

#THIS BECOMES VERY SLOW WHEN WE USE PYMATGEN's IONIC VALENCE CALCULATOR

testcounter = 0; datframerows = list(); structureMatrix = list();
materialMatrix = list();
for filename in os.listdir(directory):
    testcounter+=1;
    #if(testcounter>5): break;

    print('file no. ' + str(testcounter))
    batterydata = bbr.readBattery(filename);
    #print(data)

    for i in range(len(batterydata['adj_pairs'])):
        dischargeState = batterydata['adj_pairs'][i];

        if(batterydata['adj_pairs'][i]['max_delta_volume'] == 0):
            print(batterydata['battid']);
            continue;

        unlithiatedmpid = batterydata['adj_pairs'][i]['id_charge'];
        lithiatedmpid = batterydata['adj_pairs'][i]['id_discharge']
        mpfile = unlithiatedmpid+'.txt'; mpfile2 = lithiatedmpid+'.txt';

        try:
            [matdata, structuredata] = mbf.readCompound(mpfile)
            [matdatalith, structuredatalith] = mbf.readCompound(mpfile2)
            structureClassUnLith = pickle.load(open(structureDir+'\\'+unlithiatedmpid+'.p', 'rb'));
            ##================STRUCTURAL FEATURE EXTRACTION===============================#

            [structuredata, structureLabels] = BSF.GetAllShannonFeatures(structureClassUnLith);
            structureMatrix.append(structuredata)
            datframerows.append(filename.strip('+.txt') + ', ' + matdata['pretty_formula'] + ', ' + matdatalith['pretty_formula']
                                + ', ' + matdata['material_id'] + ', ' + matdatalith['material_id'])


        except Exception as e:
            print(e)
            raise #use raise when you want to explicitly track an error to its base line in the code
            print("mpid: " + unlithiatedmpid+'\n')
            manifest.AddMPIDtoManifest(lithiatedmpid);
            manifest.AddMPIDtoManifest(unlithiatedmpid);
            #break;

labels = structureLabels;
# print(labels);
print(len(labels))
names = labels;

structureMatrix = np.array(structureMatrix);

TotalData = structureMatrix
# Create separate csv files for the structures and for the atomistic

# atomisticMatrix = np.concatenate((atomisticMatrix,np.array(v2).reshape((len(v2),4))), axis = 1)
# BANDGAP IS AN EXCELLENT PREDICTOR!!!!!!!!!!!!!

print('data shape:' + str(TotalData.shape));
print('length of labels: ' + str(len(labels)));

datframe = pd.DataFrame(TotalData, columns=labels, index=datframerows);
datframe.to_csv(settings.DynamicFeatureSets + '\\FeatureSets\ShannonFeaturesOnly.csv');
# scatter_matrix(datframe)

################################### SOME BASIC ANALYSES ##############################################################
# print(datframe)

##Perform data validation

