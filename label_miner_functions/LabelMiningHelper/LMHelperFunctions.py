import re as r

import database_reader_functions.materials_project_reader as mbf


###################=========AUXILIARY FUNCTIONS=============#########################
def LiInFormulaCounter(chemformula):
    Lindex = chemformula.find('Li');
    if(Lindex == -1):
        return 0;
    endstrip = 2;
    # print(Lindex);
    count = '';
    while (Lindex + endstrip < len(chemformula) and chemformula[Lindex + endstrip].isdigit()):
        count += chemformula[Lindex + endstrip];
        #print(endstrip)
        endstrip += 1;
    if(count == ''):
        count = '1';
    return int(count);

def countUnlithiatedUnits(batterydict, chemformula): #We need the battery framework, as this provides the fundamental unit cell of
    framework = batterydict['framework'];
    reduced_cell_comp = framework['reduced_cell_composition'];
    formulaMult = 0; unitcellMult = 0;
    compoundParsed = compoundParser(chemformula);
    for i in compoundParsed:
        if(i[0]=='Li'):
            continue;
        unitcellMult+=i[1];
    for i in reduced_cell_comp:
        formulaMult+=reduced_cell_comp[i];
    normalization = unitcellMult/formulaMult;
    return normalization;

def AtomsPerUnitCell(mpid): #returns total # of Atoms in a Unit Cell
    file = mpid+'.txt';
    try:
        [matdata, datstruct] = mbf.readCompound(file);

        if(len(datstruct) != 0):
            formulaMult = len(datstruct['sites'])
            return formulaMult;
    except Exception as e:
        print(e)
        print('atom not found in megabase')
        return 1;


def countLiInStructure(sites):
    LiCounter = 0;
    for i in range(len(sites)):
        if(sites[i]['label']== 'Li'):
            LiCounter+=1;
    return LiCounter;

#This attempts to convert a chemical formula into a dictionary of elemen tsymbols and element counts
def compoundParser(chemformula): #this fails for compounds with polyanions (PO4)2 for example
    preliminary = r.findall(r'([A-Z][a-z]*)(\d*)', chemformula);
    for i in range(len(preliminary)):
        preliminary[i] = list(preliminary[i]);
        if(len(preliminary[i][1]) == 0):
            preliminary[i][1] = 1;
        else:
            preliminary[i][1] = int(preliminary[i][1]);
    return preliminary;

def reducedCellComposition(batterydict):
    red_cell_comp = batterydict['framework']['reduced_cell_composition'];
    redCellAtoms = 0;
    for i in red_cell_comp.keys():
        redCellAtoms += red_cell_comp[i];
    return redCellAtoms;

##this requires a list containing all the maxdeltavols in a batteryfamily
def AggregatedVolChange(maxdeltavoldata):
    start = 100;
    for i in maxdeltavoldata:
        start += start*i;
    aggregatedChange = (start - 100)/100;
    return aggregatedChange;
