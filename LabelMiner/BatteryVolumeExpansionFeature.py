import os;
import sys;

import LabelMiner.LabelMiningHelper.LMHelperFunctions as lmh
import MaterialsProjectReader.MegaBaseReader as mbf
## IMPORTANT NOTE
# DISCHARGE = LITHIATED
# CHARGE = UNLITHIATED

#DeltaVolNormFormula Units not quite right,
#(vilith-viunlith)/(deltaformulaunits)

def volumeLabels(batterydict):
    dV = batterydict['max_delta_volume']
    id_discharge = batterydict['id_discharge'];
    id_charge = batterydict['id_charge'];
    # get reduced cell composition

    search1 = id_discharge + '.txt';  # lithiated
    search2 = id_charge + '.txt';  # unlithiated
    try:
        redCellAtoms = lmh.reducedCellComposition(batterydict); #atoms in one unitcell
        DataLith = mbf.readCompound(search1);   DataUnlith = mbf.readCompound(search2);
        NLiLith = lmh.countLiInStructure(DataLith[1]['sites'])
        NLiUnLith = lmh.countLiInStructure(DataUnlith[1]['sites'])
        Atoms2 = lmh.AtomsPerUnitCell(batterydict['id_charge'])
        Atoms1 = lmh.AtomsPerUnitCell(batterydict['id_discharge'])
        nonLiAtoms2 =  Atoms2- NLiUnLith;  nonLiAtoms1 =  Atoms1- NLiLith;
        vlith = DataLith[0]['volume']; vunlith = DataUnlith[0]['volume'];
        formulaUnits1 = nonLiAtoms2 / redCellAtoms;  # lunithiated
        formulaUnits2 = nonLiAtoms1 / redCellAtoms;  # lithiated
        nDischarge = batterydict['fracA_discharge']; nCharge = batterydict['fracA_charge']
        NLiLithProp = NLiLith / formulaUnits2;
        NLiUnLithProp = NLiUnLith / formulaUnits1;
        LionConc = NLiLith/(vlith); formulaUnitConc = formulaUnits1/vlith
        print('\n')
        print('vlith: '+str(vlith)+', vunlith: '+str(vunlith));
        print('LithiumLith: ' + str(NLiLith) + ', LithiumUnlith: ' + str(NLiUnLith))
        print('chemformulas: ' + batterydict['formula_discharge'] + ', ' + batterydict['formula_charge'])
        print('formulaUnits1: ' + str(formulaUnits1) + ", formulaUnits2: " + str(formulaUnits2))
        #print('nDischarge: '+str(nDischarge)+', '+str(NLiLith/Atoms1)); #just a basic check
        dVsign = (vlith/formulaUnits2 - vunlith/formulaUnits1) / (vunlith/formulaUnits1);
        dVunNorm = (vlith-vunlith)/vunlith;
        dVperAtom = (vlith/Atoms1 - vunlith/Atoms2) / (vunlith/Atoms2);
        #Accumulate proposed volume features
        volLabelDict = dict();

        volLabelDict['dVnormLiPerFormulaUnit'] = dV / (NLiLithProp - NLiUnLithProp); #<- expansion per formula unit upon inserting 1 lithium atom
        volLabelDict['dVnormNumDens'] = dVunNorm / (NLiLith/vlith - NLiUnLith/vunlith); #IFFY
        volLabelDict['dVnormNumDensnorPerFormulaUnit'] = dVunNorm / ((NLiLith/vlith)*NLiLithProp - (NLiUnLith/vunlith)*NLiUnLithProp);  ##Measure #3

        volLabelDict['VnormLiFrac'] = (vlith*nDischarge - vunlith*nCharge)/(vlith*nDischarge) #BEST FITTED LABEL
        #and compounds without it (unintercalated version), which is to say, I can just do this by looking at the formulas
        volLabelDict['dVperAtom'] = ((vlith/Atoms1 - vunlith/Atoms2) / (vunlith/Atoms2))/(NLiLith/Atoms1-NLiUnLith/Atoms2); #GOOD
        volLabelDict['dVraw'] = (vlith/formulaUnits2 - vunlith/formulaUnits1) / (vunlith/formulaUnits1); #this is SIGN SENSITIVE
        volLabelDict['VoverLi'] = (vlith-vunlith)/(NLiLith-NLiUnLith);
        #volLabelDict['dVperAtom2'] = dVperAtom / (nDischarge - nCharge)
        volLabelDict['dVnormLiPerFormulaUnit2'] = dVsign / (NLiLithProp - NLiUnLithProp); #GOOD
        volLabelDict['dVoriginal'] = dV; #this is not sign sensitive
        volLabelDict['dVraw2'] = (vlith-vunlith)/vunlith #this should be the worst
        return volLabelDict;  # THIS SHOULD PRODUCE SAME RESULT
        # AS BATTERY EXPLORER DATA

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return -1;


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






