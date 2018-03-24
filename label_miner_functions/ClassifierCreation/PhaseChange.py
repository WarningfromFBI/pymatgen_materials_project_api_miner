import database_reader_functions.StructureBaseReader as SBR
import database_reader_functions.MegaBaseReader as MBR
import label_miner_functions.ClassifierCreation.CrystalSystem as cs


def PhaseChange(volumeLabels):
    classifiers = list(); crystalSysLabel = list();
    for i in volumeLabels.index:
        labels = str(i).split(', ')
        unlithiatedmpid = labels[3];
        lithiatedmpid = labels[4];
        structureunlith = SBR.readStructure(unlithiatedmpid);
        [matdata, structuredata] = MBR.readCompound(unlithiatedmpid + '.txt');
        [matdatalith, structuredatalith] = MBR.readCompound(lithiatedmpid + '.txt');
        crystalLabel = cs.CrystalSysClass(matdata)
        crystalSysLabel.append(crystalLabel);
        if (matdata['spacegroup']['crystal_system'] == matdatalith['spacegroup']['crystal_system']):
            classifiers.append(1);
        else:
            classifiers.append(0);

    return classifiers;
