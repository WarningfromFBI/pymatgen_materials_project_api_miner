from sklearn import preprocessing
import numpy as np
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn import svm;
from sklearn.model_selection import train_test_split;
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix
import settings
import ModelAnalysis.PCA as pca
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle
from pandas.tools.plotting import table
from sklearn.ensemble import RandomForestClassifier
import MinedDataSets.DataReader.CombineFeatureSets as cfs
import MinedDataSets.DataReader.ResponsePredictorValidation as rpv
import scripts.DataScraping.TrainingSetFiltering.FilteringFunctions as ff
import LabelMiner.ClassifierCreation.PhaseChange as pc
plt.close("all")

vlabels = fle.getLabels('volumeLabels');
[Xall, X_nparr] = fle.getFeatures('UnLayered')
#[Xall, X_nparr] = fle.getFeatures('AllStructureFeatures')

print(Xall.shape)
[X1, X2] = ff.FilterByLithiumFraction(0.25, Frame=Xall)
print(X1.shape)
[X1, X2] = ff.filterByInitialLithium(Frame=X1)
#[X1, x] = fle.getFeaturesII(settings.MinedFeatureSets+'\\FeatureSelectionSets\\ForwardFeatureSelectiondVweight.csv')
#[X2, X1] = ff.FilterByPreservedCrystalSys(Frame=X1) actually, the model predicts phase changing and non-phase changing equally well
[X, vlabels] = rpv.compareFeatureSets(X1, vlabels);

#Scaling is absolutely critical otherwise the model will prefer features with intrinsicially large variances
X_scaled = preprocessing.scale(X);


##DATA Summary
print('feature shape: '+str(X.shape))
counter = 0;
for i in (vlabels.keys()):
    counter+=1;
    y = vlabels[i]
    print('\n')
    print(i + ", " + str(y.shape))

    clf = linear_model.LogisticRegression();
    #clf = linear_model.LogisticRegressionCV();
    #clfcv.fit
    classifiers = list();
    for j in y:
        if(j > np.mean(y)):
            classifiers.append(1)
        else:
            classifiers.append(0)
    #classifiers = pc.PhaseChange(vlabels);
    yclass = np.array(classifiers).reshape(len(classifiers),1);

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, yclass, test_size=0.33, random_state=42)
    try:
        clf.fit(X_train, y_train);
        pred = clf.predict(X_test);
        miscal  = np.count_nonzero(pred.reshape(len(pred),1)-y_test)/len(pred)
        s = clf.score(X_test, y_test);
        pos = np.count_nonzero(y_test) / len(y_test)
        neg = 1-pos
        # if(s - max([pos, neg]) < 0.1):
        #     continue;

        #cross validation
        #scores = cross_val_score(clf, Xsplit, np.squeeze(yclass), cv = 10);
        #PCA for visualization
       # pca.PCAReduction(Xsplit,yclass);

        #create confusion matrix
        print(confusion_matrix(pred, y_test)) #for 2x2, it goes (0,0) = true negative (1,1)  = true positives, (0,1) = false negatives
        #(1,0) = false positives, predictive capability in the binary regime SUCKS
        print('score: ' + str(clf.score(X_test, y_test)))
        print('test set size: '+str(len(y_test)));
        print('positive examples: ' + str(pos))
        print('negative examples: '+ str(neg))
        print('classifier is '+ str((s - max([pos, neg]))*100) +'% better than majority')
        #print('cross_val: '+str(np.mean(scores)))
        plt.figure()
        plt.hist(y, 200)
        plt.title(i)
        plt.ylabel('counts')
        plt.xlabel('value of volume label')
        plt.rcParams.update({'font.size': 22})
        #pca.PCAReduction(X_scaled, classifiers)


    except Exception as e:
        print(e)
        continue;

# plt.figure()
# ax = plt.subplot(111, frame_on=False)  # no visible frame
# ax.xaxis.set_visible(False)  # hide the x axis
# ax.yaxis.set_visible(False)  # hide the y axis
#
# table(ax, data)

        #plot of change in volumes vs the set of features
    # for i in range(d[1]):
    #     plt.figure()
    #     plt.scatter(X[:,i], y, s = 200, c = classifiers, cmap = 'viridis_r') #'viridis_r

pca.PCAReduction(X_scaled, classifiers)
plt.show()

