import LabelMiner.LabelMiningHelper.LMHelperFunctions as lmh;
import LabelMiner.LabelMiningHelper.LMHelperPickleStruct as lmp;


def countElementinCell(picklestruct, element):
    counter = 0;
    for sites in picklestruct:
        if(sites.specie.name == element):
            counter+=1;
    return counter;

def generateStatistics(lithstruct, unlithstruct, batterydict):
    redCellAtoms = lmh.reducedCellComposition(batterydict);  # atoms in one unitcell
    NLiLith = lithstruct.composition.get(
        'Li')  # THIS IS WRONG...this gives lithiums in the composition, not the unit cell
    NLiUnLith = unlithstruct.composition.get('Li')

    UnlithTotAtoms = unlithstruct.composition.num_atoms;
    LithTotAtoms = lithstruct.composition.num_atoms;
    nonLiAtoms2 = UnlithTotAtoms - NLiUnLith;
    nonLiAtoms1 = LithTotAtoms - NLiLith;
    vlith = lithstruct.volume;
    vunlith = unlithstruct.volume;
    formulaUnits1 = nonLiAtoms2 / redCellAtoms;  # lunithiated
    formulaUnits2 = nonLiAtoms1 / redCellAtoms;  # lithiated
    nDischarge = batterydict['fracA_discharge'];
    nCharge = batterydict['fracA_charge']
    NLiLithProp = NLiLith / formulaUnits2;
    NLiUnLithProp = NLiUnLith / formulaUnits1;
    lithweight = lithstruct.composition.weight * formulaUnits2;
    unlithweight = unlithstruct.composition.weight * formulaUnits1;
    LionConc = NLiLith / (vlith);
    formulaUnitConc = formulaUnits1 / vlith
    LiVolFracLith = lmp.getLiVolumeFraction(lithstruct);
    LiVolFracUnlith = lmp.getLiVolumeFraction(unlithstruct);



