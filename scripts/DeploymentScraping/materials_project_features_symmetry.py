import os;

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import *

from database_reader_functions.AddMPIDToManifest import *
import database_reader_functions.structure_reader as sbr;
import settings
from database_reader_functions import battery_base_reader as bbr
from database_reader_functions import materials_project_reader as mbf;
from feature_miner_functions import SymmetryFeatures as BsymF
import sys
import pickle
'''
SLOWEST FEATURES TO MINE
'''

plt.close("all")

directory = os.path.join(settings.ROOT_DIR,'Materials_Project_Database');
structureDir = os.path.join(settings.ROOT_DIR, 'structure_database');
dump_name = os.path.join(settings.ROOT_DIR, 'data_dump', 'mp_symmetry_features.csv');
if(not os.path.isfile(dump_name) or os.stat(dump_name).st_size == 0):
    datframe = pd.DataFrame();
else:
    datframe = pd.read_csv(dump_name, index_col = 0);
testcounter = 0; datframerows = list(); symmetryMatrix = list();

for filename in os.listdir(directory):
    testcounter+=1;

    print('file no. ' + str(testcounter))

    mpid = filename.strip('.txt')
    try:

        [matdata, structuredata] = mbf.readCompound(filename)
        ID = matdata['pretty_formula'] + ', ' + matdata['material_id'];
        if(ID in datframe.columns):
            print('ALREADY PROCESSED')
            continue;
        structureClassUnLith = pickle.load(open(structureDir+'\\'+mpid+'.p', 'rb'));

        ##================SYMMETRY DATA================================#
        [symmetrydata, symmetryLabels] = BsymF.GetAllSymmetries(structureClassUnLith);
        print(symmetrydata)
        symmetryMatrix.append(symmetrydata);
        datframerows.append(matdata['pretty_formula'] + ', ' + matdata['material_id']);
        datframe.set_index = symmetryLabels;
        datframe.index = symmetryLabels;
        datframe[ID] = symmetrydata;
        datframe.to_csv(dump_name)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()

        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        print(exc_type, fname, exc_tb.tb_lineno)




labels = symmetryLabels;
# print(labels);
print(len(labels))
names = labels;

symmetryMatrix = np.array(symmetryMatrix);

TotalData = symmetryMatrix
# Create separate csv files for the structures and for the atomistic

# atomisticMatrix = np.concatenate((atomisticMatrix,np.array(v2).reshape((len(v2),4))), axis = 1)
# BANDGAP IS AN EXCELLENT PREDICTOR!!!!!!!!!!!!!

print('data shape:' + str(TotalData.shape));
print('length of labels: ' + str(len(labels)));

# datframe = pd.DataFrame(TotalData, columns=labels, index=datframerows);
# datframe.to_csv(os.path.join(settings.ROOT_DIR, 'data_dump', 'mp_symmetry_features.csv'));

