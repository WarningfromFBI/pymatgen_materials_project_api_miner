
import sys
import os
import pandas as pd;
import numpy as np
import matplotlib.pyplot as plt

# this script allows you to mine the battery database and then perform the model analysis simultaneously

# FeatureMiner Directory
# Model Directory



def getMaxDeltaVol(batteryDict):
    maxVol = 0;
    for j in range(len(batteryDict['adj_pairs'])):
        discharge = batteryDict['adj_pairs'][j];
        if(discharge['max_delta_volume'] > maxVol):
            maxVol = discharge['max_delta_volume'];
    return maxVol;

featureDirectory = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DatabaseAnalysis'
batteryMinerDirectory = 'D:\\Nathan\\Documents\StanfordYearOne\Reed Group\IntercalationResearch\BatteryMiner\InHouseDatabase_Miners'
modelAnalysisDirectory = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\ModelAnalysis'
sys.path.append(featureDirectory);
sys.path.append(batteryMinerDirectory);
sys.path.append(modelAnalysisDirectory);
#import IntercalationFeatureModeling as ifm
import GetAllBatteries as gab;

# Step 1: Mine Features
batteryDataMatrix = list();
batteries = gab.GetAllBatteries();
batteryDatDictionary = list();
for i in batteries:
    data = list();
    datadict =dict();
    for j in i:
        if(isinstance(i[j], float)):
            data.append(i[j]); datadict[j] = i[j];
    data.append(getMaxDeltaVol(i))
    print(len(data))
    batteryDataMatrix.append(data);
    batteryDatDictionary.append(datadict);
batteryMatrix = np.array(batteryDataMatrix)
batteryframe = pd.DataFrame(batteryMatrix)
batteryMatrix = np.transpose(batteryMatrix)
corrCoefs = np.corrcoef(batteryMatrix);

keys = list();
for i in batteryDatDictionary[0].keys():
    print(i)
    keys.append(i);
keys.append('volume')

print(corrCoefs.shape);
for i in range(len(corrCoefs)):
    plt.plot(corrCoefs[:, i]), '.-';
plt.plot(corrCoefs[:,-1], 'bs-')
plt.legend(keys)

plt.show()
