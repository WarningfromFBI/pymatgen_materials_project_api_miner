import os;
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import *
import sys
from database_reader_functions.AddMPIDToManifest import *
import settings
from database_reader_functions import battery_base_reader as bbr
from database_reader_functions import materials_project_reader as mbf;
from feature_miner_functions import MatDataFeatures as BAF;
'''
mines all of the readily available data in the mp_data files in Materials Project direcotry
note that we have some categorical/non-numeric labels here
'''
plt.close("all")

directory = os.path.join(settings.ROOT_DIR,'Materials_Project_Database');
structureDir = os.path.join(settings.ROOT_DIR, 'structure_database');

testcounter = 0; datframerows = list();
materialMatrix = list();

for filename in os.listdir(directory):

    print('file no. ' + str(testcounter))
    testcounter+=1;
    #if(testcounter>2): break;

    #print(data)
    mpid = filename.strip('.txt')
    try:
        [matdata, structuredata] = mbf.readCompound(filename)
        structureClassUnLith = pickle.load(open(structureDir + '\\' + mpid + '.p', 'rb'));
        ##================STRUCTURAL FEATURE EXTRACTION===============================#

        unitcellMass = BAF.unitCellMass(matdata['unit_cell_formula'])
        atomTypes = BAF.AtomTypeCount(matdata['unit_cell_formula']);
        atomNumLabels = ['atomMean', 'atomStd']
        atomTypesLabel = ['halogen','transition', 'actinoid','chalcogen', 'metalloid', 'rare', 'other', 'alkaline']
        atomNum = BAF.atomicNumber(matdata['unit_cell_formula']);

        #eventually, this requires a conversion into one-hot or some numeric label
        sg = BAF.spacegroup(matdata);
        sg_labels = ['crystal_system', 'structure_number', 'point_group', 'hall'];
        oxide_type = matdata['oxide_type']
        # vanderRad = BAF.vanderWaalRadius(matdata['unit_cell_formula'], matdata['volume']);
        answer = [matdata['density'], matdata['energy_per_atom'], matdata['nsites'],
                               matdata['nelements'], matdata['band_gap'], matdata['volume'], unitcellMass,
                               1/unitcellMass, matdata['energy'],
                               matdata['formation_energy_per_atom'], matdata['total_magnetization'],
                               matdata['e_above_hull']] + list(atomNum) + list(atomTypes)+sg + [oxide_type];
        materialMatrix.append(answer);

        materialsLabels = ['density', 'energy_per_atom', 'nsites', 'nelements', 'bandgap', 'volume',
                           'Unit Cell Mass', 'cap_grav_Li',
                           'energy', 'formationenergy_pa', 'total_magnetization', 'energysStab'] +\
                          atomNumLabels +atomTypesLabel+sg_labels+['oxide_type'];
        datframerows.append(matdata['pretty_formula'] + ', ' + matdata['material_id']);


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        print(exc_type, fname, exc_tb.tb_lineno)

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
datframe.to_csv(os.path.join(settings.ROOT_DIR, 'data_dump', 'mp_MatData_features.csv'));
# scatter_matrix(datframe)


