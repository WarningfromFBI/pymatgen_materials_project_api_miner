import settings
import csv
import pandas as pd;

import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle;
layeredDir = settings.MaterialsProject+'\\LithiumBatteryCompounds'

[Xdata, X] = fle.getFeatures('ReducedAllFeatures')
idData = Xdata.index;
XdataTranspose = Xdata.transpose();
counter = 0; totalcounter = 0; Xlayered = pd.DataFrame()
csvfile =  open(layeredDir+'\\lithiated_layered.csv', 'r');
spamreader = csv.reader(csvfile)
idData = XdataTranspose.transpose().index;
for row in spamreader:
     #print(row)
     check = False;
     lithiatedID = row[0]; unlithID = row[2]
     for j in idData:
         if(lithiatedID in j and unlithID in j):
             #print(lithiatedID+': '+j)
             Xlayered[j] = XdataTranspose[j]
             Xdata.drop(j, axis=0, inplace=True);
             counter+=1
             check = True;

     totalcounter+=1
csvfile.close();


print(counter)
print(totalcounter)
print(Xdata.shape)
print(Xlayered.shape)
print(X.shape)
Xlayered = Xlayered.transpose()
Xlayered.to_csv(settings.MinedFeatureSets+'\\FeatureSets\\Layered.csv')
Xdata.to_csv(settings.MinedFeatureSets+'\\FeatureSets\\UnLayered.csv')

