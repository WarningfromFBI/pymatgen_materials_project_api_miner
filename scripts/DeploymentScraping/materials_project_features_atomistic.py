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

directory = os.path.join(settings.ROOT_DIR,'Materials_Project_Database');
structureDir = os.path.join(settings.ROOT_DIR, 'structure_database');


testcounter = 0; datframerows = list(); atomisticMatrix = list(); weightedAtom = list()

for filename in os.listdir(directory):
    testcounter+=1;
    #if(testcounter>2): break;

    print('file no. ' + str(testcounter))
    #print(data)
    mpid = filename.strip('.txt')
    try:
        [matdata, structuredata] = mbf.readCompound(filename)
        structureClassUnLith = pickle.load(open(structureDir+'\\'+mpid+'.p', 'rb'));
        ##================WolvertonATOM FEATURE EXTRACTION===============================#

        [feat, atomisticLabels] = waf.getReducedSummaryStats(matdata['unit_cell_formula'])
        #[feat2, weightedlabel] = waf.getWeightedStats(matdata['unit_cell_formula']);
        atomisticMatrix.append(feat);
        #weightedAtom.append(np.squeeze(feat2))
        datframerows.append( matdata['pretty_formula'] + ', '  + matdata['material_id'] );

    except Exception as e:
        #raise
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


labels = atomisticLabels
# print(labels);
print(len(labels))
names = labels;

atomisticMatrix = np.array(atomisticMatrix);
weightedAtom = np.array(weightedAtom);

TotalData = atomisticMatrix;
# Create separate csv files for the structures and for the atomistic

print('data shape:' + str(TotalData.shape));
print('length of labels: ' + str(len(labels)));

datframe = pd.DataFrame(TotalData, columns=labels, index=datframerows);
#weightedframe = pd.DataFrame(weightedAtom, columns = weightedlabel, index = datframerows)
datframe.to_csv('mp_atomistic_features.csv')

