
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
import LabelMiner.ClassifierCreation.PhaseChange as pc
if __name__ == '__main__':
    plt.close("all")
    vlabels = fle.getLabels('volumeLabels');
    [Xall, X_nparr] = fle.getFeatures('UnLayered')
    #[Xall, X_nparr] = fle.getFeatures('AllStructureFeatures')

    print(Xall.shape)
    [X1, X2] = ff.FilterByLithiumFraction(0.25, Frame=Xall)
    X1 = Xall
    print(X1.shape)
    [X1, X2] = ff.filterByInitialLithium(Frame=X1)
    #[X1, x] = fle.getFeaturesII(settings.MinedFeatureSets+'\\FeatureSelectionSets\\ForwardFeatureSelectiondVweight.csv')
    #[X2, X1] = ff.FilterByPreservedCrystalSys(Frame=X1) actually, the model predicts phase changing and non-phase changing equally well
    [X, vlabels] = rpv.compareFeatureSets(X1, vlabels);
    X_scaled = preprocessing.scale(X);

    #X_scaled = X
    print('feature shape: '+str(X.shape))
    counter = 0;
    y = vlabels['dVweight'];
    classifiers = list();
    for i in y:
        if(i > np.percentile(y, 50)):
            classifiers.append(1)
        else:
            classifiers.append(0)
    classifiers = pc.PhaseChange(vlabels)
    #classifiers = ldc.createTernaryClassifier(y, 25, 75)
    # classifiers = list();
    # for i in y:
    #     if(i > 0):
    #         classifiers.append(1)
    #     else:
    #         classifiers.append(0)
    yclass = np.array(classifiers)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, yclass, test_size=0.33)

    # POTENTIAL MODELS
    print('\nneural network')
    ann = MLPClassifier(solver='lbfgs', alpha=10, hidden_layer_sizes=(10,1), random_state=1, activation = 'tanh', learning_rate='adaptive')
    ann.fit(X_train, y_train)
    pred = ann.predict(X_test);
    print(confusion_matrix(pred, y_test))
    print(ann.score(X_test, y_test))
    scores = cross_val_score(ann, X_scaled, np.squeeze(yclass), cv = 20)
    print('cross validation: ' + str(np.mean(scores)))

    print("logistic regression")
    clf = linear_model.LogisticRegression(class_weight='balanced')
    clf.fit(X_train, y_train);
    pred = clf.predict(X_test);
    miscal  = np.count_nonzero(pred.reshape(len(pred),1)-y_test)/len(pred)
    clfscore = clf.score(X_test, y_test);
    print(confusion_matrix(pred, y_test));
    print(clfscore)
    print(np.count_nonzero(y_test)/len(y_test))
    scores = cross_val_score(clf, X_scaled, classifiers, cv = 20); #y has to be a list
    print("log reg cross validation: "+str(np.mean(scores)))

    print('\n SVC')
    ## PYTHON's RANDOM FOREST
    svmach = svm.SVC(kernel='rbf', C = 1000, gamma = 0.0001)
    svmach.fit(X_train, y_train);
    preds = svmach.predict(X_test);
    print(confusion_matrix(preds, y_test))
    print(svmach.score(X_test,y_test))
    print(np.count_nonzero(y_test)/len(y_test))
    scores = cross_val_score(svmach, X_scaled, classifiers, cv= 20);  # y has to be a list
    print("random forest cross validation: " + str(np.mean(scores)))
    print('\n')

    print('\n Random Forest')
    ## PYTHON's RANDOM FOREST
    extc = ExtraTreesClassifier()
    rfc = RandomForestClassifier(n_jobs=4)
    rfc.fit(X_train, y_train);
    preds = rfc.predict(X_test);
    print(confusion_matrix(preds, y_test))
    print(rfc.score(X_test,y_test))
    print(np.count_nonzero(y_test)/len(y_test))
    scores = cross_val_score(rfc, X_scaled, classifiers, cv = 20);  # y has to be a list
    print("SVC cross validation: " + str(np.mean(scores)))
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
    scores = cross_val_score(extc, X_scaled, classifiers, cv=10);  # y has to be a list
    print("random forest cross validation: " + str(np.mean(scores)))
    print('\n')


    pcavis.PCAReduction(X_scaled, classifiers)
    plt.show()





