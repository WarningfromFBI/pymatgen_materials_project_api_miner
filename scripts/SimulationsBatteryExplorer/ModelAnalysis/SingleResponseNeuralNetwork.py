
import numpy as np
from sklearn import linear_model
from sklearn.neural_network import MLPClassifier
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
import settings
import ModelAnalysis.PCA as pcavis
import LabelMiner.ClassifierCreation.LabelDistributionClassifiers as ldc
if __name__ == '__main__':
    plt.close("all")
    vlabels = fle.getLabels('volumeLabels');

    [Xall, X_nparr] = fle.getFeatures('UnLayered')
    #[Xall, X_nparr] = fle.getFeatures('UnLayered')

    print(Xall.shape)
    [X1, X2] = ff.FilterByLithiumFraction(0.25, Frame = Xall)
    print(X1.shape)
    [X1, X2] = ff.filterByInitialLithium(Frame=X1)
    [X1, x] = fle.getFeaturesII(settings.MinedFeatureSets+'\\FeatureSelectionSets\\ForwardFeatureSelection.csv')
    #[X1, X2] = ff.FilterByPreservedCrystalSys(Frame=X1)
    #[X2, X1] = ff.FilterByLayer(Frame = X1)
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
    #classifiers =  ldc.createTernaryClassifier(y, bottom = 45, top = 55);
    yclass = np.array(classifiers).reshape(len(classifiers),1);
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, yclass, test_size=0.33)

    # POTENTIAL MODELS
    ann = MLPClassifier(solver=['lbfgs'], alpha=1e-5, hidden_layer_sizes=(40,2), random_state=1)

    #Generate array of tuples
    dualLayer = list();
    for i in range(10,30,5):
        for j in range(1,11,5):
            dualLayer.append((i,j))

    singleLayer = list()
    for i in range(20,100,10):
        singleLayer.append(i)
    #trilayertuple generation

    triLayer = list();
    for i in range(1,15,3):
        for j in range(1,15,3):
            for k in range(1,15, 3):
                triLayer.append((i,j,k))

    print('\n ANN with a Grid Parameter Search')
    #C dictates how complex the decision boundary looks, gamma affects how far a single training example reaches to other data points
    parameters = {'solver': ['lbfgs'], 'alpha': [10, 1, 0.1, 0.01, 0.001], 'hidden_layer_sizes': dualLayer+singleLayer,
                  'activation': ['tanh', 'relu', 'logistic'], 'learning_rate': ['adaptive']}
    ann2 = GridSearchCV(ann, parameters, n_jobs = -1)
    ann2.fit(X_train, np.squeeze(y_train))
    pred = ann2.predict(X_test);
    print(confusion_matrix(pred, y_test));

    random_search = RandomizedSearchCV(ann, param_distributions=parameters,
                                       n_iter=10)
    random_search.fit(X_train, np.squeeze(y_train))
    pred = random_search.predict(X_test);
    print(confusion_matrix(pred, y_test));
    #scores = cross_val_score(svc2, X_scaled, np.squeeze(yclass), cv = 5);
    #print(np.mean(scores))
    print(ann2.best_params_);
    means = ann2.cv_results_['mean_test_score']
    stds = ann2.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, ann2.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))
    ann3 = MLPClassifier(solver=['lbfgs'], alpha=4, hidden_layer_sizes=(25,1), random_state=1, learning_rate = 'adaptive')
    print(classification_report(y_test, pred))
    crossval = cross_val_score(ann2, X_scaled, np.squeeze(yclass), cv = 10)
    print('cross_validation: ' +str(np.mean(crossval)))
    pcavis.PCAReduction(X_scaled, classifiers)
    plt.show()





