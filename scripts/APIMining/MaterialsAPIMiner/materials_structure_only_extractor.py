
import os
from pymatgen.ext.matproj import MPRester
import json;
import time
import settings
import pickle
import APIMining.MaterialsAPIMiner.AddMPIDToManifest as manifest
'''
 fundamental difference between this and the materials_data_and_structure is that this thing mines the structure
 as a pymatgen structure object, so there's a higher level of abstraction and also accessibility to all of pymatgens
 structure functions, which can be useful
 
'''
MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);
structureBase = os.path.join(settings.basedirectory, 'structure_database')
if(not os.path.exists(structureBase )):
    os.makedirs(structureBase );

f = open(os.path.join(os.curdir,'mpids.txt'));
counter = 0;
for i in f:
    print(i.rstrip()); mpid = i.rstrip();
    c = True;
    while c:
        try:
            filename = mpid + '.p';
            #check if we already have it, no use in remining it...
            if (os.path.isfile(structureBase + '\\' + filename)):
                print('found')
                break;

            data = mpr.get_data(mpid);
            if(len(data) == 0): #there was one record that did not have any data in it...
                break;
            data = data[0];
            structure = mpr.get_structures(mpid)[0];
            #print(structure)
            print(type(data))
            print(type(structure))
            target = open(structureBase+'\\'+filename, 'wb')
            pickle.dump(structure, target)
            c = False;
        except Exception as e:
            print(e);
            manifest.AddMPIDtoManifest(mpid);
            time.sleep(1);
            print('moving on');
            continue
    # if (counter > 5):
    #      break;
    counter += 1;


