import settings
import pandas as pd
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle
datadir = settings.MinedFeatureSets+'\\VolumeLabels'
labeldir = settings.MinedFeatureSets+'\\FeatureSets'

def filterByInitialLithium(datadir):
    [XdataFrame, X] = fle.getFeatures(datadir);

    counter = 0; othercounter = 0;
    featuresT = XdataFrame.transpose();

    filteredFeatures = pd.DataFrame(index = XdataFrame.columns);
    filteredFeatures2 = pd.DataFrame(index = XdataFrame.columns);

    for i in XdataFrame.index:
        labels = str(i).split(',')
        if('Li' in labels[1] and 'Li' in labels[2]):
            print(labels)
            counter+=1;
            filteredFeatures2[i] = featuresT[i];
        else:
            othercounter+=1;
            filteredFeatures[i] = featuresT[i];

    print(counter)
    print(othercounter)

    datadir = settings.MinedFeatureSets + '\\FilteredDataSets'
    filteredFeatures = filteredFeatures.transpose();
    filteredFeatures2 = filteredFeatures2.transpose();
    filteredFeatures.to_csv(datadir + '\\noLiInitialFeatures.csv')
    filteredFeatures2.to_csv(datadir + '\\LiInitialFeatures.csv')
    print('Done')

    return [filteredFeatures, filteredFeatures2]



