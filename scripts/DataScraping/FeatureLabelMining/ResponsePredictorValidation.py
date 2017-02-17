
## script will go through both data files for volume response and predictors to make sure entries
## are consistent, will delete any that are not
# This applies primarily to the main feature and label set ('allfeatures')

from sklearn import preprocessing
import numpy as np
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn.linear_model import Ridge;
from sklearn import svm;
from sklearn.model_selection import train_test_split;
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix
import ModelAnalysis.Sampling.TwoClassSampling as tcs;
import settings
import ModelAnalysis.PCA as pca

plt.close("all")
datadirectory = settings.MinedFeatureSets + '\\FeatureSets';
labeldirectory = settings.MinedFeatureSets + '\\VolumeLabels';
vlabels = pd.read_csv(labeldirectory+'\\volumeLabels.csv', index_col = 0);
#anisotropylabels = pd.read_csv(labeldirectory+'\\anisotropyLabels.csv', index_col = 0);
data = pd.read_csv(datadirectory+'\\AllFeatures.csv', index_col = 0);

counter = 0; removeInd1 = list(); matchcounter  =0;
for ind, row in vlabels.iterrows():
    if(ind in data.index):
        matchcounter+=1;
    else:
        print(ind)
        removeInd1.append(counter);
    counter+=1;

counter = 0; removeInd2 = list(); matchcounter  =0;
for ind, row in data.iterrows():
    if(ind in vlabels.index):
        matchcounter+=1;
    else:
        print(ind)
        removeInd2.append(counter);
    counter+=1;

data = data.drop(data.index[removeInd2])
vlabels = vlabels.drop(vlabels.index[removeInd1])
print('volume labels shape: ' + str(vlabels.shape))
print('feature set shape: ' + str(data.shape))

vlabels.to_csv(labeldirectory+'\\volumeLabels.csv');
data.to_csv(datadirectory+'\\AllFeatures.csv')
#anisotropylabels.to_csv(labeldirectory+'\\anisotropyLabels.csv')
