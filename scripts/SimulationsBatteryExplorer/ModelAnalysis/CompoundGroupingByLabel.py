
## With different volume labels, we want to create lists of different compounds grouped as low expansion or
## high expansion
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle;
from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np;
import settings

plt.close("all")
[vlabels, Data, X, anisotropylabels] = fle.getLabelsFeatures();
counter = 0;
X_scaled = preprocessing.scale(X);
batteryid = vlabels['Unnamed: 0'].values;
counter = 0;
for i in vlabels:
    if(counter == 0):
        counter+=1;
        continue;
    highlist = list(); lowlist = list();
    y = vlabels[i].values;
    yavg = np.mean(y);
    for j in range(len(y)):
        if(y[j] > yavg):
            highlist.append(batteryid[j]);
        else:
            lowlist.append(batteryid[j]);

    writedirectory = settings.MinedFeatureSets+'\\LabelledDataSets';

    file = open(writedirectory+'\\HighExpansion'+i+'.txt', 'w');
    file.writelines(["%s\n" % item  for item in highlist])
    file2 = open(writedirectory+'\\LowExpansion+'+i+'.txt', 'w');
    file2.writelines(["%s\n" % item  for item in lowlist])
    file.close();
    file2.close();




