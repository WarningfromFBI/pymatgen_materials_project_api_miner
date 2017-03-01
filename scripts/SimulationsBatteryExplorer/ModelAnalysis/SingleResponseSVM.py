
import numpy as np
from sklearn import linear_model
from sklearn import svm;
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split;
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle;
from sklearn.model_selection import GridSearchCV;
from sklearn.model_selection import RandomizedSearchCV;
import MinedDataSets.DataReader.CombineFeatureSets as cfs
import MinedDataSets.DataReader.ResponsePredictorValidation as rpv
import scripts.DataScraping.TrainingSetFiltering.FilteringFunctions as ff
import scripts.DataScraping.TrainingSetFiltering.MultiFiltering as mf
from sklearn import svm
import pandas as pd
import random
import ModelAnalysis.PCA as pcavis
import settings
if __name__ == '__main__':
    plt.close("all")
    vlabels = fle.getLabels('volumeLabels');

    [Xall, X_nparr] = fle.getFeatures('UnLayered')
    print(Xall.shape)
    [X1, X2] = ff.FilterByLithiumFraction(0.25, Frame = Xall)
    print(X1.shape)
    [X1, X2] = ff.filterByInitialLithium(Frame=X1)
    #[X1, X2] = ff.FilterByPreservedCrystalSys(Frame=X1)
    [X1, x] = fle.getFeaturesII(settings.MinedFeatureSets+'\\FeatureSelectionSets\\ForwardFeatureSelection.csv')
    [X, symLabels] = rpv.compareFeatureSets(X1, vlabels);

    X_scaled = preprocessing.scale(X);
    print('vlabels: '+str(vlabels.shape))
    print('feature shape: '+str(X_scaled.shape))
    print('begin modeling')
    counter = 0;

    y = symLabels['VolRatio'];
    classifiers = list();
    for i in y:
        if(i > np.percentile(y,50)):
            classifiers.append(1)
        else:
            classifiers.append(0)
    yclass = np.array(classifiers).reshape(len(classifiers),1);
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, yclass, test_size=0.33)

    # POTENTIAL MODELS
    svc = svm.SVC(); #rbf is radial basis function, poly = nonlinear
    print('\n Support Vector Machine with a Grid Parameter Search')
    #C dictates how complex the decision boundary looks, gamma affects how far a single training example reaches to other data points
    parameters = {'kernel': ['rbf', 'sigmoid'], 'C':[1, 10, 100, 1000, 10000, 100000, 5*10**5, 10**6],
                  'gamma': [0.1, 0.01,0.001, 0.0001, 0.00001, 0.000001, 1e-7]}
    svc2 = GridSearchCV(svc, parameters, n_jobs = -1)
    svc2.fit(X_train, np.squeeze(y_train))
    pred = svc2.predict(X_test);
    print(confusion_matrix(pred, y_test));

    random_search = RandomizedSearchCV(svc, param_distributions=parameters,
                                       n_iter=10)
    random_search.fit(X_train, np.squeeze(y_train))
    pred = random_search.predict(X_test);
    print(confusion_matrix(pred, y_test));
    # scores = cross_val_score(svc2, X_scaled, np.squeeze(yclass), cv = 5);
    # print(np.mean(scores))
    print(svc2.best_params_);
    results = open(settings.MinedFeatureSets+'\\FeatureSelectionSets\\paramSearch.txt', 'w')
    means = svc2.cv_results_['mean_test_score']
    stds = svc2.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, svc2.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))
        results.write(("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params)));

    print(classification_report(y_test, pred))
    pcavis.PCAReduction(X_scaled, classifiers)
    plt.show()





