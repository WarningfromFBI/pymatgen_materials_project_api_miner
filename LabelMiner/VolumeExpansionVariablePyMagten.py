import os;
import pickle
import sys;

import pymatgen as mg

import LabelMiner.LabelMiningHelper.LMHelperFunctions as lmh
import LabelMiner.LabelMiningHelper.LMHelperPickleStruct as lmp
import MaterialsProjectReader.MegaBaseReader as mbf
import settings

## IMPORTANT NOTE
# DISCHARGE = LITHIATED
# CHARGE = UNLITHIATED
#DeltaVolNormFormula Units not quite right,
#(vilith-viunlith)/(deltaformulaunits)

def volumeLabels(batterydict, lithstruct, unlithstruct):
    dV = batterydict['max_delta_volume']
    id_discharge = batterydict['id_discharge'];
    id_charge = batterydict['id_charge'];

    ## STILL NEED THE STRUCTURE DATA
    lithcomp = mg.Composition(batterydict['formula_discharge']);
    unlithcomp = mg.Composition(batterydict['formula_charge']);


    redCellAtoms = lmh.reducedCellComposition(batterydict); #atoms in one unitcell
    NLiLith = lithstruct.composition.get('Li') #THIS IS WRONG...this gives lithiums in the composition, not the unit cell
    NLiUnLith = unlithstruct.composition.get('Li')

    UnlithTotAtoms = unlithstruct.composition.num_atoms;
    LithTotAtoms = lithstruct.composition.num_atoms;
    nonLiAtoms2 =  UnlithTotAtoms- NLiUnLith;  nonLiAtoms1 =  LithTotAtoms- NLiLith;
    vlith = lithstruct.volume ; vunlith = unlithstruct.volume;
    formulaUnits1 = nonLiAtoms2 / redCellAtoms;  # lunithiated
    formulaUnits2 = nonLiAtoms1 / redCellAtoms;  # lithiated
    nDischarge = batterydict['fracA_discharge']; nCharge = batterydict['fracA_charge']
    NLiLithProp = NLiLith / formulaUnits2;
    NLiUnLithProp = NLiUnLith / formulaUnits1;
    lithweight = lithstruct.composition.weight;
    unlithweight = unlithstruct.composition.weight;
    LithiumAW = 6.941;
    LionConc = NLiLith/(vlith); formulaUnitConc = formulaUnits1/vlith
    LiVolFracLith = lmp.getLiVolumeFraction(lithstruct);
    LiVolFracUnlith = lmp.getLiVolumeFraction(unlithstruct);
    #volume weighted fraction

    print('\nvlith: '+str(vlith)+', vunlith: '+str(vunlith));
    print('LithiumLith: ' + str(NLiLith) + ', LithiumUnlith: ' + str(NLiUnLith))
    print('chemformulas: ' + batterydict['formula_discharge'] + ', ' + batterydict['formula_charge'])
    print('formulaUnits1: ' + str(formulaUnits1) + ", formulaUnits2: " + str(formulaUnits2))
    #print('nDischarge: '+str(nDischarge)+', '+str(NLiLith/LithTotAtoms)); #just a basic check

    dVsign = (vlith/formulaUnits2 - vunlith/formulaUnits1) / (vunlith/formulaUnits1);
    dVunNorm = (vlith-vunlith)/vunlith;
    dVpermass = (vlith/lithweight - vunlith/unlithweight)/(vunlith/unlithweight);

    #Accumulate proposed volume features
    volLabelDict = dict();

    volLabelDict['dVnormLiPerFormulaUnit'] = dV / (NLiLithProp - NLiUnLithProp); #<- expansion per formula unit upon inserting 1 lithium atom
    volLabelDict['dVnormLiPerFormulaUnit2'] = dVsign / (NLiLithProp - NLiUnLithProp); #GOOD
    #volLabelDict['dVnormNumDens'] = dVunNorm / (NLiLith/vlith - NLiUnLith/vunlith); #IFFY
    #volLabelDict['dVnormNumDensnorPerFormulaUnit'] = dVunNorm / ((NLiLith/vlith)*NLiLithProp - (NLiUnLith/vunlith)*NLiUnLithProp);  ##Measure #3

    volLabelDict['VnormLiFrac'] = (vlith*nDischarge - vunlith*nCharge)/(vlith*nDischarge) #BEST FITTED LABEL
    #volLabelDict['VnormLiFormFrac'] = (vlith*NLiLithProp - vunlith*NLiUnLithProp)/(vlith*NLiLithProp) #this is trivial...model can differentiate between compounds with lithium
    #and compounds without it (unintercalated version), which is to say, I can just do this by looking at the formulas
    volLabelDict['dVperAtom'] = ((vlith/LithTotAtoms - vunlith/UnlithTotAtoms) / (vunlith/UnlithTotAtoms))/(NLiLith/LithTotAtoms-NLiUnLith/UnlithTotAtoms); #GOOD
   # volLabelDict['dVperLiVolumeWeighted'] = (vlith/LiVolFracLith - vunlith/LiVolFracUnlith) / (NLiLith/LiVolFracLith - NLiUnLith/LiVolFracUnlith);
    volLabelDict['dVraw'] =  dVsign
    volLabelDict['dVraw2'] = dVunNorm
    volLabelDict['dVraw3'] = dVpermass;
    #volLabelDict['dVperAtom2'] = dVperAtom / (nDischarge - nCharge)
    volLabelDict['dVoriginal'] = dV; #this is not sign sensitive
    #volLabelDict['VoverLi'] = (vlith - vunlith) / (NLiLith - NLiUnLith);

    #everything here is normalized by the volume...the unit is mass
    volLabelDict['dVdensity'] = (lithweight/vlith - unlithweight/vunlith)/(unlithweight/vunlith)/ (NLiLith/vlith - NLiUnLith/vunlith)
    #this is basically the inverse of density
    volLabelDict['dVweight'] = dVpermass/(NLiLith/lithweight - NLiUnLith/unlithweight); #REALLY GOOD
    volLabelDict['dvnormweight'] = dVpermass/(lithweight-unlithweight);
    volLabelDict['dvnormweight2'] = dVpermass/(LithiumAW*(NLiLith-NLiUnLith))
    return volLabelDict;  # THIS SHOULD PRODUCE SAME RESULT
    # AS BATTERY EXPLORER DATA




