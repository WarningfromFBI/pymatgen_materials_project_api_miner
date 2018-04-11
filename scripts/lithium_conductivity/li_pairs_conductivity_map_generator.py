## script to analyze stoichiometrically the lithium pairs
## that potentially exist in the materials proejct
## which are intercalation candidates
import pandas as pd
import pickle;
import os
import settings
# from pymatgen.ext.matproj import MPRester
#
#
# MAPI_KEY = 'kT08xPXKwuvhfBdb';
# MP_ID = 'mp-19017';
# mpr = MPRester(MAPI_KEY);
'''
generate the conductivity map which maps unlithiated to lithiated based on stoichiometry
this script should probably be in the pymatgen api miner and data scraper
'''

dir = os.path.join(settings.ROOT_DIR, 'datasets', 'lithium_conductivity')

file1 = open(os.path.join(dir,'MPLithiatedUnlithiatedPairs.p'), 'rb'); # contains just MPIDS
file2 = open(os.path.join(dir,'MPUnlithiatedLithiatedPairs.p'), 'rb'); #these just contain MPIDS
file3 = open(os.path.join(dir,'MPUnlithiated_Lithiated_Formulas.p'), 'rb')
LU=pickle.load(file1);
UL = pickle.load(file2);
UL2 = pickle.load(file3);
print(LU.keys());
print(len(LU.keys()))

#only 11581 materials in the MP will have a stoich match?
#this seems large...let's verify
print(len(UL.keys()))

print(UL2)
print('number of lithium pair matches')
print(len(UL2)) ## UL2 suggests 11581 compounds match by stoichiometry? that seems like TOO MANY
                ## in fact, that's almost the same number as the total number of Li compounds

bad_counter = 0;
## we will manually edit the dictionary
kill_list = list();

for i in UL2.keys():
    print(i)
    '''
        this does the stoichiometric MAPPING of unlith-lith pairs
    '''
    key1 = UL2[i][1]; #unlith formula as dictionary (obviously no lithium here)
    key2 = UL2[i][2]; #lith formula as dictionary without lithium
    ratio = -1; #initialize it as -1 so we know that a ratio hasn't been calculated yet
    deleteKey = False;
    for elem in key1:
        if(ratio < 0): #check the ratio of
            if(key1[elem]%key2[elem] != 0):
                print('false')
                bad_counter += 1;
                deleteKey = True;
                break;
            else:
                ratio = (key1[elem])/key2[elem]
        else:
            if(key1[elem]/key2[elem] != ratio):
                print('false')
                deleteKey = True;
                bad_counter+=1;
                break;
            else:
                print(key1, key2)
    if(deleteKey):
        kill_list.append(i);

for dead in kill_list:
    del UL2[dead];

print(bad_counter)
print(len(UL2))
pickle.dump(UL2, open('MPUnlithiated_Lithiated_Formulas.p', 'wb'))

## compare this dictionary to the prediction set
# this should filter out things in UL2 that actually have lithium in it

Xp = pd.read_csv(os.path.join(settings.ROOT_DIR, 'datasets', 'deployment_data',\
                              'deployment_set.csv'), index_col = 0);
counter = 0;
prediction_mpid = list();
prediction_compound_map = dict();
for key in Xp.index:
    [compound, mpid] = key.split(', ');
    prediction_mpid.append(mpid); prediction_compound_map[mpid] = compound;
    if(mpid in UL2.keys()):
        counter+=1;
print(counter)

mismatched_UL2 = list();
matched_UL2_compounds = list();
for key in UL2.keys():
    if(key not in prediction_mpid):
        mismatched_UL2.append(key);
    else:
        matched_UL2_compounds.append(prediction_compound_map[key])
#kill those keys
for mismatch_key in mismatched_UL2:
    del UL2[mismatch_key];
print(mismatched_UL2);
print(len(UL2))

## ============= CREATE THE CONDUCTIVITY MAP =====================##

conductivity = pd.read_csv(os.path.join(dir,'lithium_conductivities.csv'), index_col = 0);
conductivity_map = list();
for mpid in UL2.keys():

    lithiated_mpid = UL2[mpid][0];
    if(lithiated_mpid in conductivity.T.columns):
        print(mpid+', '+lithiated_mpid+', '+str(conductivity.T[lithiated_mpid]))
        conductivity_map.append([mpid, lithiated_mpid, prediction_compound_map[mpid], \
                                 conductivity.T[lithiated_mpid]['probability']]);
import numpy as np
cmap = pd.DataFrame(conductivity_map, columns = ['unlith_mpid', 'lith_mpid', 'unlith_compound',  'conductivity'])
cmap.set_index('unlith_mpid', inplace=True)
cmap.to_csv('conductivity_map.csv')