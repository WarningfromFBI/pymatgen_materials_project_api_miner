
import numpy as np
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn.linear_model import Ridge;
from sklearn import svm;
from sklearn.model_selection import train_test_split;
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle;
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
import ModelAnalysis.Sampling.TwoClassSampling as tcs;
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm

plt.close("all")
[vlabels, Data, X, anisotropylabels] = fle.getLabelsFeatures('AllFeatures');
[vlabels, data, X] = fle.getFilteredLabelsFeatures('noLiInitialFeatures', 'noLiInitialLabels')
counter = 0;
X_scaled = preprocessing.scale(X);

print('feature shape: '+str(X.shape))
counter = 0;
for j in vlabels:

    y = vlabels[j];
    if(len(y) == 0 or len(set(y))<100):
        continue
    X_scaled = X;
    classifiers = list();
    for i in y:
        if(i > np.mean(y)):
            classifiers.append(1)
        else:
            classifiers.append(0)
    yclass = np.array(classifiers).reshape(len(classifiers),1);

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, yclass, test_size=0.33)
    lassoreg = linear_model.Lasso();
    lassoreg.fit(X, y);
    lassopred = lassoreg.predict(X_train);
    print(lassoreg.score(X, y));
    print(np.mean(abs(lassopred - y_test)))
    print(np.max(y)-np.mean(y))
    print('\n')
