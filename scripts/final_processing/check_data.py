'''

script to check that the data in the mined dataframes are okay
no NaNs, or weird data formats (i.e. arrays where there should be numerics)

'''
import os
import numpy as np
import settings
import pandas as pd
directory = os.path.join(settings.ROOT_DIR,'data_dump');

file = os.path.join(directory, 'materials_project.csv');
data = pd.read_csv(file, index_col = 0);
print('start: '+str(data.shape))
data.dropna(axis = 0, inplace = True)
#drop NaNs by row
print(data.shape)

for col in data.columns:
    if(data[col].dtype == 'object'):
        print(col)