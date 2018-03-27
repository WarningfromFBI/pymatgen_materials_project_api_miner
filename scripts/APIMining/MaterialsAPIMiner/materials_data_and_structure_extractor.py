
import os
from pymatgen.ext.matproj import MPRester
import json;
import time
import settings
import settings
import os

MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);
megabase = os.path.join(settings.basedirectory,'Materials_Project_Database');
f = open(os.path.join(os.curdir,'mpids.txt')); #alwasy keep mpids.txt in the same directory as this script
database = megabase

## create the Materials megabase if it doesn't exist
if(not os.path.exists(megabase)):
    os.makedirs(megabase);


counter = 0;
for i in f:
    print(i.rstrip()); mpid = i.rstrip();
    c = True;
    while c:
        try:
            filename = mpid + '.txt';
            if (os.path.isfile(os.path.join(database, filename))):
                break;

            data = mpr.get_data(mpid);
            print(data)
            if(len(data) == 0): #there was one record that did not have any data in it...
                break;
            data = data[0];
            structure = mpr.get_structures(mpid)[0].as_dict();
            jsondat1 = json.dumps(data);
            jsondat2 = json.dumps(structure);
            g = open(os.path.join(database, filename), 'w');
            g.write(jsondat1);
            g.write('\n')
            g.write(jsondat2);

            c = False;
        except Exception as e:
            print(e);
            time.sleep(0.1);
            print('moving on')
            continue
    # if (counter > 5):
    #     break;
    counter += 1;
    print(counter)