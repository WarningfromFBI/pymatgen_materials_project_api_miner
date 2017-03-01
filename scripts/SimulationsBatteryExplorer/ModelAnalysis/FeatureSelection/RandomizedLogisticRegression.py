
from sklearn import preprocessing
import numpy as np
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn import svm;
from sklearn.model_selection import train_test_split;
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix

import ModelAnalysis.AutoFitModel.LogisticReg as LR;
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle
from sklearn import linear_model
import MinedDataSets.DataReader.ResponsePredictorValidation as rpv
import LabelMiner.ClassifierCreation.LabelDistributionClassifiers as ldc
import scripts.DataScraping.TrainingSetFiltering.MultiFiltering as mf
import scripts.DataScraping.TrainingSetFiltering.FilteringFunctions as ff
import MinedDataSets.DataReader.CombineFeatureSets as cfs
import settings
import copy
plt.close("all")

vlabels = fle.getLabels('volumeLabels');
[Xall, X_nparr] = fle.getFeatures('UnLayered')
print(Xall.shape)
[X1, X2] = ff.FilterByLithiumFraction(0.25, Frame=Xall)
print(X1.shape)
[X1, X2] = ff.filterByInitialLithium(Frame=X1)
#[X1, X2] = ff.FilterByPreservedCrystalSys(Frame=X1)
[X, vlabels] = rpv.compareFeatureSets(X1, vlabels);
X_scaled = preprocessing.scale(X);

##DATA Summary
print('feature shape: '+str(X.shape))
clf = linear_model.LogisticRegression();

print(X.shape)
Xcopy = pd.DataFrame(); #this remains empty
goodLabels = ['dVweight', 'dVdensity', 'dVperAtom', 'dvnormweight', 'dvnormweight2', 'VolRatio']
goodEnergyLabels = ['volCap3', 'avgVolt2'];
Xcopy2 = pd.DataFrame();
for response in (vlabels.keys()):
    Xcopy2 = copy.copy(X);
    if(response not in goodLabels):
        continue;
    y = vlabels[response]
    print(response)
    # PYTHON'S STABILITY SELECTION
    yclass = ldc.createBinaryClassifierbyMean(y);
    if(len(set(list(yclass))) <2):
        continue;
    gdf = linear_model.RandomizedLogisticRegression();
    gdf.fit(X, yclass);

    print(sorted(zip(map(lambda x: round(x, 4), gdf.scores_),Xall.columns), reverse=True))

    Xstable = gdf.fit_transform(X, yclass);
    LR.runLogReg(Xstable, yclass)

    #write individual optimal featuresets for every volume label:
    dropindices2 = list();
    for i in range(len(gdf.scores_)):
        if (gdf.scores_[i] < 0.1):
            dropindices2.append(i)
    Xcopy2.drop(X.columns[dropindices2], axis = 1);
    Xcopy2.to_csv(settings.DynamicFeatureSets+'\\FeatureSelectionSets\\RandomizedLogReg\\Features_'+response+'.csv')

    dropindices = list();
    for i in range(len(gdf.scores_)):
        if(gdf.scores_[i] > 0.3):
            if(X.columns[i] in Xcopy.columns):
                continue;
            Xcopy[X.columns[i]] = X[X.columns[i]]
            print(Xcopy.shape)
Xcopy.to_csv(settings.DynamicFeatureSets+'\\FeatureSelectionSets\\RandomizedLogRegFeatureSelection.csv')