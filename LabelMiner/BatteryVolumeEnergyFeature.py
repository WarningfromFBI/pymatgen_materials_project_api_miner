import LabelMiner.LabelMiningHelper.LMHelperFunctions as lmh

def deltaVolNormCapacity(batterydict, lith, unlith,lithstruct, unlithstruct): #YIELDS 0.3 max correlation coefficient
    dV = batterydict['max_delta_volume']
    volDict = dict();
    voltCap = batterydict['average_voltage'];

    id_discharge = batterydict['id_discharge'];
    id_charge = batterydict['id_charge'];



    redCellAtoms = lmh.reducedCellComposition(batterydict);  # atoms in one unitcell
    DataLith = lith;
    DataUnlith = unlith;
    NLiLith = lmh.countLiInStructure(DataLith[1]['sites'])
    NLiUnLith = lmh.countLiInStructure(DataUnlith[1]['sites'])
    Atoms2 = lmh.AtomsPerUnitCell(batterydict['id_charge'])
    Atoms1 = lmh.AtomsPerUnitCell(batterydict['id_discharge'])
    nonLiAtoms2 = Atoms2 - NLiUnLith;
    nonLiAtoms1 = Atoms1 - NLiLith;
    formulaUnits1 = nonLiAtoms2 / redCellAtoms;  # lunithiated
    formulaUnits2 = nonLiAtoms1 / redCellAtoms;  # lithiated
    lithweight = lithstruct.composition.weight * formulaUnits2;
    unlithweight = unlithstruct.composition.weight * formulaUnits1;
    NLiLithProp = NLiLith / formulaUnits2;
    NLiUnLithProp = NLiUnLith / formulaUnits1;
    vlith = DataLith[0]['volume'];
    vunlith = DataUnlith[0]['volume'];
    dVsign = (vlith / formulaUnits2 - vunlith / formulaUnits1) / (vunlith / formulaUnits1);
    dVunNorm = (vlith - vunlith) / vunlith;
    dVperAtom = (vlith / Atoms1 - vunlith / Atoms2) / (vunlith / Atoms2)
    dvpermass = (vlith/lithweight - vunlith/unlithweight)/(vunlith/unlithweight);

    #THESE DON'T REALLY MAKE SENSE....
    # volDict['avgVolt'] = dV / voltCap;
    # volDict['volumetricCap'] = dV / batterydict['capacity_vol']
    # volDict['gravCap'] = dV / batterydict['capacity_grav']
    # volDict['energy_grav'] = dV / batterydict['energy_grav']
    # volDict['energy_vol'] = dV / batterydict['energy_vol']
    volDict['avgVolt2'] = dVsign / voltCap;
    volDict['volumetricCap2'] = dVsign / ((NLiLithProp - NLiUnLithProp)*batterydict['capacity_vol'])
    volDict['gravCap2'] = dVsign / ((NLiLithProp - NLiUnLithProp)*batterydict['capacity_grav'])
    volDict['energy_grav2'] = dVsign / ((NLiLithProp - NLiUnLithProp)*batterydict['energy_grav'])
    volDict['energy_vol2'] = dVsign / ((NLiLithProp - NLiUnLithProp)*batterydict['energy_vol'])
    volDict['avgVolt3'] = dVsign / voltCap;
    volDict['volumetricCap3'] = dVsign / ( batterydict['capacity_vol'])
    volDict['gravCap3'] = dVsign / (batterydict['capacity_grav'])
    volDict['energy_grav3'] = dVsign / ( batterydict['energy_grav'])
    volDict['energy_vol3'] = dVsign / (batterydict['energy_vol'])
    volDict['avgVolt4'] = dvpermass / voltCap;
    volDict['volumetricCap4'] = dvpermass / (batterydict['capacity_vol'])
    volDict['gravCap4'] = dvpermass / (batterydict['capacity_grav'])
    volDict['energy_grav4'] = dvpermass / (batterydict['energy_grav'])
    volDict['energy_vol4'] = dvpermass / (batterydict['energy_vol'])
    return volDict;




