import numpy as np


#Anisotropy sensitive feaures, this is for volume expansion
#get change in the unit cell sizes

def getDeltaR(structureLith, structureUnLith):
    #the inputs are the structure elements for the lithmpid, unlithmpid
    anisotropyLabelDict = dict();
    latticeLith = structureLith.lattice;
    latticeUnLith = structureUnLith.lattice;
    NLiLith = structureLith.composition.get('Li')
    NLiUnLith = structureUnLith.composition.get('Li')

    Atoms2 = structureUnLith.composition._natoms
    Atoms1 = structureLith.composition._natoms
    nonLiAtoms2 = Atoms2 - NLiUnLith;
    nonLiAtoms1 = Atoms1 - NLiLith;
    # vlith = structureLith.volume;
    # vunlith = structureUnLith.volume;
    redCellAtoms = structureLith.composition.reduced_composition._natoms
    validcell = structureUnLith.composition.reduced_composition._natoms;
    formulaUnits1 = nonLiAtoms2 / redCellAtoms;  # lunithiated
    formulaUnits2 = nonLiAtoms1 / redCellAtoms;  # lithiated

    NLiLithProp = NLiLith / formulaUnits2;
    NLiUnLithProp = NLiUnLith / formulaUnits1;

    xcent = latticeLith.a
    ycent = latticeLith.b
    zcent = latticeLith.c

    xlith = latticeUnLith.a;
    ylith = latticeUnLith.b;
    zlith = latticeUnLith.c;

    #change in lithium proportion

    #Normalize the change based on the amount of Li that has been inserted into the lattice
    deltaLith = NLiLith; deltaProp = NLiLithProp-NLiUnLithProp;
    deltax = (xlith-xcent)/deltaLith;
    deltay = (ylith-ycent)/deltaLith;
    deltaz = (zlith-zcent)/deltaLith;
    deltax2 = (xlith - xcent) / deltaProp ;
    deltay2 = (ylith - ycent) / deltaProp;
    deltaz2 = (zlith - zcent) / deltaProp;
    anisVec = [deltax, deltay, deltaz];
    anisotropyMean = (deltax + deltay + deltaz)/3

    anisotropyLabelDict['deltax'] = deltax;
    anisotropyLabelDict['deltay'] = deltay;
    anisotropyLabelDict['deltaz'] = deltaz;
    anisotropyLabelDict['deltax2'] = deltax2;
    anisotropyLabelDict['deltay2'] = deltay2;
    anisotropyLabelDict['deltaz2'] = deltaz2;
    anisotropyLabelDict['anisotropyMean'] = anisotropyMean;
    anisotropyLabelDict['max Anisotropy'] = np.max(anisVec);

    return anisotropyLabelDict;

def getDeltaAngle(latticeLith, latticeUnlith):
    return None;

