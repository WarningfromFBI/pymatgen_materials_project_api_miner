from sklearn import preprocessing
import numpy as np
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn.linear_model import Ridge;
from sklearn import svm;
from sklearn.model_selection import train_test_split;
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix
import ModelAnalysis.Sampling.TwoClassSampling as tcs;
import settings
from sklearn.feature_selection import RFE
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import ModelAnalysis.AutoFitModel.LogisticReg as LR;
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
import MinedDataSets.DataReader.ResponsePredictorValidation as rpv
import scripts.DataScraping.TrainingSetFiltering.FilterbyLithiumLevel as fll

plt.close("all")

[data, X] = fle.getFeatures('StructureFeatures')
vlabels = fle.getLabels('volumeLabels');
[data, vlabels] = rpv.compareFeatureSets(data, vlabels);
X = data.values

vlabels = fle.getLabels('volumeLabels');
Xsymmetry = fle.getFeatures('StructureFeatures')
Xstruct = fle.getFeatures('SymmetryFeatures');
[Xstruct, Xsym] = rpv.compareFeatureSets(Xstruct[0], Xsymmetry[0]);
[Xsym, symLabels] = rpv.compareFeatureSets(Xsym, vlabels)
X = np.concatenate((Xsym.values, Xstruct.values), axis=1);
print('vlabels: ' + str(vlabels.shape))
[ff1, ff2] = fll.filterByInitialLithium('AtomisticFeatures')
[X2, symLabels] = rpv.compareFeatureSets(ff2, vlabels);

# Standardizing the Data
X = preprocessing.scale(X2.values);
vlabels = symLabels;

##DATA Summary
print('feature shape: '+str(X.shape))
clf = linear_model.LogisticRegression();
d = open('topFeatures.txt', 'w')
f2 = open('topfeatureschi.txt', 'w')

print(X.shape)

response = 'dVperAtom'
#X_train, y_train, X_test, y_test = train_test_split(X, y);
y = vlabels[response].values; #some of our y's are coming out with 1893 samples, but the X features only has 1891 samples
print(response + ", " + str(y.shape))
Xsplit = X;
ysplit = y;
topFeaturesList = list();
classifiers = list();
for i in y:
    if (i > np.mean(y)):
        classifiers.append(1)
    else:
        classifiers.append(0)
yclass = np.array(classifiers).reshape(len(classifiers), 1);

# ## BEST FEATURE SELECTION
# J = SelectKBest(k = 23);
# X_new = J.fit_transform(Xsplit, yclass) #requires non-negative X
# featuresSelected = J.get_support(J);
# #print(featuresSelected)
# print('\n')
# #print(X_new.shape)
#
# #quicktest
# LR.runLogReg(X_new,yclass)
clf = linear_model.LogisticRegression();

scoreList = list();
for i in range(20): #this yields pretty shitty models
    selector = RFE(clf, len(yclass)-i, step=1)
    selector = selector.fit(Xsplit, np.squeeze(yclass))
    #print(selector.get_support(selector))

    topFeaturesList.sort()
    X2 = selector.fit_transform(Xsplit, yclass);
    X_train, X_test, y_train, y_test = train_test_split(X2, yclass, test_size=0.33)

    clf.fit(X_train, y_train);
    scoreList.append((clf.score(X_test, y_test)))

    LR.runLogReg(X2, yclass);
#WE NEED TO IDENTIFY THE FEATURES THAT WERE KEPT


d.close()
plt.plot(scoreList)
plt.show()



