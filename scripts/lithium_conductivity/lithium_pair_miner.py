import os;
import pickle
from database_reader_functions import materials_project_reader as mbf;
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import *
import sys
import json
from database_reader_functions.AddMPIDToManifest import *
import settings
from database_reader_functions import materials_project_reader as mbf;

'''
script which extracts possible potential cathode pairs based on stoichiometry or compositional matching
'''
## match unit cell formulas precisely...
def compareUnitCellFormula(f1, f2):
    if(len(f1)!= len(f2)):
        return False;
    else:
        for i in f1:
            if(i not in f2.keys()):
                return False
            else:
                if(f1[i]!= f2[i]):
                    return False;
    return True;


plt.close("all")

directory = os.path.join(settings.ROOT_DIR,'Materials_Project_Database');
structureDir = os.path.join(settings.ROOT_DIR, 'structure_database');

lithium_containing = list(); non_lithium_containing = list();
c = 0;
for filename in os.listdir(directory):
    try:
        [matdata, structuredata] = mbf.readCompound(filename);
        elements = matdata['unit_cell_formula'];
        if('Li' in elements.keys()):
            lithium_containing.append(filename);
        else:
            non_lithium_containing.append(filename)
    except Exception as e:
        print(e);

    c+=1;
    print(c)
print(len(lithium_containing))

'''
now perform the pairing analysis
'''

counter = 0;
unlithiated_to_lithiated_paris = list();
for line in non_lithium_containing:
    print(counter)
    print(line)
    mpid = line.strip('.txt');
    [matdata, structdata] = mbf.readCompound(line);
    #get an unlithiated version of the material
    unlith_ucf = matdata['unit_cell_formula'];
    #remove Li from unit_cell_formula
    unlith_formula = matdata['pretty_formula']
    #now we have to cycle through the entire materials project database
    for lith_filename in lithium_containing:
        #print(ucf)
        lith_mpid = lith_filename.strip('.txt')
        [lith_matdata, lith_structdata] = mbf.readCompound(lith_filename);
        lith_ucf = lith_matdata['unit_cell_formula'];
        lith_formula = lith_matdata['pretty_formula'];
        if(compareUnitCellFormula(lith_ucf, unlith_ucf)):
            unlithiated_to_lithiated_paris.append([mpid, unlith_formula, lith_mpid, lith_formula]);
    counter +=1;
    # if(counter > 2):
    #     break;





