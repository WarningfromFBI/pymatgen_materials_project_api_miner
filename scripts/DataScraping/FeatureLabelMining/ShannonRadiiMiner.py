
##Read out all the Shannon radii data into a data file...write a version to our materials project database
#we want the dataset so that we can access everything by an element key, then get access to all remaining data.
import settings
import pandas as pd
import numpy as np;
import re
import json
ShannonBase = settings.MaterialsProject+'\\ShannonRadii';

dataframe = pd.read_csv(ShannonBase+'\\'+'Radii.csv', index_col = 0);
d2 = pd.read_csv(ShannonBase+'\\'+'Radii.csv')
ShannonPoints = dict();
for i in dataframe.index:
    key = " ".join(re.findall("[a-zA-Z]+", i))
    if(key in ShannonPoints.keys()):
        continue;
    else:
        ShannonPoints[key] = list();

#create a dictionary for every element
for i in d2.values:
    key = " ".join(re.findall("[a-zA-Z]+", i[0]))
    print(key)
    if(key in ShannonPoints.keys()):
        continue;
    else:
        ShannonPoints[key].append(list())
print(ShannonPoints)

#start populating the dictionary for each element
for i in d2.values:
    key = " ".join(re.findall("[a-zA-Z]+", i[0]))
    newdict = dict();
    newdict['oxidation_num'] =i[1];
    newdict['electron_config'] = i[2];
    newdict['ionic_radius'] = i[5]
    newdict['coordination_no'] = i[3];
    newdict['crystal_radius'] = i[6]
    newdict['Z/IR'] = i[8]
    ShannonPoints[key].append(newdict)


#write the new dictionary as a json file

f = open(ShannonBase +'\\ShannonRadiiDictionary.json', 'w');
json.dump(ShannonPoints, f);
f.close()

#test
f2 = open(ShannonBase+'\\ShannonRadiiDictionary.json','r');
test = json.load(f2);