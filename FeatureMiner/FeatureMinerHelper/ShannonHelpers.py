
def isAnion(ShannonDict):
    checker = True;
    for dictionary in ShannonDict:
        if(dictionary['oxidation_num'] < 0):
            continue;
        else:
            checker = False;
            break;
    return checker;

def getIonicRadiusWithCoordination(ShannonDict, coordin_no):
    for dictionary in ShannonDict:
        if(dictionary['coordination_no'] == coordin_no):
            return dictionary['ionic_radius']
    return 0;

def getOxNumbGivenCoordination(ShannonDict, coordin_no):
    for dictionary in ShannonDict:
        if(dictionary['coordination_no'] == coordin_no):
            return dictionary['oxidation_num']
    return 0;

def getIonicRadGivenOx(ShannonDict, ox):
    for dictionary in ShannonDict:
        if(dictionary['oxidation_num'] == ox):
            return dictionary['ionic_radius']
    return 0;

