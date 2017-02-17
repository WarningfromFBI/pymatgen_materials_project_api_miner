
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
import ModelAnalysis.Sampling.TwoClassSampling as tcs;
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
import MinedDataSets.DataReader.ResponsePredictorValidation as rpv
import scripts.DataScraping.TrainingSetFiltering.FilterbyLithiumLevel as fll
from sklearn import svm
import pandas as pd
import random
import ModelAnalysis.PCA as pcavis


if __name__ == '__main__':
    plt.close("all")
    [vlabels, data, X] = fle.getFilteredLabelsFeatures('noLiInitialFeatures', 'noLiInitialLabels')
    vlabels = fle.getLabels('volumeLabels');
    Xsymmetry = fle.getFeatures('StructureFeatures')
    Xstruct = fle.getFeatures('SymmetryFeatures');

    [Xstruct, Xsym] = rpv.compareFeatureSets(Xstruct[0], Xsymmetry[0]);
    [Xsym, symLabels] = rpv.compareFeatureSets(Xsym, vlabels)
    X = np.concatenate((Xsym.values, Xstruct.values), axis=1);
    print('vlabels: '+str(vlabels.shape))
    [ff1, ff2] = fll.filterByInitialLithium('AtomisticFeatures')
    [ff3, ff4] = fll.filterByInitialLithium('StructureFeatures')
    [X2, symLabels] = rpv.compareFeatureSets(ff1, vlabels);
    [X3, X2] = rpv.compareFeatureSets(ff3, X2)
    counter = 0;
    Xfinal = np.concatenate((X2.values,X3.values), axis = 1)
    X_scaled = preprocessing.scale(Xfinal);
    #X_scaled = X
    print('feature shape: '+str(X.shape))
    counter = 0;

    y = symLabels['dVweight'];
    classifiers = list();
    for i in y:
        if(i > np.mean(y)):
            classifiers.append(1)
        else:
            classifiers.append(0)
    yclass = np.array(classifiers).reshape(len(classifiers),1);

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, yclass, test_size=0.33)

    # POTENTIAL MODELS
    clf = linear_model.LogisticRegression()
    svc = svm.SVC(); #rbf is radial basis function, poly = nonlinear
    print('\nneural network')
    ann = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(10,10), random_state=1)
    ann.fit(X_train, y_train)
    pred = ann.predict(X_test);
    print(confusion_matrix(pred, y_test))
    print(ann.score(X_test, y_test))

    print("logistic regression")
    clf.fit(X_train, y_train);
    pred = clf.predict(X_test);
    miscal  = np.count_nonzero(pred.reshape(len(pred),1)-y_test)/len(pred)
    clfscore = clf.score(X_test, y_test);
    print(confusion_matrix(pred, y_test));
    print(clfscore)
    print(np.count_nonzero(y_test)/len(y_test))
    #scores = cross_val_score(clf, X_scaled, classifiers, cv = 5); #y has to be a list
    #print("cross validation: "+str(scores))

    print('\n RandomForest')
    ## PYTHON's RANDOM FOREST
    extc = ExtraTreesClassifier()
    rfc = RandomForestClassifier(n_jobs=4)
    rfc.fit(X_train, y_train);
    preds = rfc.predict(X_test);
    print(confusion_matrix(preds, y_test))
    print(rfc.score(X_test,y_test))
    print(np.count_nonzero(y_test)/len(y_test))
    print('\n')
    # parameters = { 'n_estimators': random.randint(100, 5000), 'max_features' : ['auto', None], 'min_samples_split' : random.randint(2, 6) }
    # sl2 = RandomizedSearchCV(rfc, parameters, n_jobs = -1);
    # sl2.fit(X_train, y_train);
    # print(sl2.score(X_test, y_test));
    #
    extc.fit(X_train, y_train);
    preds = extc.predict(X_test);
    print('extra-random')
    print(confusion_matrix(preds, y_test))
    print(extc.score(X_test,y_test))
    print(np.count_nonzero(y_test)/len(y_test))
    print('\n')

    # if(clfscore >0.74):
    # #     svc = svm.SVC(kernel = 'rbf', class_weight = 'balanced');
    # #     svc.fit(X_train, y_train);
    # #     preds = svc.predict(X_test);
    # #     print('SVM for the unbalanced data')
    # #     print(confusion_matrix(preds, y_test))
    # # svc = svm.SVC(class_weight = 'balanced');
    #     print('\n Support Vector Machine with a Grid Parameter Search')
    #     #C dictates how complex the decision boundary looks, gamma affects how far a single training example reaches to other data points
    #     parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10, 100, 1000],  'gamma': [0.001, 0.0001], 'class_weight': ['balanced']}
    #     svc2 = GridSearchCV(svc, parameters, n_jobs = -1)
    #     svc2.fit(X_train, np.squeeze(y_train))
    #     pred = svc2.predict(X_test);
    #     print(confusion_matrix(pred, y_test));
    #pcavis.PCAReduction(X_scaled, classifiers)
    plt.show()





