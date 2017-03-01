import json;
import os;
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import LabelMiner.VolumeExpansionVariablePyMagten as VEVP
import MaterialsProjectReader.MegaBaseReader as mbf
import LabelMiner.BatteryAnisotropyFeature as anfeat
import settings
from LabelMiner import BatteryVolumeEnergyFeature as bve
from LabelMiner import BatteryVolumeExpansionFeature as BVEF;
import MaterialsProjectReader as mpr;

plt.close("all")
structureclasses = settings.MaterialsProject +'\\StructureBase'
batteries = settings.MaterialsProject+ '\\LithiumBatteryExplorer';
MinedDataSets = settings.DynamicFeatureSets+'\\VolumeLabels'
testcounter = 0;

volumesNormStoich = list(); rownames= list();
volumesNormEnergy = list();
for filename in os.listdir(batteries):
    testcounter += 1;
    file = open(batteries + "\\" + filename, 'r')
    data = "";
    for line in file:
        data = json.loads(line);
    print(data)
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
        batterydict = data['adj_pairs'][i];
        mpfile = unlithiatedmpid+'.txt'; mpfile2 = lithiatedmpid+'.txt';
        try:
            ## THIS IS THE ONLY PLACE WHERE WE READ ANY FILES
            [matdata, structuredata] = mpr.MegaBaseReader.readCompound(mpfile)
            [matdatalith, structuredatalith] = mpr.MegaBaseReader.readCompound(mpfile2)
            lithstruct = pickle.load(open(structureclasses + '\\' + batterydict['id_discharge'] + '.p', 'rb'));
            unlithstruct = pickle.load(open(structureclasses + '\\' + batterydict['id_charge'] + '.p', 'rb'))

            lith = [matdatalith, structuredatalith]; unlith = [matdata, structuredata];
            #Check the phases are teh same

            labels = ""
            ##=======================APPLY MINING FUNCTIONS TO GET DATA =====================================#
            volLabels = VEVP.volumeLabels(batterydict, lithstruct, unlithstruct);
            volenergyLabels = bve.deltaVolNormCapacity(batterydict, lith, unlith, lithstruct, unlithstruct);
            if(volLabels == -1 or volenergyLabels == -1): #this is the case where there was no data for one of the component compounds
                continue;
            batteryid = (data['battid']+', '+batterydict['formula_charge']+', '+batterydict['formula_discharge'] +
                    ', ' + matdata['material_id'] + ', ' + matdatalith['material_id'])
            #Getanisotropylabels
            anisotropyLabels = anfeat.getDeltaR(lithstruct, unlithstruct);
            rownames.append(batteryid)
            volumesNormStoich.append(list(volLabels.values())+list(volenergyLabels.values())+list(anisotropyLabels.values()));
            labels = list(volLabels.keys())+list(volenergyLabels.keys())+list(anisotropyLabels.keys());

        except Exception as e: #generally designed to deal with problems when a file does not exist
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


print(labels); volumesNormStoich = np.array(volumesNormStoich)
print(volumesNormStoich.shape)
plt.plot(volumesNormStoich)
print(len(labels))
names = labels;

##---WRITE LABELS TO A CSV FILE
volumeLabels = pd.DataFrame(volumesNormStoich, columns = labels, index = rownames);
volumeLabels.to_csv(settings.DynamicFeatureSets+'\\VolumeLabels\\volumeLabels.csv');

#Now perform the validation

#importing this script runs it
#import scripts.DataScraping.FeatureLabelMining.ResponsePredictorValidation