# ================ This is good as number density is intensive ==================
def fractionLabels(batterydict):
    #count Li Ions in charged and discharged formulas
    #get volumes of charged and dicharged
    id_discharge = batterydict['id_discharge'];
    id_charge = batterydict['id_charge'];
    search1 = id_discharge + '.txt';  # lithiated
    search2 = id_charge + '.txt';  # unlithiated

    redCellAtoms = lmh.reducedCellComposition(batterydict);

    try:
        fracLabels = dict();
        DataLith = mbf.readCompound(search1);
        DataUnlith = mbf.readCompound(search2);
        vlith = DataLith[0]['volume'];
        vunlith = DataUnlith[0]['volume'];
        NLiLith = lmh.countLiInStructure(DataLith[1]['sites'])
        NLiUnLith = lmh.countLiInStructure(DataUnlith[1]['sites'])
        nonLiAtoms2 = lmh.AtomsPerUnitCell(batterydict['id_charge']) - NLiUnLith;
        nonLiAtoms1 = lmh.AtomsPerUnitCell(batterydict['id_discharge']) - NLiLith;
        formulaUnits1 = nonLiAtoms2 / redCellAtoms;  # lunithiated
        formulaUnits2 = nonLiAtoms1 / redCellAtoms;  # lithiated
        NLiLithProp = NLiLith / formulaUnits2;
        NLiUnLithProp = NLiUnLith / formulaUnits1;
        fracLabels['dN'] = (NLiUnLith/vunlith) - (NLiLith/vlith);
        fracLabels['LiProp'] = NLiLithProp - NLiUnLithProp
        return fracLabels #change in the number Li atoms per volume
    except Exception as e:
        print(e)
        return 0;






