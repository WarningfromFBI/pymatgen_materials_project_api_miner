import os;
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import *

from database_reader_functions.AddMPIDToManifest import *
import settings
from database_reader_functions import battery_base_reader as bbr
from database_reader_functions import materials_project_reader as mbf;
from feature_miner_functions import WolvertonAtomisticFeatures as waf;
import sys

plt.close("all")

'''
atomistic_type features, from the seminal Wolverton Paper
'''

directory = os.path.join(settings.ROOT_DIR,'Battery_Explorer');
structureDir = os.path.join(settings.ROOT_DIR, 'structure_database');



testcounter = 0; datframerows = list(); atomisticMatrix = list(); weightedAtom = list()

for filename in os.listdir(directory):
    testcounter+=1;
    #if(testcounter>2): break;

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
            ##================WolvertonATOM FEATURE EXTRACTION===============================#

            [feat, atomisticLabels] = waf.getReducedSummaryStats(matdata['unit_cell_formula'])
            [feat2, weightedlabel] = waf.getWeightedStats(matdata['unit_cell_formula']);
            atomisticMatrix.append(feat);
            weightedAtom.append(np.squeeze(feat2))
            datframerows.append( filename.strip('+.txt') + ', ' + matdata['pretty_formula'] + ', ' + matdatalith['pretty_formula']
                + ', ' + matdata['material_id'] + ', ' + matdatalith['material_id'])


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("mpid: " + unlithiatedmpid)
            AddMPIDtoManifest(lithiatedmpid);
            AddMPIDtoManifest(unlithiatedmpid);
            print(exc_type, fname, exc_tb.tb_lineno)
            break;

labels = atomisticLabels + weightedlabel;
# print(labels);
print(len(labels))
names = labels;

atomisticMatrix = np.array(atomisticMatrix);
weightedAtom = np.array(weightedAtom);

TotalData = np.concatenate((atomisticMatrix, weightedAtom), axis = 1);
# Create separate csv files for the structures and for the atomistic

# atomisticMatrix = np.concatenate((atomisticMatrix,np.array(v2).reshape((len(v2),4))), axis = 1)
# BANDGAP IS AN EXCELLENT PREDICTOR!!!!!!!!!!!!!

print('data shape:' + str(TotalData.shape));
print('length of labels: ' + str(len(labels)));

datframe = pd.DataFrame(TotalData, columns=labels, index=datframerows);
weightedframe = pd.DataFrame(weightedAtom, columns = weightedlabel, index = datframerows)
import os;
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import *

from database_reader_functions.AddMPIDToManifest import *
import settings
from database_reader_functions import battery_base_reader as bbr
from database_reader_functions import materials_project_reader as mbf;
from feature_miner_functions import BatteryStructureFeatures as BSF;

plt.close("all")

directory = os.path.join(settings.ROOT_DIR,'Battery_Explorer');
structureDir = os.path.join(settings.ROOT_DIR, 'structure_database');


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

            [structuredata, structureLabels] = BSF.GetAllStructureFeatures(structuredata, structureClassUnLith);
            structureMatrix.append(structuredata)
            datframerows.append(filename.strip('+.txt') + ', ' + matdata['pretty_formula'] + ', ' + matdatalith['pretty_formula']
                                + ', ' + matdata['material_id'] + ', ' + matdatalith['material_id'])


        except Exception as e:
                print(e)
                #raise #use raise when you want to explicitly track an error to its base line in the code
                print("mpid: " + unlithiatedmpid+'\n')
                AddMPIDtoManifest(lithiatedmpid);
                AddMPIDtoManifest(unlithiatedmpid);
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
datframe.to_csv(os.path.join(settings.ROOT_DIR, 'data_dump', 'atomistic_features.csv'));
# scatter_matrix(datframe)
# weightedframe.to_csv(settings.DynamicFeatureSets + '\\FeatureSets\WeightedAtomisticFeatures.csv')
# # scatter_matrix(datframe)

