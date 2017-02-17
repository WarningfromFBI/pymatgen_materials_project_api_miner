
import os
from pymatgen.matproj.rest import MPRester
import json;
import time
import settings

MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);
megabase = settings.MaterialsProject+'\\Megabase'
f = open(os.curdir+'\\mpids.txt');
database = megabase

counter = 0;
for i in f:
    print(i.rstrip()); mpid = i.rstrip();
    c = True;
    while c:
        try:
            filename = mpid + '.txt';
            if (os.path.isfile(database + '\\' + filename)):
                break;

            data = mpr.get_data(mpid);
            if(len(data) == 0): #there was one record that did not have any data in it...
                break;
            data = data[0];
            structure = mpr.get_structures(mpid)[0].as_dict();
            jsondat1 = json.dumps(data);
            jsondat2 = json.dumps(structure);
            g = open(database + '\\' + filename, 'w');
            g.write(jsondat1);
            g.write('\n')
            g.write(jsondat2);

            c = False;
        except Exception as e:
            print(e);
            time.sleep(10)
            continue
    # if (counter > 5):
    #     break;
    counter += 1;
    print(counter)