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

file2 = os.path.join(directory, 'mp_structural_features.csv');
data2 = pd.read_csv(file2, index_col = 0);
print(data2.shape)

#get intersection of features with data features
print(len(list(set(data1.index) & set(data2.index))))
retained_indices = list(set(data1.index) & set(data2.index));

#convert index to a column
data1.reset_index(level=0, inplace=True)
# data2.reset_index(level=0, inplace=True)
# print(data1.columns)
# ## concatenate the two dataframes, dropping anything that doesn't match
# materials_project = pd.merge(data1, data2, on='index', how='inner')
# materials_project.set_index('index', inplace = True);
# materials_project.dropna(axis=0, how='any', inplace = True)
# print(materials_project.shape)
#
# materials_project.to_csv(os.path.join(settings.ROOT_DIR, 'data_dump','materials_project.csv'));
all_features = list(data1.columns);
materials_project = data1;
for file in os.listdir(directory):
    if('mp' not in file or file == 'mp_MatData_features.csv' or \
                   file == 'mp_shannon_features.csv' or file == 'mp_atomistic_features.csv'):
        print(file)
        continue;
    data = pd.read_csv(os.path.join(directory, file), index_col = 0)
    if(len(data.columns) > 2000):
        data = data.T;
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