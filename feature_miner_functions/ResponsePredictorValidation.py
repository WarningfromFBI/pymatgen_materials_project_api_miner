
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

def compareFeatureSets(frame1, frame2):
    counter = 0; removeInd1 = list(); matchcounter  =0;
    for ind, row in frame1.iterrows():
        if(ind in frame2.index):
            matchcounter+=1;
        else:
            print(ind)
            removeInd1.append(counter);
        counter+=1;

    counter = 0; removeInd2 = list(); matchcounter  =0;
    for ind, row in frame2.iterrows():
        if(ind in frame1.index):
            matchcounter+=1;
        else:
            print(ind)
            removeInd2.append(counter);
        counter+=1;

    frame1 = frame1.drop(frame1.index[removeInd1])
    frame2 = frame2.drop(frame2.index[removeInd2])
    print('volume labels shape: ' + str(frame1.shape))
    print('feature set shape: ' + str(frame2.shape))
    #drop any pproblematic indices
    inds = pd.isnull(frame1).any(1).nonzero()[0]
    frame1 = frame1.drop(frame1.index[inds])
    frame2 = frame2.drop(frame2.index[inds])

    return [frame1, frame2]


def compareMultiFeatureSets(frameList):
    removeInd1 = list();
    matchcounter = 0;
    referenceFrame = None;  # this is the smallest frame
    smallestLen = float('Inf');
    for dataframe in frameList:
        if (len(dataframe) < smallestLen):
            smallestLen = len(dataframe)
            referenceFrame = dataframe

    TotalFrame = pd.DataFrame();
    frame2 = referenceFrame;
    frameList.remove(frame2);
    for frame1 in frameList:

        counter1 = 0;
        for ind, row in frame1.iterrows():
            if (ind in frame2.index):
                matchcounter += 1;
            else:
                removeInd1.append(counter1);
            counter1 += 1;

        counter2 = 0;
        removeInd2 = list();
        matchcounter = 0;
        for ind, row in frame2.iterrows():
            if (ind in frame1.index):
                matchcounter += 1;
            else:
                removeInd2.append(counter2);
            counter2 += 1;

        frame1 = frame1.drop(frame1.index[removeInd1])
        frame2 = frame2.drop(frame2.index[removeInd2])
        inds = pd.isnull(frame1).any(1).nonzero()[0]
        frame1 = frame1.drop(frame1.index[inds])
        frame2 = frame2.drop(frame2.index[inds])
        TotalFrame = pd.concat([frame1, frame2], axis=1);
        frame2 = TotalFrame;
        print('volume labels shape: ' + str(frame1.shape))
        print('feature set shape: ' + str(frame2.shape))
    return TotalFrame;