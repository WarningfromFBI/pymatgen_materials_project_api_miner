'''
converts categorical features to numeric, relevant to matdata,
which has structural specifications
'''
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
import os
import pandas as pd
import settings
import numpy as np

directory = os.path.join(settings.ROOT_DIR,'data_dump');

file = os.path.join(directory, 'materials_project.csv');
data = pd.read_csv(file, index_col = 0);
data.dropna(axis = 0, inplace = True)
#drop NaNs by row
print(data.shape)
for col in data.columns:
    if(data[col].dtype == 'object'):
        le = preprocessing.LabelEncoder()
        a = le.fit_transform(data[col]);
        print(len(set(a)));
        print(col)
        data[col] = a;

        #we should only do one hot encodings for labels with small numbers of distinct labels
        # if(len(set(a)) < 10):
        #     ohe = OneHotEncoder();
        #     b = np.expand_dims(a, axis = 1).shape;
        #     print(ohe.fit_transform(b).shape)
data.to_csv(os.path.join(settings.ROOT_DIR,'data_dump', 'materials_project.csv'));