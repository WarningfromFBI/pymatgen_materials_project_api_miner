##===========FILTER BY NORM LI FRAC ===============================#
#VNORM LiFRAC GIVES THE BEST TRAINING/TEST RESULTS....
import settings
import pandas as pd
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle
import numpy as np

Label = 'VnormLiFrac'

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

filtering = vlabels[Label]

for i in vlabels.index:
    if(vlabelsT[i][Label] > np.mean(filtering)):
        filteredLabels2[i] = (vlabelsT[i]);
        filteredFeatures2[i] = featuresT[i];
    else:
        filteredLabels[i] = (vlabelsT[i]);
        filteredFeatures[i] = featuresT[i];

datadir = settings.MinedFeatureSets + '\\FilteredDataSets'
filteredLabels = filteredLabels.transpose();
filteredFeatures = filteredFeatures.transpose();
filteredFeatures2 = filteredFeatures2.transpose();
filteredLabels2 = filteredLabels2.transpose();
filteredLabels.to_csv(datadir+ '\\LabelsFilteredBy'+Label+'.csv')
filteredFeatures.to_csv(datadir + '\\FeaturesFilteredBy'+Label+'.csv')
filteredLabels2.to_csv(datadir+ '\\InitialLabels'+Label+'.csv')
filteredFeatures2.to_csv(datadir + '\\InitialFeatures'+Label+'.csv')

