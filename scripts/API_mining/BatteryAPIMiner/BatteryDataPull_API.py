import time
import os
from pymatgen.ext.matproj import MPRester
import json
import settings

## EXTRACT DATABASE OF ALL LITHIUM CONTAINING BATTERY COMPOUNDS from materials project API

## Key is a make_request command that can get a list of all existing battery IDs

#Check if the battery project database exists, if not, then create it.
storage_dir = 'Battery_Explorer'
storage_dir = os.path.join(settings.basedirectory, storage_dir);
if(not os.path.exists(storage_dir)):
    os.makedirs(storage_dir);

databasedir = os.path.join(settings.MaterialsProject, "LithiumBatteryExplorer");
MAPI_KEY = 'kT08xPXKwuvhfBdb';
mpr = MPRester(MAPI_KEY);
def get_battery_data(formula_or_batt_id):
    return mpr._make_request('/battery/%s' % formula_or_batt_id)

allbattids = mpr._make_request('/battery/all_ids')
batterycounter = 0; BatteryIDs = dict(); BatteryBase = list()
counter = 0;
for id in allbattids:
    print(id)
    gotData = True;
    while gotData:
        try:
            battery = mpr.get_battery_data = get_battery_data(id);
            print(battery)
            gotData = False;
        except Exception as e:
            print(e);
            time.sleep(10)
            continue;
        break
    if (len(battery) == 0):
        continue;
    else:
        batterycounter += 1;
    for batt in battery:
        name = id + ".txt";
        # Check if the name is already in the database:
        print(databasedir + "\\" + name)
        if (os.path.isfile(databasedir + "\\+" + name)):
            print('found')
            continue;
        if (batt['working_ion'] != 'Li'):  # getting non-lithium materials...
            continue;
        else:
            print('new battery')
            h = open(os.path.join(storage_dir, name), 'w+')
            # convert the data into json object
            jsonbat = json.dumps(batt);  # jsonbat is a string
            h.write(jsonbat);
            print(batterycounter);

            print(battery)

            h.close();

    #get the ids for future reference
    BatteryIDs['battid'] = battery[0]['battid'];
    BatteryIDs['components'] = battery[0]['adj_pairs'][0]['material_ids']
    BatteryBase.append(BatteryIDs);
    counter += 1;
    if (counter % 200 == 0):
        time.sleep(10)


## Generate a text file containing all the mpids of the batteries mined
g = open(os.path.join(storage_dir, 'LithiumBatteryExplorer.txt'), 'w+')
for i in BatteryBase:
    for keys in i:
        g.write(keys + "," + "".join(i[keys]) + " ");
    g.write('\n')
g.close();
