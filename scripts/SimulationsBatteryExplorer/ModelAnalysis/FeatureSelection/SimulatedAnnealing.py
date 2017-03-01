
import numpy as np
from sklearn import linear_model
from sklearn import svm;
from sklearn.model_selection import train_test_split;
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle;
from sklearn.neural_network import MLPClassifier
import LabelMiner.ClassifierCreation.LabelDistributionClassifiers as ldc
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import svm
import pandas as pd
import random
import ModelAnalysis.PCA as pcavis
import MinedDataSets.DataReader.CombineFeatureSets as cfs
import MinedDataSets.DataReader.ResponsePredictorValidation as rpv
import scripts.DataScraping.TrainingSetFiltering.FilteringFunctions as ff
import scripts.DataScraping.TrainingSetFiltering.MultiFiltering as mf
import settings

plt.close("all")
vlabels = fle.getLabels('volumeLabels');
[Xall, X_nparr] = fle.getFeatures('UnLayered')
#[Xall, X_nparr] = fle.getFeatures('AllStructureFeatures')

print(Xall.shape)
[X1, X2] = ff.FilterByLithiumFraction(0.25, Frame=Xall)
X1 = Xall
print(X1.shape)
[X1, X2] = ff.filterByInitialLithium(Frame=X1)
[X1, x] = fle.getFeaturesII(settings.MinedFeatureSets+'\\FeatureSelectionSets\\CompiledLogReg\\RandomizedLogRegFeatureSelection.csv')
#[X2, X1] = ff.FilterByPreservedCrystalSys(Frame=X1) actually, the model predicts phase changing and non-phase changing equally well
[X, symLabels] = rpv.compareFeatureSets(X1, vlabels);
X_scaled = preprocessing.scale(X);

#X_scaled = X
print('feature shape: '+str(X.shape))
counter = 0;
y = symLabels['dVweight'];
classifiers = list();
for i in y:
    if(i > np.percentile(y, 50)):
        classifiers.append(1)
    else:
        classifiers.append(0)
#classifiers = ldc.createTernaryClassifier(y, 25, 75)
# classifiers = list();
# for i in y:
#     if(i > 0):
#         classifiers.append(1)
#     else:
#         classifiers.append(0)
yclass = np.array(classifiers).reshape(len(classifiers),1);

## ===============MONTE CARLO METROPOLIS HASTINGS ALGO =========================##
d = X.shape;
iterations = 1000
NumberFeatures = 6

thresh = 0.98; #this is the probability that a bad feature is kept, basically the temperature;
featuresMatrix = X.transpose()[0:NumberFeatures];
featuresMatrix = featuresMatrix.transpose();
scores = list();
#every iteration, we switch a feature, if the score improves, keep it, if it doesn't, keep it with some probability
bestFeatures = ""; maxScore = 0;
for i in range(iterations):
    X_train, X_test, y_train, y_test = train_test_split(featuresMatrix, np.squeeze(yclass), test_size=0.33)
    clf0 = linear_model.LogisticRegression();
    clf = linear_model.LogisticRegression();
    #generate random index
    colindex = np.random.randint(0,d[1]);
    while(X.columns[colindex] in featuresMatrix.columns):
        colindex = np.random.randint(0,d[1]);
    newData = X[X.columns[colindex]];
    coldata = np.random.randint(0,NumberFeatures);
    clf0.fit(X_train, y_train);
    score0 = np.mean(cross_val_score(clf0, featuresMatrix, np.squeeze(yclass), cv = 10)) #score without new feature

    oldFeature = featuresMatrix[featuresMatrix.columns[coldata]];
    featuresMatrix.drop(featuresMatrix.columns[coldata], axis = 1, inplace = True)
    featuresMatrix[X.columns[colindex]] = newData;
    #featuresMatrix is different, so we need new test set
    X_train, X_test, y_train, y_test = train_test_split(featuresMatrix, np.squeeze(yclass), test_size=0.33)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    #print(confusion_matrix(y_test, preds));
    score2 = np.mean(cross_val_score(clf, featuresMatrix, np.squeeze(yclass), cv = 10))
    #score with new feature
    #print(str(score2) + ', '+ str(score0))
    #print(featuresMatrix.shape)
    if(score2 > score0):
        scores.append(score2)
    else:
        scores.append(score0);
        p = random.random(); print(p)
        if(p > thresh):
            #retain the new feature; even though it sucked
            continue;
        else: #get back old feature
            featuresMatrix.drop(X.columns[colindex], axis=1, inplace=True);
            featuresMatrix[oldFeature.name] = oldFeature;
    print(featuresMatrix.shape)
    if(score2 > maxScore):
        maxScore = score2;
        bestFeatures = featuresMatrix;

plt.plot(scores)
plt.show()
print(np.max(scores))





