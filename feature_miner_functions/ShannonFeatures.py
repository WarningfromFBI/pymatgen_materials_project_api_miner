import pymatgen as mg
import numpy as np
from sympy import *
import settings
import json
import feature_miner_functions.FeatureMinerHelper.CalculationHelpers as ch
import feature_miner_functions.FeatureMinerHelper.ShannonHelpers as sh
import copy
import pymatgen.analysis.bond_valence as pabv;
import pymatgen.symmetry.analyzer as psa
import pymatgen.analysis.defects.point_defects as pdf
import os
## THIS IS STILL UNDER DEVELOPMENT AS THERE ARE AMBIGUITIES ABOUT OXIDATION NUMBER FOR
## CERTAIN COMPOUNDS

structureDir = os.path.join(settings.ROOT_DIR, 'structure_database');
ShannonBase = os.path.join(settings.ROOT_DIR, 'Shannon_Radii');
ShannonData = json.load(open(os.path.join(ShannonBase,'ShannonRadiiDictionary.json'), 'r'));

#Li always has a +1 oxidation state in an atom, which means upon lithiation, materials should reduce
#their oxidation state... get a sense of how willing the constituents are to decrease their oxidation state
def oxidationStateFlexibility(picklestruct):
    #if we normalize against the cell volume, it gives a sense of what the oxidation difference can do per unit volume
    #at the same time, the unnormalized version of this data is already a top feature
    initialvol = picklestruct.volume
    diffs = list();
    for site in picklestruct.sites:
        minox = site.specie.min_oxidation_state
        maxox = site.specie.max_oxidation_state;
        diff = maxox-minox; diffs.append(diff);
    return [np.mean(diffs)/(len(picklestruct.sites)), np.std(diffs)/(len(picklestruct.sites)),
            np.max(diffs)/(len(picklestruct.sites)), np.min(diffs)/(len(picklestruct.sites))];

def oxidationStateVolumeFlexibility(pickleStruct):
    #how much does atomic volume change when charge state changes
    #we can use physical volumes as we normalize to teh volume of the unit cell
    volume = pickleStruct.volume;
    VolChange = 0;
    for site in pickleStruct.sites:
        elem = site.specie.value;
        ShannonPoint = ShannonData[elem]
        maxrad = 0; minrad = float('inf');
        for i in ShannonPoint:
            rad = i['ionic_radius'];
            if(rad > maxrad):
                maxrad = rad;
            if(rad<minrad):
                minrad = rad;
        volDiff = ch.sphereVol(maxrad)-ch.sphereVol(minrad);
    VolChange += volDiff;
    return VolChange/volume; #does this need a normalization to the unit cell?

def VolumeByAvgIonicRadius(pickleStruct):
    volume = pickleStruct.volume;
    Vtot = 0;
    for site in pickleStruct.sites:
        elem = site.specie;
        avgionicrad = elem.average_ionic_radius
        Vtot += ch.sphereVol(avgionicrad);
    return (volume - Vtot)/volume;

#SHANNON RADII MINING...all features should be normalized so they can be comparable between compounds
def VolumeByShannonRadii(pickleStruct):
    volume = pickleStruct.volume;
    picklestruct = pdf.ValenceIonicRadiusEvaluator(pickleStruct); #this automatically attempts to assign valences
    Vtot = 0;
    for ionicRadii in picklestruct._get_ionic_radii():
        v = ch.sphereVol(ionicRadii);
        Vtot += v;
    return (volume - Vtot)/volume;

def VolumeFlexibilityByShannonRadii(pickleStruct): #change in volume when anion charge state is modified
    startVol = VolumeByShannonRadii(pickleStruct);
    TotDeltaVol = 0;
    for site in pickleStruct.sites:
        elem = site.specie.value;
        coordin_no = site.coordination_no;
        ShannonPoint = ShannonData[elem];
        deltaVol = 0;
        if(sh.isAnion(ShannonPoint) == True):
            originalRad = sh.getIonicRadiusWithCoordination(ShannonPoint, coordin_no);
            originalOx = sh.getOxNumbGivenCoordination(ShannonPoint, coordin_no);
            newRad = sh.getIonicRadGivenOx(ShannonPoint, originalOx - 1);
            if(newRad == None):
                newRad = originalRad
            deltaVol = ch.sphereVol(originalRad) - ch.sphereVol(newRad);
        TotDeltaVol+=deltaVol
    return TotDeltaVol/startVol;

