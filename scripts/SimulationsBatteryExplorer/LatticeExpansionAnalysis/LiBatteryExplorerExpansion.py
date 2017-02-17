import json
import os

import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sympy import *

import LabelMiner.LabelMiningHelper.VolumeStatisticsCalculator as cesl
import MaterialsProjectReader.StructureBaseReader as SBR
import settings


def reducedCell(batterydict):
    red_cell_comp = batterydict['framework']['reduced_cell_composition'];
    redCellAtoms = 0;
    for i in red_cell_comp.keys():
        redCellAtoms += red_cell_comp[i];
    return redCellAtoms;

# Script to assess the extent of battery expansion within a specific family of compounds
directory2 = settings.MaterialsProject + '\\LithiumBatteryExplorer';
plt.figure();
superFamilyBatteries = list(); maxVolumes = list();
counter = 0;
for filename in os.listdir(directory2):
    file = open(directory2+"\\"+filename, 'r')
    data = "";
    for line in file:
        data = json.loads(line);
    volumeChange = [0]
    fracLithium = [0];
    print(data['reduced_cell_formula'])
    for i in range(len(data['adj_pairs'])):
        try:
            redCellAtoms = reducedCell(data['adj_pairs'][i])
            #print(str(data['reduced_cell_formula']+" "+str(redCellAtoms)))
            unlithiated = data['adj_pairs'][i]['id_discharge']
            lithiated = data['adj_pairs'][i]['id_charge']
            lithstruct = SBR.readStructure(lithiated);
            unlithstruct = SBR.readStructure(unlithiated)

            NLiLith = cesl.countElementinCell(lithstruct, 'Li')  # THIS IS WRONG...this gives lithiums in the composition, not the unit cell
            NLiUnLith = cesl.countElementinCell(unlithstruct, 'Li')
            print('Nlith: '+str(NLiLith)+", Nunlith: "+str(NLiUnLith))
            UnlithTotAtoms = unlithstruct.composition.num_atoms;
            LithTotAtoms = lithstruct.composition.num_atoms;
            nonLiAtoms2 = UnlithTotAtoms - NLiUnLith;
            nonLiAtoms1 = LithTotAtoms - NLiLith;
            vlith = lithstruct.volume;
            vunlith = unlithstruct.volume;
            formulaUnits1 = nonLiAtoms2 / redCellAtoms;  # lunithiated
            formulaUnits2 = nonLiAtoms1 / redCellAtoms;  # lithiated
            nDischarge = data['adj_pairs'][i]['fracA_discharge'];
            nCharge = data['adj_pairs'][i]['fracA_charge']
            NLiLithProp = NLiLith / formulaUnits2;
            NLiUnLithProp = NLiUnLith / formulaUnits1;
            print('proportions: '+str(NLiLithProp)+" "+str(NLiUnLithProp))
            dVSign = ((vlith/formulaUnits2 - vunlith/formulaUnits1)/(vunlith/formulaUnits1))
            if ((data['adj_pairs'][i]['framework']['nelements']) <=1):
                print((data['adj_pairs'][i]['formula_discharge']))

            if(data['adj_pairs'][i]['max_delta_volume'] == 0):
                print(data['battid']);
                continue;
            volumeChange.append(dVSign)
            fracLithium.append(nDischarge-nCharge);

        except Exception as e:
            print(e);
            continue;
    if(len(volumeChange) > 3):
        plt.figure()
        plt.scatter(fracLithium, volumeChange, s = 200)
        plt.xlabel('fraction of lithium')
        plt.ylabel('change in volume')
        plt.title('volume change plots for '+str(data['reduced_cell_formula']))
        # Calculate Initial Slope with linear regression
        X = np.array(fracLithium);
        y = np.array(volumeChange)
        X = np.reshape(X, (len(X), 1));
        y = np.reshape(y, (len(y), 1))
        clf = linear_model.LinearRegression();
        clf.fit(X[:2], y[:2])
        print('expansion slope: ' + str(clf.coef_))
        plt.plot(X, clf.predict(X), '-')

        plt.show()







