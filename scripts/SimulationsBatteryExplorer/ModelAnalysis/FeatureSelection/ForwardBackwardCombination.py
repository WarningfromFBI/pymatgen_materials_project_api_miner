
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
from sklearn import svm
import pandas as pd
import random
import ModelAnalysis.PCA as pcavis
import MinedDataSets.DataReader.CombineFeatureSets as cfs
import MinedDataSets.DataReader.ResponsePredictorValidation as rpv

import settings

vlabels = fle.getLabels('volumeLabels');

[X1, x] = fle.getFeaturesII(settings.MinedFeatureSets + '\\FeatureSelectionSets\\BackwardFeatureSelectionBond.csv')
[X2, x] = fle.getFeaturesII(settings.MinedFeatureSets + '\\FeatureSelectionSets\\ForwardFeatureSelectionBond.csv')
result = pd.concat([X1, X2], axis = 1)

[X, symLabels] = rpv.compareFeatureSets(result, vlabels);
seen = list();
for i in X.columns:
    if(i in seen):
        X.drop(i, axis = 1, inplace = True)
    seen.append(i)
X = result #does repetitive features actually improve model performance?
X_scaled = preprocessing.scale(X);

y = symLabels['dVdensity'];
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
print('\nneural network')
ann = MLPClassifier(solver='lbfgs', alpha=1, hidden_layer_sizes=(15, 4), random_state=1)
ann.fit(X_train, y_train)
pred = ann.predict(X_test);
print(confusion_matrix(pred, y_test))
print(ann.score(X_test, y_test))
scores = cross_val_score(ann, X_scaled, np.squeeze(yclass), cv=20)
print('cross validation: ' + str(np.mean(scores)))

print("logistic regression")
clf.fit(X_train, y_train);
pred = clf.predict(X_test);
miscal = np.count_nonzero(pred.reshape(len(pred), 1) - y_test) / len(pred)
clfscore = clf.score(X_test, y_test);
print(confusion_matrix(pred, y_test));
print(clfscore)
print(np.count_nonzero(y_test) / len(y_test))
scores = cross_val_score(clf, X_scaled, classifiers, cv=10);  # y has to be a list
print("log reg cross validation: " + str(np.mean(scores)))

print('\n SVC')
## PYTHON's RANDOM FOREST
svmach = svm.SVC(kernel='rbf', C=1000, gamma=0.0001)
svmach.fit(X_train, y_train);
preds = svmach.predict(X_test);
print(confusion_matrix(preds, y_test))
print(svmach.score(X_test, y_test))
print(np.count_nonzero(y_test) / len(y_test))
scores = cross_val_score(svmach, X_scaled, classifiers, cv=10);  # y has to be a list
print("random forest cross validation: " + str(np.mean(scores)))
print('\n')

print('\n Random Forest')
## PYTHON's RANDOM FOREST
extc = ExtraTreesClassifier()
rfc = RandomForestClassifier(n_jobs=4)
rfc.fit(X_train, y_train);
preds = rfc.predict(X_test);
print(confusion_matrix(preds, y_test))
print(rfc.score(X_test, y_test))
print(np.count_nonzero(y_test) / len(y_test))
scores = cross_val_score(rfc, X_scaled, classifiers, cv=10);  # y has to be a list
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
print(extc.score(X_test, y_test))
print(np.count_nonzero(y_test) / len(y_test))
scores = cross_val_score(extc, X_scaled, classifiers, cv=10);  # y has to be a list
print("random forest cross validation: " + str(np.mean(scores)))
print('\n')

#store the combined feature set
result.to_csv(settings.MinedFeatureSets + '\\FeatureSelectionSets\\BackwardForwardSelectionBond.csv')

pcavis.PCAReduction(X_scaled, classifiers)
plt.show()








