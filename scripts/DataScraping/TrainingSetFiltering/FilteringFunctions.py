import settings
import pandas as pd
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle
import label_miner_functions.ClassifierCreation.CrystalSystem as cs
import database_reader_functions.MegaBaseReader as MBR;
import database_reader_functions.StructureBaseReader as SBR;
datadir = settings.MinedFeatureSets+'\\VolumeLabels'
labeldir = settings.MinedFeatureSets+'\\FeatureSets'
layeredDir = settings.MaterialsProject+'\\LithiumBatteryCompounds'
layered = pd.read_csv(layeredDir+'\\lithiated_layered.csv')
layeredT = layered.transpose();

def filterByInitialLithium(datadir = 'AllFeatures', Frame = ""):
    [Xdataframe, X] = fle.getFeatures(datadir);
    if(len(Frame) > 0):
        Xdataframe = Frame;

    counter = 0; othercounter = 0;
    featuresT = Xdataframe.transpose();

    filteredFeatures = pd.DataFrame(index = Xdataframe.columns);
    filteredFeatures2 = pd.DataFrame(index = Xdataframe.columns);

    for i in Xdataframe.index:
        labels = str(i).split(',')
        if('Li' in labels[1] and 'Li' in labels[2]):
            #print(labels)
            counter+=1;
            filteredFeatures2[i] = featuresT[i];
        else:
            othercounter+=1;
            filteredFeatures[i] = featuresT[i];

    print(counter)
    print(othercounter)

    datadir = settings.MinedFeatureSets + '\\FilteredDataSets'
    filteredFeatures = filteredFeatures.transpose();
    filteredFeatures2 = filteredFeatures2.transpose();
    filteredFeatures.to_csv(datadir + '\\noLiInitialFeatures.csv')
    filteredFeatures2.to_csv(datadir + '\\LiInitialFeatures.csv')
    print('Done')
    return [filteredFeatures, filteredFeatures2]


def FilterByPreservedCrystalSys(datadir = 'AllFeatures', Frame = ""):
    [Xdataframe, X] = fle.getFeatures(datadir);
    if(len(Frame) > 0):
        Xdataframe = Frame;
    featuresT = Xdataframe.transpose();

    filteredFeatures = pd.DataFrame(index = Xdataframe.columns);
    filteredFeatures2 = pd.DataFrame(index = Xdataframe.columns);
    classifiers = list();
    for i in Xdataframe.index:
        labels = str(i).split(', ')
        unlithiatedmpid = labels[3]; lithiatedmpid = labels[4];
        structureunlith = SBR.readStructure(unlithiatedmpid);
        [matdata, structuredata] = MBR.readCompound(unlithiatedmpid+'.txt');
        [matdatalith, structuredatalith] = MBR.readCompound(lithiatedmpid+'.txt');
        crystalLabel = cs.CrystalSysClass(matdata)
        classifiers.append(crystalLabel);
        if(matdata['spacegroup']['crystal_system'] == matdatalith['spacegroup']['crystal_system']):
            filteredFeatures[i] = (featuresT[i]);
        else:
            filteredFeatures2[i] = (featuresT[i]);

    datadir = settings.MinedFeatureSets + '\\FilteredDataSets'
    filteredFeatures = filteredFeatures.transpose();
    filteredFeatures2 = filteredFeatures2.transpose();
    filteredFeatures.to_csv(datadir + '\\FeaturesNoPhaseChange.csv')
    filteredFeatures2.to_csv(datadir + '\\FeaturesPhaseChange.csv')
    return [filteredFeatures, filteredFeatures2];


def FilterByCrystalSys(crystalsys, datadir = 'AllFeatures', Frame = ""):
    [Xdataframe, X] = fle.getFeatures(datadir);
    if(len(Frame) > 0):
        Xdataframe = Frame;
    featuresT = Xdataframe.transpose();

    filteredFeatures = pd.DataFrame(index = Xdataframe.columns);
    filteredFeatures2 = pd.DataFrame(index = Xdataframe.columns);
    classifiers = list();
    for i in Xdataframe.index:
        labels = str(i).split(', ')
        unlithiatedmpid = labels[3]; lithiatedmpid = labels[4];
        structureunlith = SBR.readStructure(unlithiatedmpid);
        [matdata, structuredata] = MBR.readCompound(unlithiatedmpid+'.txt');
        [matdatalith, structuredatalith] = MBR.readCompound(lithiatedmpid+'.txt');
        crystalLabel = cs.CrystalSysClass(matdata)
        classifiers.append(crystalLabel);
        for sys in crystalsys:
            if (matdata['spacegroup']['crystal_system'] == sys):
                filteredFeatures[i] = (featuresT[i]);
            else:
                filteredFeatures2[i] = (featuresT[i]);

    datadir = settings.MinedFeatureSets + '\\FilteredDataSets'
    filteredFeatures = filteredFeatures.transpose();
    filteredFeatures2 = filteredFeatures2.transpose();
    filteredFeatures.to_csv(datadir + '\\Features'+ 'crystalsys'+'.csv')
    filteredFeatures2.to_csv(datadir + '\\Features'+ 'crystalsys'+'.csv')
    return [filteredFeatures, filteredFeatures2];


