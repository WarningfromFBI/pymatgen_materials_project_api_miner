import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle
from sklearn import linear_model
from sklearn.model_selection import train_test_split;
import LabelMiner.ClassifierCreation.LabelDistributionClassifiers as ldc
import pandas as pd;
import numpy as np
import matplotlib.pyplot as plt

## forward feature selection

[vlabels, XDataFrame, X, anisotropy] = fle.getLabelsFeatures('AllFeatures')
[vlabels, XDataFrame, X] = fle.getFilteredLabelsFeatures('noLiInitialFeatures', 'noLiInitialLabels')
for k in vlabels:
    print(k)
    y = vlabels[k];
    yclass = ldc.createBinaryClassifierbyMean(y);
    if(len(set(yclass))<2):
        continue;
    yclass = np.reshape(np.array(yclass),(len(yclass),1))
    bestFeatures = pd.DataFrame(columns = XDataFrame.columns);
    errors = list();
    featuresMatrix = np.empty((len(y),1))
    for i in range(5):
        #pick the best set of features in X
        scoreDict = dict();
        clf = linear_model.LogisticRegression();
        for feature in XDataFrame:
            #print(feature)
            data = (XDataFrame[feature].values);
            data = np.array(data).transpose()
            data = np.reshape(data,(len(data),1))
            data = np.concatenate((featuresMatrix, data), axis=1)

            X_train, X_test, y_train, y_test = train_test_split(data, yclass, test_size=0.33)
            clf.fit(X_train, y_train)
            correct = clf.score(X_test,y_test)
            misclass = 1-correct;
            #print(misclass)
            scoreDict[feature] = correct;

        #now select the best feature
        maxSeen = 0; maxLabel = "";
        for feat in scoreDict:
            if(scoreDict[feat] > maxSeen):
                maxSeen = scoreDict[feat];
                maxLabel = feat;

        errors.append(maxSeen);
        print(maxLabel)
        featuresMatrix = np.concatenate((featuresMatrix, np.reshape((XDataFrame[maxLabel].values), (len(y),1))), axis = 1)
        bestFeatures.add(XDataFrame[maxLabel])
        #print(featuresMatrix)
        print(maxSeen)

        #del XDataFrame[maxLabel]
    #check how good this optimal model is

    f2 = linear_model.LogisticRegression();
    X_train, X_test, y_train, y_test = train_test_split(featuresMatrix, yclass, test_size=0.33)
    f2.fit(X_train, y_train);
    print(f2.score(X_test,y_test))
    print(errors)
    print('\n')

    plt.figure();
    plt.plot(errors);
    plt.show()
