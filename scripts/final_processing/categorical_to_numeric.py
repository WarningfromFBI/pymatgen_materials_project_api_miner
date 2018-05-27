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
le = preprocessing.LabelEncoder()
directory = os.path.join(settings.ROOT_DIR,'data_dump');

file = os.path.join(directory, 'materials_project.csv');
data = pd.read_csv(file, index_col = 0);
data.dropna(axis = 0, inplace = True)
#drop NaNs by row
print(data.shape)
for col in data.columns:
    ohe = OneHotEncoder();
    if(data[col].dtype == 'object'):
        print(col)
        print(data[col])
    if(col == 'crystal_system'): # check what
        column = data['crystal_system'];
        revised = le.fit_transform(column.values);
        print(le.classes_)
        revised = np.expand_dims(revised, axis = 1);
        ohe_values = ohe.fit_transform(revised)
        print(ohe_values.shape)

        ohe_frame = pd.DataFrame(ohe_values.todense(), index = data.index, columns = le.classes_)
        data = data.join(ohe_frame);
        data.drop('crystal_system', axis = 1, inplace = True);
        #we should only do one hot encodings for labels with small numbers of distinct labels
        # if(len(set(a)) < 10):
        #     ohe = OneHotEncoder();
        #     b = np.expand_dims(a, axis = 1).shape;
        #     print(ohe.fit_transform(b).shape)
data.to_csv(os.path.join(settings.ROOT_DIR,'data_dump', 'materials_project.csv'));