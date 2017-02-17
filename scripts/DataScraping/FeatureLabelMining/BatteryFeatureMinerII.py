import os;
import sys;
import pickle
from multiprocessing import Pool
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import *

import APIMining.MaterialsAPIMiner.AddMPIDToManifest as manifest
import settings
from FeatureMiner import BatteryStructureFeaturesII as BAF;
from FeatureMiner import BatteryStructureFeatures as BSF;
from FeatureMiner import WolvertonAtomisticFeatures as waf;
from FeatureMiner import BatterySymmetryFeatures as BsymF
from MaterialsProjectReader import BatteryBaseReader as bbr
from MaterialsProjectReader import MegaBaseReader as mbf;
import MinedDataSets.DataReader.ResponsePredictorValidation as rpv
plt.close("all")

directory = settings.basedirectory + '\\MaterialsProject\LithiumBatteryExplorer';
structureDir = settings.MaterialsProject+'\\StructureBase'

#iterate through all data files in the batterydatabase; Create a total matrix of all the data we want
structureMatrix = list(); materialMatrix = list();
materialCrystalSys = list(); elementCounter = list(); atomisticMatrix = list(); v2 = list();
weightedAtom = list();
materialsLabels = list(); structureLabels = list(); symmetryMatrix = list();
datframerows = list();

debugcounter = 0;testcounter = 0;
for filename in os.listdir(directory):
    testcounter+=1;
    if(testcounter > 2): break;

    print('file no. ' + str(testcounter))
    file = open(directory + "\\" + filename, 'r')
    batterydata = bbr.readBattery(file);
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
            labels = ""
            [matdata, structuredata] = mbf.readCompound(mpfile)
            [matdatalith, structuredatalith] = mbf.readCompound(mpfile2)
            structureClassUnLith = pickle.load(open(structureDir+'\\'+unlithiatedmpid+'.p', 'rb'));
            datframerows.append(filename.strip('+.txt') + ', ' + matdata['pretty_formula'] + ', ' + matdatalith['pretty_formula']
                + ', ' + matdata['material_id'] + ', ' + matdatalith['material_id'])
            ##================STRUCTURAL FEATURE EXTRACTION===============================#

            [structuredata, structureLabels] = BSF.GetAllStructureFeatures(structuredata, structureClassUnLith);
            structureMatrix.append(structuredata)
            #Materials Intrinsic Properties Mining
            unitcellMass = BAF.unitCellMass(matdata['unit_cell_formula'])
            atomTypes = BAF.AtomTypeCount(matdata['unit_cell_formula']);
            #vanderRad = BAF.vanderWaalRadius(matdata['unit_cell_formula'], matdata['volume']);
            elementCounter.append(atomTypes);
            materialMatrix.append([matdata['density'], matdata['energy_per_atom'], matdata['nsites'],
                                   matdata['nelements'], matdata['band_gap'], matdata['volume'], unitcellMass, matdata['energy'],
                                   matdata['formation_energy_per_atom'], matdata['total_magnetization'], matdata['e_above_hull']]);

            materialsLabels = ['density', 'energy_per_atom', 'nsites', 'nelements', 'bandgap', 'volume', 'Unit Cell Mass',
                               'energy', 'formationenergy_pa', 'total_magnetization', 'energysStab'];


            #=================Atomistic Mining from Wolverton=============================#
            [feat, atomisticLabels] = waf.getAllSummaryStats(matdata['unit_cell_formula'])
            [feat2, weightedlabel] = waf.getWeightedStats(matdata['unit_cell_formula']);
            atomisticMatrix.append(feat);  weightedAtom.append(np.squeeze(feat2))

            ##================SYMMETRY DATA================================#
            [symmetrydata, symmetryLabels] = BsymF.GetAllSymmetries(structureClassUnLith);
            symmetryMatrix.append(symmetrydata);


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("mpid: " + unlithiatedmpid)
            manifest.AddMPIDtoManifest(lithiatedmpid);
            manifest.AddMPIDtoManifest(unlithiatedmpid);
            print(exc_type, fname, exc_tb.tb_lineno)
            datframerows.remove(filename.strip('+.txt') + ', ' + matdata['pretty_formula'] + ', ' + matdatalith['pretty_formula']
                + ', ' + matdata['material_id'] + ', ' + matdatalith['material_id'])
            break;



labels = materialsLabels + structureLabels + atomisticLabels + weightedlabel+ symmetryLabels;
#print(labels);
print(len(labels))
names = labels;
atomisticMatrix = np.array(atomisticMatrix); weightedAtom = np.array(weightedAtom); symmetryMatrix = np.array(symmetryMatrix);
structureMatrix = np.array(structureMatrix); materialMatrix = np.array(materialMatrix)
atomisticFrame = pd.DataFrame(atomisticMatrix, columns =  atomisticLabels, index = datframerows)
weightedAtomFrame = pd.DataFrame(weightedAtom, columns = weightedlabel, index = datframerows)
structureFrame=pd.DataFrame(symmetryMatrix, columns = symmetryLabels, index = datframerows)
symmetryFrame=pd.DataFrame(structureMatrix, columns = structureLabels, index = datframerows)
materialFrame=pd.DataFrame(materialMatrix, columns = materialsLabels, index = datframerows)

totalframes = [atomisticFrame, weightedAtomFrame, structureFrame, symmetryFrame, materialFrame]

#do data validation
reference = totalframes[0];
for i in range(1,len(totalframes)):
    rpv.compareFeatureSets(reference,totalframes[i])

# Create separate csv files for the structures and for the atomistic

#atomisticMatrix = np.concatenate((atomisticMatrix,np.array(v2).reshape((len(v2),4))), axis = 1)
#BANDGAP IS AN EXCELLENT PREDICTOR!!!!!!!!!!!!!

print('length of labels: '+str(len(labels)));

datframe = pd.concat(totalframes, axis = 1);
datframe.to_csv(settings.DynamicFeatureSets + '\\FeatureSets\AllFeatures.csv');
# scatter_matrix(datframe)

################################### SOME BASIC ANALYSES ##############################################################
#print(datframe)

##Perform data validation

