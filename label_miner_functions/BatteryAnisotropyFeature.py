import numpy as np

#Anisotropy is in the literature, generally defined as differences in linear density along different
#directions

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
    vlith = structureLith.volume; cubescalelith = vlith**(1/3);
    vunlith = structureUnLith.volume; cubescaleunlith = vunlith**(1/3);
    redCellAtoms = structureLith.composition.reduced_composition._natoms
    formulaUnits1 = nonLiAtoms2 / redCellAtoms;  # lunithiated
    formulaUnits2 = nonLiAtoms1 / redCellAtoms;  # lithiated

    NLiLithProp = NLiLith / formulaUnits2;  NLiUnLithProp = NLiUnLith / formulaUnits1;

    xunlith = latticeUnLith.a;  xlith = latticeLith.a;
    yunlith = latticeUnLith.b; ylith = latticeLith.b;
    zunlith = latticeUnLith.c; zlith = latticeLith.c;
    rlith = [xlith, ylith, zlith]; runlith = [xunlith, yunlith, zunlith];
    lithDistFromIso = [x - cubescalelith for x in rlith];
    unlithDistFromIso = [x - cubescaleunlith for x in runlith];
    AnisotropyVec = [(x - y) for x,y in zip(lithDistFromIso, unlithDistFromIso)];

    #change in lithium proportion
    #Normalize the change based on the amount of Li that has been inserted into the lattice
    deltaLith = NLiLith; deltaProp = NLiLithProp-NLiUnLithProp;

    ##ratios calculation:
    ratios = list();
    ratios.append((xlith/ylith - xunlith/yunlith)/deltaProp);
    ratios.append((xlith/xunlith - zlith/zunlith)/deltaProp);
    ratios.append((ylith/yunlith - zlith/zunlith)/deltaProp);

    anisotropyLabelDict['Range Anisotropy'] = np.max(AnisotropyVec)-np.min(AnisotropyVec);
    anisotropyLabelDict['Std Anisotropy'] = np.std((AnisotropyVec));
    anisotropyLabelDict['Anisotropy Ratio Range'] = np.max(ratios)-np.min(ratios);
    anisotropyLabelDict['Anisotropy Ratio Std'] = np.std((ratios))

    return anisotropyLabelDict;

def getDeltaAngle(latticeLith, latticeUnlith):
    return None;

