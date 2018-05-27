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
from feature_miner_functions import StructureFeatures as BSF;

plt.close("all")

directory = os.path.join(settings.ROOT_DIR,'Materials_Project_Database');
structureDir = os.path.join(settings.ROOT_DIR, 'structure_database');


testcounter = 0; datframerows = list(); structureMatrix = list();
materialMatrix = list();
for filename in os.listdir(directory):

    print('file no. ' + str(testcounter))
    testcounter+=1;
    #if(testcounter>2): break;

    #print(data)
    mpid = filename.strip('.txt')
    try:
            [matdata, structuredata] = mbf.readCompound(filename)
            structureClassUnLith = pickle.load(open(structureDir+'\\'+mpid+'.p', 'rb'));
            ##================STRUCTURAL FEATURE EXTRACTION===============================#

            [structuredata, structureLabels] = BSF.GetAllStructureFeatures(structuredata, structureClassUnLith);
            structureMatrix.append(structuredata)
            datframerows.append(matdata['pretty_formula'] + ', ' + matdata['material_id']);



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

datframe = pd.DataFrame(TotalData, columns=labels, index=datframerows);
datframe.to_csv(os.path.join(settings.ROOT_DIR, 'data_dump', 'mp_structural_features.csv'));

# scatter_matrix(datframe)