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

def SimulatedAnnealing(X, yclass):
    ## ===============MONTE CARLO METROPOLIS HASTINGS ALGO =========================##
    d = X.shape;
    iterations = 100
    NumberFeatures = 5

    thresh = 0.99;  # this is the probability that a bad feature is kept, basically the temperature;
    featuresMatrix = X.transpose()[0:NumberFeatures];
    featuresMatrix = featuresMatrix.transpose();
    scores = list();
    # every iteration, we switch a feature, if the score improves, keep it, if it doesn't, keep it with some probability

    for i in range(iterations):
        X_train, X_test, y_train, y_test = train_test_split(featuresMatrix, yclass, test_size=0.33)
        clf0 = linear_model.LogisticRegression();
        clf = linear_model.LogisticRegression();
        # generate random index
        colindex = np.random.randint(0, d[1]);
        while (X.columns[colindex] in featuresMatrix.columns):
            colindex = np.random.randint(0, d[1]);
        newData = X[X.columns[colindex]];
        coldata = np.random.randint(0, NumberFeatures);
        clf0.fit(X_train, y_train);
        score0 = np.mean(cross_val_score(clf0, featuresMatrix, np.squeeze(yclass), cv=10))  # score without new feature

        oldFeature = featuresMatrix[featuresMatrix.columns[coldata]];
        featuresMatrix.drop(featuresMatrix.columns[coldata], axis=1, inplace=True)
        featuresMatrix[X.columns[colindex]] = newData;
        # featuresMatrix is different, so we need new test set
        X_train, X_test, y_train, y_test = train_test_split(featuresMatrix, yclass, test_size=0.33)
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)
        # print(confusion_matrix(y_test, preds));
        score2 = np.mean(cross_val_score(clf, featuresMatrix, np.squeeze(yclass), cv=10))
        # score with new feature
        print(str(score2) + ', ' + str(score0))
        print(featuresMatrix.shape)
        if (score2 > score0):
            scores.append(score2)
        else:
            scores.append(score0);
            p = random.random();
            print(p)
            if (p > thresh):
                # retain the new feature; even though it sucked
                continue;
            else:  # get back old feature
                featuresMatrix.drop(X.columns[colindex], axis=1, inplace=True);
                featuresMatrix[oldFeature.name] = oldFeature;
        print(featuresMatrix.shape)

    plt.plot(scores)
    plt.show()
    print(np.max(scores))




