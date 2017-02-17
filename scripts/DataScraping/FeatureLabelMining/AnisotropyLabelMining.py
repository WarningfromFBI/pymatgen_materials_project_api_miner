import json;
import os;
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import LabelMiner.BatteryAnisotropyFeature as baf
import MaterialsProjectReader.MegaBaseReader as mbf;
import MaterialsProjectReader.StructureBaseReader as SBR
import settings

plt.close("all")

batteries = settings.MaterialsProject + '\\LithiumBatteryExplorer';
MinedDataSets = settings.MinedFeatureSets+'\\VolumeLabels'
testcounter = 0;

rownames= list();
latticeAnisotropy = list();
for filename in os.listdir(batteries):
    testcounter += 1;
    file = open(batteries + "\\" + filename, 'r')
    data = "";
    for line in file:
        data = json.loads(line);
    maxVol = 0;
    for i in range(len(data['adj_pairs'])):
        dischargeState = data['adj_pairs'][i];
        if(dischargeState['max_delta_volume'] > maxVol):
            maxVol = dischargeState['max_delta_volume'];
        if(data['adj_pairs'][i]['max_delta_volume'] == 0):
            print(data['battid']);
            continue;
        #Now we can perform whatever analysis we want
        # now we can extract all the dat
        unlithiatedmpid = data['adj_pairs'][i]['id_charge'];
        lithiatedmpid = data['adj_pairs'][i]['id_discharge']
        mpfile = unlithiatedmpid+'.txt'; mpfile2 = lithiatedmpid+'.txt';
        try:
            [matdata, structuredata] = mbf.readCompound(mpfile)
            [matdatalith, structuredatalith] = mbf.readCompound(mpfile2)
            structureunlith = SBR.readStructure(unlithiatedmpid);
            structurelith = SBR.readStructure(lithiatedmpid);
            #print(structuredata)
            #Check the phases are th same
            anisotropy = baf.getDeltaR(structureunlith, structurelith);
            latticeAnisotropy.append(list(anisotropy.values()))
            rownames.append(data['battid'])
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            continue;

labels = anisotropy.keys();
print(labels); latticeAnisotropy= np.array(latticeAnisotropy)
print(latticeAnisotropy.shape)
plt.plot(latticeAnisotropy)
names = labels;

##---WRITE LABELS TO A CSV FILE
anisotropyLabels = pd.DataFrame(latticeAnisotropy, columns = labels, index = rownames);

summary_ave_data = anisotropyLabels.copy()
summary_ave_data.to_csv(MinedDataSets + '\\anisotropyLabels.csv');


