import os;
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import *

import APIMining as manifest
import settings
from MaterialsProjectReader import BatteryBaseReader as bbr
from MaterialsProjectReader import MegaBaseReader as mbf;
from feature_miner_functions import BatteryMatDataFeatures as BAF;

plt.close("all")

directory = settings.basedirectory + '\\MaterialsProject\LithiumBatteryExplorer';
structureDir = settings.MaterialsProject+'\\StructureBase'


testcounter = 0; datframerows = list();
materialMatrix = list();
for filename in os.listdir(directory):
    testcounter+=1;
    #if(testcounter>2): break;

    print('file no. ' + str(testcounter))
    batterydata = bbr.readBattery(filename);
    #print(data)

    for i in range(len(batterydata['adj_pairs'])):
        dischargeState = batterydata['adj_pairs'][i];

        if(batterydata['adj_pairs'][i]['max_delta_volume'] == 0):
            print(batterydata['battid']);
            continue;

        unlithiatedmpid = batterydata['adj_pairs'][i]['id_charge'];
        lithiatedmpid = batterydata['adj_pairs'][i]['id_discharge']
        mpfile = unlithiatedmpid+'.txt'; mpfile2 = lithiatedmpid+'.txt';

        try:
            [matdata, structuredata] = mbf.readCompound(mpfile)
            [matdatalith, structuredatalith] = mbf.readCompound(mpfile2)
            structureClassUnLith = pickle.load(open(structureDir+'\\'+unlithiatedmpid+'.p', 'rb'));
            ##================STRUCTURAL FEATURE EXTRACTION===============================#


            unitcellMass = BAF.unitCellMass(matdata['unit_cell_formula'])
            atomTypes = BAF.AtomTypeCount(matdata['unit_cell_formula']);
            atomNumLabels = ['atomMean', 'atomStd']
            atomTypesLabel = ['halogen','transition', 'actinoid','chalcogen', 'metalloid', 'rare', 'other', 'alkaline']
            atomNum = BAF.atomicNumber(matdata['unit_cell_formula']);

            # vanderRad = BAF.vanderWaalRadius(matdata['unit_cell_formula'], matdata['volume']);
            answer = [matdata['density'], matdata['energy_per_atom'], matdata['nsites'],
                                   matdata['nelements'], matdata['band_gap'], matdata['volume'], unitcellMass,
                                   matdata['energy'],
                                   matdata['formation_energy_per_atom'], matdata['total_magnetization'],
                                   matdata['e_above_hull']] + list(atomNum) + list(atomTypes);
            materialMatrix.append(answer);

            materialsLabels = ['density', 'energy_per_atom', 'nsites', 'nelements', 'bandgap', 'volume',
                               'Unit Cell Mass',
                               'energy', 'formationenergy_pa', 'total_magnetization', 'energysStab'] + atomNumLabels +atomTypesLabel;

            datframerows.append(
                filename.strip('+.txt') + ', ' + matdata['pretty_formula'] + ', ' + matdatalith['pretty_formula']
                + ', ' + matdata['material_id'] + ', ' + matdatalith['material_id'])

        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("mpid: " + unlithiatedmpid)
                manifest.AddMPIDtoManifest(lithiatedmpid);
                manifest.AddMPIDtoManifest(unlithiatedmpid);
                print(exc_type, fname, exc_tb.tb_lineno)
                break;

labels = materialsLabels;
# print(labels);
print(len(labels))
names = labels;

materialMatrix = np.array(materialMatrix)
TotalData = materialMatrix

# Create separate csv files for the structures and for the atomistic
# atomisticMatrix = np.concatenate((atomisticMatrix,np.array(v2).reshape((len(v2),4))), axis = 1)
# BANDGAP IS AN EXCELLENT PREDICTOR!!!!!!!!!!!!!

print('data shape:' + str(TotalData.shape));
print('length of labels: ' + str(len(labels)));

datframe = pd.DataFrame(TotalData, columns=labels, index=datframerows);
datframe.to_csv(settings.DynamicFeatureSets + '\\FeatureSets\MatDataFeatures.csv');
# scatter_matrix(datframe)

################################### SOME BASIC ANALYSES ##############################################################
# print(datframe)

##Perform data validation

