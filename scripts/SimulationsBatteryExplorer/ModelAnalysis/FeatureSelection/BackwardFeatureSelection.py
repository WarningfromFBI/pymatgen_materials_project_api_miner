import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle
from sklearn import linear_model
from sklearn.model_selection import train_test_split;
import LabelMiner.ClassifierCreation.LabelDistributionClassifiers as ldc
import pandas as pd;
import numpy as np
import matplotlib.pyplot as plt
import MinedDataSets.DataReader.ResponsePredictorValidation as rpv
from sklearn.model_selection import cross_val_score
import scripts.DataScraping.TrainingSetFiltering.FilteringFunctions as ff
import settings
import copy
## forward feature selection

vlabels = fle.getLabels('volumeLabels');

[Xall, X_nparr] = fle.getFeatures('UnLayered')
#[Xall, X_nparr] = fle.getFeaturesII(settings.FeatureSets + '\\StoredDataSets\\FeatureSelectionSets\\ForwardFeatureSelection.csv')
[Xall, X_nparr] = fle.getFeaturesII(settings.FeatureSets + '\\StoredDataSets\\FeatureSelectionSets\\RandomizedLogRegFeatureSelection.csv')
#[Xall, X_nparr] = fle.getFeaturesII(settings.MinedFeatureSets + '\\FeatureSelectionSets\\RandomLogRegFeatures\\Features_VolRatio.csv')

[X1, X2] = ff.FilterByLithiumFraction(0.25, Frame=Xall)
print(X1.shape)
[X1, X2] = ff.filterByInitialLithium(Frame=X1)
#[X1, X2] = ff.FilterByPreservedCrystalSys(Frame=X1)
[X, vlabels] = rpv.compareFeatureSets(X1, vlabels);

#[X1, X2] = ff.FilterByPreservedCrystalSys(Frame=X1)
[X, vlabels] = rpv.compareFeatureSets(Xall, vlabels);

y = vlabels['VolRatio'];
yclass = ldc.createBinaryClassifierbyMean(y);

errors = list()
featuresMatrix = X; bestFeatures = copy.copy(featuresMatrix);
dataShape= X.shape; globalmax = 0;
for i in range(dataShape[1]):
    if(featuresMatrix.shape[1] == 1):
        break;
    print('Feature: '+str(i))
    #pick the best set of features in X
    scoreDict = dict();
    clf = linear_model.LogisticRegression();
    for feature in featuresMatrix:
        storedFeat = featuresMatrix[feature];
        featuresMatrix.drop(feature, 1, inplace = True)
        data = featuresMatrix.values;
        X_train, X_test, y_train, y_test = train_test_split(data, np.squeeze(yclass), test_size=0.33)
        clf.fit(X_train, y_train)
        correct = np.mean(cross_val_score(clf, data, np.squeeze(yclass), cv = 20))
        misclass = 1-correct;
        #print(correct)
        #print(misclass)
        scoreDict[feature] = correct;
        featuresMatrix = pd.concat([featuresMatrix, storedFeat], axis=1)
    print(featuresMatrix.shape)
    #now select the best feature
    maxSeen = 0; maxLabel = "";
    for feat in scoreDict:
        if(scoreDict[feat] > maxSeen):
            maxSeen = scoreDict[feat];
            maxLabel = feat;

    errors.append(maxSeen);
    print('label dropped: '+maxLabel)
    featuresMatrix.drop(maxLabel, 1, inplace = True)
    if (maxSeen > globalmax):
        globalmax = maxSeen
        bestFeatures.drop(maxLabel, 1, inplace = True)
    #XDataFrame.drop(maxLabel,1, inplace = True)
    #print(featuresMatrix)
    print(maxSeen)
    if(i%5 == 0 and i > 1):
        plt.plot(errors);
        plt.draw()
        plt.show(block = False)

    #del XDataFrame[maxLabel]
#check how good this optimal model is

f2 = linear_model.LogisticRegression();
X_train, X_test, y_train, y_test = train_test_split(featuresMatrix, yclass, test_size=0.33)
f2.fit(X_train, y_train);
print(f2.score(X_test,y_test))
print(errors)
print('\n')
scores = cross_val_score(f2, featuresMatrix, yclass, cv = 20)
print(scores)
print(np.mean(scores))
print(errors)
print('\n')

bestFeatures.to_csv(settings.DynamicFeatureSets+'\\FeatureSelectionSets\\BackwardFeatureSelectionBond.csv')


plt.figure();
plt.plot(errors);
plt.show()
