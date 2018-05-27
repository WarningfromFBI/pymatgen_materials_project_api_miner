'''
new function which attempts to do a smarter version of executing
the feature minder functions

assumes the function outputs a smart piece of data, a dictionary
'''

from feature_miner_functions import SpecialFeatures
from feature_miner_functions import FINAL_PAPER_FEATURES
from feature_miner_functions import Bond_Order_Features
#important that every feature accepts a picklestruct


import os;
import pickle
import inspect
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import *

import settings
from database_reader_functions import battery_base_reader as bbr
from database_reader_functions import materials_project_reader as mbf;
from feature_miner_functions import ShannonFeatures as BSF;

'''
this is a special function which can read any of the feature miner scripts
and execute all the functions and put it into a dataframe

the only requirements is that all the functions must accept a picklestruct
and output everything as a DICTIONARY (which is more efficient anyways)
'''
#this is the shannon feature miner for specific pairing with the pymatgen ionvalence analyzer...Problem is that not all
#compounds have known valences, which makes computation here problematic to say the last...

plt.close("all")

directory = os.path.join(settings.ROOT_DIR,'Materials_Project_Database');
structureDir = os.path.join(settings.basedirectory, 'structure_database');

#THIS BECOMES VERY SLOW WHEN WE USE PYMATGEN's IONIC VALENCE CALCULATOR
dump_name = os.path.join(settings.ROOT_DIR, 'data_dump', 'mp_new_structure_features.csv');
if(not os.path.isfile(dump_name) or os.stat(dump_name).st_size == 0):
    print('starting')
    datframe = pd.DataFrame();
else:
    print('loading existing')
    datframe = pd.read_csv(dump_name, index_col = 0);

testcounter = 0; datframerows = list(); structureMatrix = list();
materialMatrix = list();
errors = 0;
for filename in os.listdir(directory):

    print('file no. ' + str(testcounter))
    testcounter+=1;
    #if(testcounter>2): break;

    #print(data)
    mpid = filename.strip('.txt')
    try:

        [matdata, s] = mbf.readCompound(filename)
        ID = matdata['pretty_formula'] + ', ' + matdata['material_id'];
        #print(ID)
        if(ID in datframe.index):
            print('ALREADY PROCESSED')
            continue;
        structureClassUnLith = pickle.load(open(structureDir + '\\' + mpid + '.p', 'rb'));
        picklestruct = structureClassUnLith
        ##================STRUCTURAL FEATURE EXTRACTION===============================#

        all_functions = inspect.getmembers(FINAL_PAPER_FEATURES, inspect.isfunction)
        for key, value in all_functions:
            if str(inspect.signature(value)) == "(picklestruct)":
                data = value(picklestruct)
                #print(data)
                #iterate through keys of data
                for key in data:
                    datframe.set_value(ID, key, data[key])
        #print(datframe)
        if(testcounter%1000 == 0):
            print(datframe.shape);
            print('errors: '+str(errors))
    except Exception as e:
        #dump the file so we don't lose any progress we made during the mining process
        datframe.to_csv(dump_name)
        #print(inspect.signature(value))

        errors+=1;
        print(e)

print('ERRORS ENCOUNTERED: '+str(errors))
datframe.to_csv(dump_name)