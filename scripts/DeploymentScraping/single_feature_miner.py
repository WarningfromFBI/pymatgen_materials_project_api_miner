'''
new function which attempts to do a smarter version of executing
the feature minder functions

assumes the function outputs a smart piece of data, a dictionary
'''

from feature_miner_functions import SpecialFeatures

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
dump_name = os.path.join(settings.ROOT_DIR, 'data_dump', 'mp_special_features.csv');
if(not os.path.isfile(dump_name) or os.stat(dump_name).st_size == 0):
    datframe = pd.DataFrame();
else:
    datframe = pd.read_csv(dump_name, index_col = 0);

testcounter = 0; datframerows = list(); structureMatrix = list();
materialMatrix = list();
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
        if(ID in datframe.columns):
            print('ALREADY PROCESSED')
            continue;
        structureClassUnLith = pickle.load(open(structureDir + '\\' + mpid + '.p', 'rb'));
        picklestruct = structureClassUnLith
        ##================STRUCTURAL FEATURE EXTRACTION===============================#

        all_functions = inspect.getmembers(SpecialFeatures, inspect.isfunction)
        for key, value in all_functions:
            if str(inspect.signature(value)) == "(picklestruct)":
                data = value(picklestruct)
                #iterate through keys of data
                for key in data:
                    datframe.set_value(ID, key, data[key])
        #print(datframe)
    except Exception as e:
        print(e)

datframe.to_csv(dump_name)