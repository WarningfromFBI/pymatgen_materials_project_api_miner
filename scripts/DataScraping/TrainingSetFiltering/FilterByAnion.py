import settings
import pandas as pd
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle
datadir = settings.MinedFeatureSets+'\\VolumeLabels'
labeldir = settings.MinedFeatureSets+'\\FeatureSets'

[vlabels, XdataFrame, X, anisotropy] = fle.getLabelsFeatures('AllFeatures')

counter = 0; othercounter = 0;
vlabelsT = vlabels.transpose();
featuresT = XdataFrame.transpose();

filteredLabels = pd.DataFrame(index = vlabels.columns);
filteredFeatures = pd.DataFrame(index = XdataFrame.columns);

filteredLabels2 = pd.DataFrame(index = vlabels.columns);
filteredFeatures2 = pd.DataFrame(index = XdataFrame.columns);

for i in vlabels.index:
    labels = str(i).split(',')
    if('Li' in labels[1] and 'Li' in labels[2]):
        print(labels)
        counter+=1;
        filteredLabels2[i] = (vlabelsT[i]);
        filteredFeatures2[i] = featuresT[i];
    else:
        othercounter+=1;
        filteredLabels[i] = (vlabelsT[i]);
        filteredFeatures[i] = featuresT[i];

print(counter)
print(othercounter)

datadir = settings.MinedFeatureSets + '\\FilteredDataSets'
filteredLabels = filteredLabels.transpose();
filteredFeatures = filteredFeatures.transpose();
filteredFeatures2 = filteredFeatures2.transpose();
filteredLabels2 = filteredLabels2.transpose();
filteredLabels.to_csv(datadir+ '\\noLiInitialLabels.csv')
filteredFeatures.to_csv(datadir + '\\noLiInitialFeatures.csv')
filteredLabels2.to_csv(datadir+ '\\LiInitialLabels.csv')
filteredFeatures2.to_csv(datadir + '\\LiInitialFeatures.csv')