def ShannonRatio(picklestruct):
    rads = list();
    valence = pdf.ValenceIonicRadiusEvaluator(picklestruct); #this automatically attempts to assign valences
    picklestruct = valence.structure;
    for site in picklestruct:
        oxi_state = np.mean(site.specie.common_oxidation_states);
        rad = site.specie.average_ionic_radius; 
        ratio = oxi_state/rad;
        rads.append(ratio)
    return [np.mean(rads), np.std(rads)]

def deltaShannonRadii(pickleStruct): #We need the shannon dictoinary as the pymatgen valence can't gauge 'maximal differences'
    initialVol = pickleStruct.volume;
    deltaVolList = list();
    for site in pickleStruct.sites:
        elem = site.specie.value;
        ShannonPoint = ShannonData[elem];
        maxSeen = 0; minSeen = float('Inf');
        for dictionary in ShannonPoint:
            rad = dictionary['ionic_radius'];
            if(rad > maxSeen): maxSeen = rad;
            if(rad < minSeen): minSeen = rad;
        deltaVol = ch.sphereVol(maxSeen) - ch.sphereVol(minSeen);
        deltaVolList.append(deltaVol);
    return [np.mean(deltaVolList), np.std(deltaVolList), np.min(deltaVolList), np.max(deltaVolList)]/(initialVol)**(1/3);

def deltaShannonCrystalRadii(pickleStruct):
    initialVol = pickleStruct.volume;
    deltaVolList = list();
    for site in pickleStruct.sites:
        elem = site.specie.value;
        ShannonPoint = ShannonData[elem];
        maxSeen = 0; minSeen = float('Inf');
        for dictionary in ShannonPoint:
            rad = dictionary['crystal_radius'];
            if(rad > maxSeen): maxSeen = rad;
            if(rad < minSeen): minSeen = rad;
        deltaVol = ch.sphereVol(maxSeen) - ch.sphereVol(minSeen);
        deltaVolList.append(deltaVol);
    return [np.mean(deltaVolList), np.std(deltaVolList), np.min(deltaVolList), np.max(deltaVolList)]/(initialVol)**(1/3);


def CellOxidationStateDensity(pickleStruct): #normalize against the total number of elements...
    numElements = len(pickleStruct.sites); initialVol = pickleStruct.volume;
    negativeOxPop = 0; positiveOxPop = 0;
    valence = pdf.ValenceIonicRadiusEvaluator(pickleStruct); #this automatically attempts to assign valences
    for site in valence.structure.sites:
        oxistate = site.specie.min_oxidation_state  # this is the charge
        if(oxistate < 0):
            negativeOxPop+=1;
        if(site.specie.max_oxidation_state > 0):
            positiveOxPop+=1;
    return [positiveOxPop/initialVol, negativeOxPop/initialVol]; #the stoich fraction is 100% correlated to the positiveox fraction.

##=================FUNCTION TO APPLY ALL THESE FUNCTIONS AT ONCE ==============================#


def GetAllShannonFeatures(picklestruct):

    [a1, b1, c1, d1] = oxidationStateFlexibility(picklestruct);
    a2 = VolumeByShannonRadii(picklestruct);
    [a3,b3] = CellOxidationStateDensity(picklestruct)
    a4 = VolumeByAvgIonicRadius(picklestruct)
    a5 = oxidationStateVolumeFlexibility(picklestruct)
    a6 = ShannonRatio(picklestruct);
    a7 = VolumeFlexibilityByShannonRadii(picklestruct)

    data = [a1, b1, c1, d1, a2, a3, b3, a4, a5, a6, a7];
    labels = ['oxflexy1', 'oxflex2', 'oxflex3', 'oxflex4', 'shannondeltavol', 'positiveox1', 'positiveox2',
              'avgionicrad', 'volume flex', 'ShannonRat2', 'vflexshanrad2'];
    return [data, labels]







