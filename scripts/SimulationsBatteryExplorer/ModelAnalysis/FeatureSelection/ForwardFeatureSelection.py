import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle
from sklearn import linear_model
from sklearn.model_selection import train_test_split;
import LabelMiner.ClassifierCreation.LabelDistributionClassifiers as ldc
import pandas as pd;
import numpy as np
import matplotlib.pyplot as plt
import MinedDataSets.DataReader.ResponsePredictorValidation as rpv
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
import settings
import scripts.DataScraping.TrainingSetFiltering.FilteringFunctions as ff
import DataStorage.StoreData as sd
## forward feature selection

vlabels = fle.getLabels('volumeLabels');

[Xall, X_nparr] = fle.getFeatures('AllStructureFeatures')
[Xall, X_nparr] = fle.getFeaturesII(settings.MinedFeatureSets + '\\FeatureSelectionSets\\CompiledLogReg\\RandomizedLogRegFeatureSelectionBig.csv')

print(Xall.shape)
[X1, X2] = ff.FilterByLithiumFraction(0.25, Frame=Xall)
print(X1.shape)
[X1, X2] = ff.filterByInitialLithium(Frame=X1)
#[X1, X2] = ff.FilterByPreservedCrystalSys(Frame=X1)
[X, vlabels] = rpv.compareFeatureSets(X1, vlabels);

y = vlabels['VolRatio'];
yclass = ldc.createBinaryClassifierbyMean(y);
XDataFrame = X;
featuresMatrix = pd.DataFrame();
bestFeatures = pd.DataFrame(); globalMaxScore = 0;
errors = list(); trainScores = list();
for i in range(28):
    print('Features: '+str(i))
    #pick the best set of features in X
    scoreDict = dict(); trainScoreDict = dict();
    clf = linear_model.LogisticRegression();
    for feature in XDataFrame:
        #print(feature)
        #print(XDataFrame[feature])
        featuresMatrix = pd.concat([featuresMatrix, XDataFrame[feature].to_frame()], axis = 1)
        X = featuresMatrix.values;
        X = preprocessing.scale(X);

        X_train, X_test, y_train, y_test = train_test_split(X, yclass, test_size=0.33)
        clf.fit(X_train, y_train)
        trainScore = clf.score(X_train, y_train);
        correct = np.mean(cross_val_score(clf, X, np.squeeze(yclass), cv = 20))#we want to make this as smooth as possible
        misclass = 1-correct;
        scoreDict[feature] = correct; trainScoreDict[feature] = trainScore;
        featuresMatrix.drop(feature, 1, inplace = True)

    #now select the best feature
    maxSeen = 0; maxLabel = ""; maxTrain = 0;
    prevScore = maxSeen
    for feat in scoreDict:
        if(scoreDict[feat] > maxSeen):
            maxSeen = scoreDict[feat]; maxTrain = trainScoreDict[feat];
            maxLabel = feat;
    if(maxSeen > globalMaxScore):
        globalMaxScore = maxSeen;
        bestFeatures = pd.concat([bestFeatures, XDataFrame[maxLabel].to_frame()], axis=1)

    trainScores.append(maxTrain);
    errors.append(maxSeen);
    print(maxLabel)
    featuresMatrix = pd.concat([featuresMatrix, XDataFrame[maxLabel].to_frame()], axis=1)
    XDataFrame.drop(maxLabel,1, inplace = True)
    #print(featuresMatrix)
    print('best score so far: ' + str(maxSeen))
    print('\n')
    if(i%5 == 0 and i > 0):
        plt.figure()
        plt.plot(errors)
        plt.plot(trainScores)
        plt.show(block = False)

    #del XDataFrame[maxLabel]
#check how good this optimal model is
#============================PERSIST DATA============================#
sd.WriteArrayToFile([errors, trainScores], 'ForwardSelectionPlot')

f2 = linear_model.LogisticRegression();
X_train, X_test, y_train, y_test = train_test_split(featuresMatrix, yclass, test_size=0.33)
f2.fit(X_train, y_train);
print(f2.score(X_test,y_test))
scores = cross_val_score(f2, featuresMatrix, yclass, cv = 10)
print(scores)
print(np.mean(scores))
print(errors)
print('\n')

bestFeatures.to_csv(settings.DynamicFeatureSets+'\\FeatureSelectionSets\\ForwardFeatureSelectionAllBondOrder.csv')

plt.figure();
plt.plot(errors);
plt.xlabel('number of features')
plt.ylabel('score')
plt.show()
