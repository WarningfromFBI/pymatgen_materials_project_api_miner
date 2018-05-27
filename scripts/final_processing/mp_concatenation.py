import os;
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import *
import settings
from database_reader_functions import battery_base_reader as bbr
import sys

plt.close("all")

feature_list = os.path.join(settings.ROOT_DIR, 'data_dump', 'feature_list.txt');
features = list();
with open(feature_list) as f:
    lines = f.read().splitlines()
features = lines;
print(features)
directory = os.path.join(settings.ROOT_DIR,'data_dump');

file = os.path.join(directory, 'mp_MatData_features.csv');
data1 = pd.read_csv(file, index_col = 0);
print(data1.shape)

#convert index to a column
data1.reset_index(level=0, inplace=True)

all_features = list(data1.columns);
materials_project = data1;

files = ['mp_new_structure_features.csv', 'mp_MatData_features.csv', 'mp_special_features.csv']

for file in os.listdir(directory):
    if(file not in files):
        continue;
    if('mp' not in file or file == 'mp_MatData_features.csv' or \
                   file == 'mp_shannon_features.csv' or file == 'mp_atomistic_features.csv'):
        print(file)
        continue;
    data = pd.read_csv(os.path.join(directory, file), index_col = 0)

    ## check that none of the features are categorical (must all be numeric)

    data.reset_index(level=0, inplace=True)
    materials_project = pd.merge(materials_project, data, on='index', how='inner')
    print(materials_project.shape)
    #print(len(data.columns))
    all_features += list(data.columns);
print(len(all_features))

print(len(list(set(all_features)& set(features))))

#determine which features we missed:
print('missing features')
for i in features:
    if(i not in all_features):
        print(i)
materials_project.set_index('index', inplace = True);
print(materials_project.shape)
materials_project.to_csv(os.path.join(settings.ROOT_DIR, 'data_dump', 'materials_project.csv'))