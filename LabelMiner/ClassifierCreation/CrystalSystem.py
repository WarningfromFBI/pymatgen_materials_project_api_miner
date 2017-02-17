import settings

def CrystalSysClass(structure): #input is the matdata json from the megabase
    data = structure['spacegroup']['crystal_system']
    if(data == 'monoclinic'):
        return 1
    if (data == 'triclinic'):
        return 2
    if (data == 'orthorhombic'):
        return 3
    if (data == 'tetragonal'):
        return 4
    if (data == 'trigonal'):
        return 5
    if (data == 'hexagonal'):
        return 6
    if (data == 'cubic'):
        return 7
    return 0;

def CrystalSysClassFeat(crystalsys): #input is the matdata json from the megabase
    if(crystalsys == 'monoclinic'):
        return 1
    if (crystalsys == 'triclinic'):
        return 2
    if (crystalsys == 'orthorhombic'):
        return 3
    if (crystalsys == 'tetragonal'):
        return 4
    if (crystalsys == 'trigonal'):
        return 5
    if (crystalsys == 'hexagonal'):
        return 6
    if (crystalsys == 'cubic'):
        return 7
    return 0;