def FilterByComplexity( threshold, datadir = 'AllFeatures', Frame = ""):
    [Xdataframe, X] = fle.getFeatures(datadir);
    if(len(Frame) > 0):
        Xdataframe = Frame;
    featuresT = Xdataframe.transpose();

    filteredFeatures = pd.DataFrame(index = Xdataframe.columns);
    filteredFeatures2 = pd.DataFrame(index = Xdataframe.columns);
    classifiers = list();
    for i in Xdataframe.index:
        labels = str(i).split(', ')
        unlithiatedmpid = labels[3]; lithiatedmpid = labels[4];
        structureunlith = SBR.readStructure(unlithiatedmpid);
        [matdata, structuredata] = MBR.readCompound(unlithiatedmpid+'.txt');
        [matdatalith, structuredatalith] = MBR.readCompound(lithiatedmpid+'.txt');
        crystalLabel = cs.CrystalSysClass(matdata)
        classifiers.append(crystalLabel);
        if (len(structureunlith.sites) < threshold):
            filteredFeatures[i] = (featuresT[i]);
        else:
            filteredFeatures2[i] = (featuresT[i]);

    datadir = settings.MinedFeatureSets + '\\FilteredDataSets'
    filteredFeatures = filteredFeatures.transpose();
    filteredFeatures2 = filteredFeatures2.transpose();
    filteredFeatures.to_csv(datadir + '\\Features'+ 'complexity'+'.csv')
    filteredFeatures2.to_csv(datadir + '\\Features'+ 'complexity'+'.csv')
    return [filteredFeatures, filteredFeatures2];


def FilterByLithiumFraction(threshold, datadir = 'AllFeatures', Frame = ""):
    [Xdataframe, X] = fle.getFeatures(datadir);
    if(len(Frame) > 0):
        Xdataframe = Frame;
    featuresT = Xdataframe.transpose();

    filteredFeatures = pd.DataFrame(index = Xdataframe.columns);
    filteredFeatures2 = pd.DataFrame(index = Xdataframe.columns);
    classifiers = list();
    for i in Xdataframe.index:
        labels = str(i).split(', ')
        unlithiatedmpid = labels[3]; lithiatedmpid = labels[4];
        structureunlith = SBR.readStructure(unlithiatedmpid);
        [matdata, structuredata] = MBR.readCompound(unlithiatedmpid+'.txt');
        [matdatalith, structuredatalith] = MBR.readCompound(lithiatedmpid+'.txt');
        crystalLabel = cs.CrystalSysClass(matdata)
        classifiers.append(crystalLabel);
        Lith = matdatalith['unit_cell_formula']['Li']
        if (Lith/matdatalith['nsites'] < threshold):
            filteredFeatures[i] = (featuresT[i]);
        else:
            filteredFeatures2[i] = (featuresT[i]);

    datadir = settings.MinedFeatureSets + '\\FilteredDataSets'
    filteredFeatures = filteredFeatures.transpose();
    filteredFeatures2 = filteredFeatures2.transpose();
    filteredFeatures.to_csv(datadir + '\\Features'+ 'LithFracLow'+'.csv')
    filteredFeatures2.to_csv(datadir + '\\Features'+ 'LithFracHigh'+'.csv')
    return [filteredFeatures, filteredFeatures2];

def FilterByLayer(datadir = 'AllFeatures', Frame = ""):
    [Xdataframe, X] = fle.getFeatures(datadir);
    if(len(Frame) > 0):
        Xdataframe = Frame;
    featuresT = Xdataframe.transpose();

    filteredFeatures = pd.DataFrame(index = Xdataframe.columns);
    filteredFeatures2 = pd.DataFrame(index = Xdataframe.columns);
    classifiers = list();
    for i in Xdataframe.index:
        labels = str(i).split(', ')
        unlithiatedmpid = labels[3]; lithiatedmpid = labels[4];
        check = False;
        for elem in layeredT:
            lith = layeredT[elem][0];
            unlith = layeredT[elem][1];
            if(unlithiatedmpid == unlith and lithiatedmpid ==lith):
                filteredFeatures[i] = featuresT[i];
                check = True;
                break;
        if(not check):
            filteredFeatures2[i] = featuresT[i];

    datadir = settings.MinedFeatureSets + '\\FilteredDataSets'
    filteredFeatures = filteredFeatures.transpose();
    filteredFeatures2 = filteredFeatures2.transpose();
    filteredFeatures.to_csv(datadir + '\\Features'+ 'Layered'+'.csv')
    filteredFeatures2.to_csv(datadir + '\\Features'+ 'UnLayered'+'.csv')
    return [filteredFeatures, filteredFeatures2];

def FilterByNumberInFormula(threshold, datadir = 'AllFeatures', Frame = ""):
    [Xdataframe, X] = fle.getFeatures(datadir);
    if(len(Frame) > 0):
        Xdataframe = Frame;
    featuresT = Xdataframe.transpose();

    filteredFeatures = pd.DataFrame(index = Xdataframe.columns);
    filteredFeatures2 = pd.DataFrame(index = Xdataframe.columns);
    classifiers = list();
    for i in Xdataframe.index:
        labels = str(i).split(', ')
        unlithiatedmpid = labels[3]; lithiatedmpid = labels[4];
        structureunlith = SBR.readStructure(unlithiatedmpid);
        [matdata, structuredata] = MBR.readCompound(unlithiatedmpid+'.txt');
        [matdatalith, structuredatalith] = MBR.readCompound(lithiatedmpid+'.txt');
        crystalLabel = cs.CrystalSysClass(matdata)
        classifiers.append(crystalLabel);
        if (matdata['nsites'] < threshold):
            filteredFeatures[i] = (featuresT[i]);
        else:
            filteredFeatures2[i] = (featuresT[i]);

    datadir = settings.MinedFeatureSets + '\\FilteredDataSets'
    filteredFeatures = filteredFeatures.transpose();
    filteredFeatures2 = filteredFeatures2.transpose();
    filteredFeatures.to_csv(datadir + '\\Features'+ 'Simple'+'.csv')
    filteredFeatures2.to_csv(datadir + '\\Features'+ 'Complex'+'.csv')
    return [filteredFeatures, filteredFeatures2];





