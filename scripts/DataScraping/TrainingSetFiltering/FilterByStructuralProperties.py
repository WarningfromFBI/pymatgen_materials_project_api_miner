import pandas as pd
from sklearn import preprocessing

import LabelMiner.ClassifierCreation.CrystalSystem as cs
import MaterialsProjectReader.MegaBaseReader as MBR;
import MaterialsProjectReader.StructureBaseReader as SBR;
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle
import ModelAnalysis.PCA as pcavis
import settings

#[vlabels, XdataFrame, X, anisotropy] = fle.getLabelsFeatures('AllFeatures')
[vlabels, XdataFrame, X] = fle.getFilteredLabelsFeatures('FeaturesFilteredByVnormLiFrac', 'LabelsFilteredByVnormLiFrac')


counter = 0; othercounter = 0;
vlabelsT = vlabels.transpose();
featuresT = XdataFrame.transpose();

filteredLabels = pd.DataFrame(index = vlabels.columns);
filteredFeatures = pd.DataFrame(index = XdataFrame.columns);

filteredLabels2 = pd.DataFrame(index = vlabels.columns);
filteredFeatures2 = pd.DataFrame(index = XdataFrame.columns);
classifiers = list();
Xnew = list();
for i in vlabels.index:
    labels = str(i).split(', ')
    unlithiatedmpid = labels[3]; lithiatedmpid = labels[4];
    structureunlith = SBR.readStructure(unlithiatedmpid);
    [matdata, structuredata] = MBR.readCompound(unlithiatedmpid+'.txt');
    [matdatalith, structuredatalith] = MBR.readCompound(lithiatedmpid+'.txt');
    crystalLabel = cs.CrystalSysClass(matdata)
    classifiers.append(crystalLabel);
    if(matdata['spacegroup']['crystal_system'] == matdatalith['spacegroup']['crystal_system']):
        filteredFeatures[i] = (featuresT[i]);
        filteredLabels[i] = (vlabelsT[i]);
    else:
        filteredFeatures2[i] = (featuresT[i]);
        filteredLabels2[i] = (vlabelsT[i]);

datadir = settings.MinedFeatureSets + '\\FilteredDataSets'
filteredLabels = filteredLabels.transpose();
filteredFeatures = filteredFeatures.transpose();
filteredFeatures2 = filteredFeatures2.transpose();
filteredLabels2 = filteredLabels2.transpose();
filteredLabels.to_csv(datadir+ '\\LabelNoPhaseChangeNoInitialLi.csv')
filteredFeatures.to_csv(datadir + '\\FeaturesNoPhaseChangeNoInitialLi.csv')
filteredLabels2.to_csv(datadir+ '\\LabelPhaseChangeNoInitialLi.csv')
filteredFeatures2.to_csv(datadir + '\\FeaturesPhaseChangeNoInitialLi.csv')

X = preprocessing.scale(X);
pcavis.PCAReduction(X, classifiers)



