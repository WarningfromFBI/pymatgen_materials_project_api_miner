import os;
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import *

import settings
from database_reader_functions import battery_base_reader as bbr
from database_reader_functions import materials_project_reader as mbf;
from feature_miner_functions import ShannonFeatures as BSF;

'''
Because these computations are slow, we generate the final dataframe and write each entry elementwise into it
'''
#this is the shannon feature miner for specific pairing with the pymatgen ionvalence analyzer...Problem is that not all
#compounds have known valences, which makes computation here problematic to say the last...

plt.close("all")

directory = os.path.join(settings.ROOT_DIR,'Materials_Project_Database');
structureDir = os.path.join(settings.basedirectory, 'structure_database');

#THIS BECOMES VERY SLOW WHEN WE USE PYMATGEN's IONIC VALENCE CALCULATOR
dump_name = os.path.join(settings.ROOT_DIR, 'data_dump', 'mp_shannon_features.csv');
if(not os.path.isfile(dump_name) or os.stat(dump_name).st_size == 0):
    datframe = pd.DataFrame();
else:
    datframe = pd.read_csv(dump_name, index_col = 0);

testcounter = 0; datframerows = list(); structureMatrix = list();
materialMatrix = list();
for filename in os.listdir(directory):

    print('file no. ' + str(testcounter))
    testcounter+=1;
    if(testcounter>2): break;

    #print(data)
    mpid = filename.strip('.txt')
    try:
        [matdata, s] = mbf.readCompound(filename)
        ID = matdata['pretty_formula'] + ', ' + matdata['material_id'];
        if(ID in datframe.columns):
            print('ALREADY PROCESSED')
            continue;
        structureClassUnLith = pickle.load(open(structureDir + '\\' + mpid + '.p', 'rb'));
        ##================STRUCTURAL FEATURE EXTRACTION===============================#

        [structuredata, structureLabels] = BSF.GetAllShannonFeatures(structureClassUnLith);
        structureMatrix.append(structuredata)

        datframerows.append(matdata['pretty_formula'] + ', ' + matdata['material_id']);
        datframe.set_index = structureLabels;
        datframe.index = structureLabels;
        datframe[ID] = structuredata;
        datframe.to_csv(dump_name)

    except Exception as e:
        print(e)
        #raise #use raise when you want to explicitly track an error to its base line in the code

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

# datframe = pd.DataFrame(TotalData, columns=labels, index=datframerows);
# datframe.to_csv(os.path.join(settings.ROOT_DIR, 'data_dump', 'mp_shannon_features.csv'));
# scatter_matrix(datframe)

################################### SOME BASIC ANALYSES ##############################################################
# print(datframe)

##Perform data validation

