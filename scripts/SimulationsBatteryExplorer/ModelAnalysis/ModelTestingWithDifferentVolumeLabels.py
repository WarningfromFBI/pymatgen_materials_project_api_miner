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
import ModelAnalysis.PCA as pca
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle
from pandas.tools.plotting import table
from sklearn.ensemble import RandomForestClassifier

plt.close("all")
datadirectory = settings.MinedFeatureSets + '\\FeatureSets';
labeldirectory = settings.MinedFeatureSets + '\\VolumeLabels';
filtereddirectory = settings.MinedFeatureSets + '\\FilteredDataSets'
vlabels = pd.read_csv(labeldirectory+'\\volumeLabels.csv', index_col = 0);
anisotropylabels = pd.read_csv(labeldirectory+'\\anisotropyLabels.csv');
data = pd.read_csv(datadirectory+'\\AllFeatures.csv', index_col = 0);
# Convert data pdframe to np array

counter = 0; X = list();
for k in data.keys():
    if(counter == 0):
        counter+=1;
        continue;
    X.append(data[k].values);
X = np.array(X); X = np.transpose(X)
counter = 0;

[vlabels, data, X] = fle.getFilteredLabelsFeatures('noLiInitialFeatures', 'noLiInitialLabels')
experimentlabels = vlabels
X = preprocessing.scale(X);
##DATA Summary
print('feature shape: '+str(X.shape))

for i in (experimentlabels.keys()):
    counter+=1;
    y = experimentlabels[i].values; #some of our y's are coming out with 1893 samples, but the X features only has 1891 samples
    print('\n')
    print(i + ", " + str(y.shape))
    [train, intermed, ytrain, yintermed] = tcs.TwoClassSeparatedLabels(X,y, 100,0);
    Xsplit = X;
    ysplit = y;

    clf = linear_model.LogisticRegression();
    clf = linear_model.LogisticRegressionCV();
    #clfcv.fit
    classifiers = list();
    for j in ysplit:
        if(j > np.mean(y)):
            classifiers.append(1)
        else:
            classifiers.append(0)
    yclass = np.array(classifiers).reshape(len(classifiers),1);

    X_train, X_test, y_train, y_test = train_test_split(Xsplit, yclass, test_size=0.33, random_state=42)
    try:
        clf.fit(X_train, y_train);
        pred = clf.predict(X_test);
        miscal  = np.count_nonzero(pred.reshape(len(pred),1)-y_test)/len(pred)
        s = clf.score(X_test, y_test);
        pos = np.count_nonzero(y_test) / len(y_test)
        neg = 1-pos
        if(s - max([pos, neg]) < 0.1):
            continue;

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
        d = data.shape;

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

plt.show()

