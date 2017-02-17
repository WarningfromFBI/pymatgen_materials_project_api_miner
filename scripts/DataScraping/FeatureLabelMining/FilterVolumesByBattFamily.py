import matplotlib.pyplot as plt

import os;
import json;
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import settings
import pickle
plt.close("all")

batteries = settings.MaterialsProject + '\\LithiumBatteryExplorer';
MinedDataSets = settings.MinedFeatureSets + '\\VolumeLabels'
testcounter = 0;

volumesNormStoich = list();
rownames = list();
volumesNormEnergy = list();
BatteriesByElements = dict();
for filename in os.listdir(batteries):
    testcounter += 1;

    file = open(batteries + "\\" + filename, 'r')
    data = "";
    for line in file:
        data = json.loads(line);
    maxVol = 0;
    framework = data['framework']
    key = tuple(framework['elements'])
    if(key in BatteriesByElements):
        BatteriesByElements[key].append(data['adj_pairs']);
    else:
        BatteriesByElements[key] = list();
        BatteriesByElements[key].append(data['adj_pairs']);

print(BatteriesByElements)
f = open(settings.MinedFeatureSets+'\\BatteriesByElements.pickle', 'wb') #couldn't get this into a json file
pickle.dump(BatteriesByElements, f)
f.close()

f = open(settings.MinedFeatureSets+'\\BatteriesByElements.pickle', 'rb')
test = pickle.load(f)
print(test == BatteriesByElements);
