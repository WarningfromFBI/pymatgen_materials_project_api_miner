import settings
import pandas as pd
import numpy as np
datadirectory = settings.MinedFeatureSets + '\\FeatureSets';
labeldirectory = settings.MinedFeatureSets + '\\VolumeLabels';
filteredDirectory = settings.MinedFeatureSets + '\\FilteredDataSets'

def getLabelsFeatures(datadir):
    vlabels = pd.read_csv(labeldirectory+'\\volumeLabels.csv', index_col = 0);
   # anisotropylabels = pd.read_csv(labeldirectory+'\\anisotropyLabels.csv', index_col = 0);
    data = pd.read_csv(datadirectory+'\\'+datadir+'.csv', index_col = 0);

    ##Convert data into a np.array (for sk-learn)
    counter = 0;
    X = list();
    for i in data.keys():
        if (counter == 0):
            print(i);
            counter += 1;
            continue;
        X.append(data[i].values);
    X = np.array(X);
    X = np.transpose(X)

    return [vlabels, data, X]

def getLabels(datadir):
    vlabels = pd.read_csv(labeldirectory + '\\volumeLabels.csv', index_col=0);
    return vlabels

def getFeatures(datadir):
    data = pd.read_csv(datadirectory+'\\'+datadir+'.csv', index_col = 0);
    ##Convert data into a np.array (for sk-learn)
    counter = 0;
    X = list();
    for i in data.keys():
        if (counter == 0):
            print(i);
            counter += 1;
            continue;
        X.append(data[i].values);
    X = np.array(X);
    X = np.transpose(X)

    return [data, X]


def getFilteredLabelsFeatures(Features, Labels):
    vlabels = pd.read_csv(filteredDirectory+'\\'+Labels+'.csv', index_col = 0);
    data = pd.read_csv(filteredDirectory+'\\'+Features+'.csv', index_col = 0);

    ##Convert data into a np.array (for sk-learn)
    counter = 0;
    X = list();
    for i in data.keys():
        if (counter == 0):
            print(i);
            counter += 1;
            continue;
        X.append(data[i].values);
    X = np.array(X);
    X = np.transpose(X)

    return [vlabels, data, X]
