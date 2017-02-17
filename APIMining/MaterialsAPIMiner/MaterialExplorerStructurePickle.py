
import os
from pymatgen.matproj.rest import MPRester
import json;
import time
import settings
import pickle
import APIMining.MaterialsAPIMiner.AddMPIDToManifest as manifest

MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);
structureBase = settings.MaterialsProject+'\\StructureBase'
f = open(os.curdir+'\\mpids.txt');

counter = 0;
for i in f:
    print(i.rstrip()); mpid = i.rstrip();
    c = True;
    while c:
        try:
            filename = mpid + '.p';
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
            time.sleep(10)
            continue
    # if (counter > 5):
    #      break;
    counter += 1;


