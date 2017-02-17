
import numpy as np
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn import svm;
from sklearn.model_selection import train_test_split;
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations
from sklearn import preprocessing
from sympy import *
from sklearn.metrics import confusion_matrix
import ModelAnalysis.Sampling.TwoClassSampling as tcs;
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle;
import settings

[vlabels, Data, X, anisotropylabels] = fle.getLabelsFeatures('AllFeatures');
#select the y data that we are interested in;

data =  X
d = data.shape;
## FILTERING SEGMENT TO GET RID OF SPARSE DATA (mostly 0's)

firstkey = ""; counter = 0;
for i in Data.keys():
    if(counter == 0):
        firstkey = Data[i];
    else:
        if(len(set(Data[i]))<10):
            print(i)
            del Data[i];
    counter+=1;

print('filtering successful')
##Write filtered data to datafile
datadir = settings.MinedFeatureSets +'\\FeatureSets'
Data.to_csv(datadir+'\\FilteredFeatures.csv', index = False)



