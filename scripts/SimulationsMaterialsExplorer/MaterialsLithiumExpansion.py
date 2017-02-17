import json

import matplotlib.pyplot as plt

import MaterialsProjectReader as MBR
import settings

#this code attempts to analyze volume properties for all lithium containing compounds
#challenge is to sort elements so they are essentially the same unlithiated element

# MAPI_KEY = 'kT08xPXKwuvhfBdb';
# MP_ID = 'mp-19017';
# mpr = MPRester(MAPI_KEY);

megabase = settings.MaterialsProject+'\\MegaBase'
currentdir = settings.MaterialsProject+'\\LithiumBatteryCompoundPairs';
#lithium battery compounds proposed
f = open(currentdir+'\\PotentialLiBattCompoundsII.txt');
#compound, lithiated, unlithiated
def getDat(file):
    d1 = ""; d2 = "";
    counter = 0;
    for line in file:
        if (counter == 0):  # BASE MATERIAL DATA
            d1 = json.loads(line);
        if (counter == 1):  # STRUCTURE
            d2 = json.loads(line);
        counter+=1
    return [d1, d2];


vols = list();
atomisticMatrix = list();
counter = 0; failedCounter = 0;
classifiers = list(); compoundsDictionary = dict();
for line in f:
    if(counter == 0):
        counter+=1;
        continue; #skip titlr

    data = line.rstrip().split(', ');
    #print(data);
    lithiated = data[1];
    unlithiated = data[2];
    if('Si' in unlithiated):
        print(lithiated)
    search1 = lithiated+'.txt';
    search2 = unlithiated+'.txt';

    try: # need a schema to group compounds by their formula
        [DataLith, structLith] = MBR.readCompound(search1);
        [DataUnLith, structUnLith] = MBR.readCompound(search2);
        #Check that the phases are the same

        key = DataUnLith['pretty_formula']
        unitcelldictLith = DataLith['unit_cell_formula'];
        vols.append(DataLith['volume']);
        LiCount = 0;
        totalAtoms = sum(unitcelldictLith.values());
        proportion = unitcelldictLith['Li']/(sum(unitcelldictLith.values()))
        classifiers.append(sum(unitcelldictLith.values())-unitcelldictLith['Li']);
        if(key in compoundsDictionary.keys()):
            compoundsDictionary[key].append({'volunlith': DataUnLith['volume'], 'vol': DataLith['volume']/totalAtoms, 'lithprop': proportion})
        else:
            compoundsDictionary[key] = list();
            compoundsDictionary[key].append({'volunlith': DataUnLith['volume'], 'vol': DataLith['volume']/totalAtoms, 'lithprop': proportion})
        counter+=1;
    except Exception as e:
        print(e); failedCounter+=1;
       # admt.AddMPIDtoManifest(unlithiated)
        #mine the compound into the megabase: where the code for that?
        continue


f.close();

#analyze the compoundDict

for i in compoundsDictionary:
    fracLith = list();
    vol = list();
    for data in compoundsDictionary[i]:
        fracLith.append(data['lithprop']);
        vol.append((data['vol']));

    if(len(vol)> 4):
        plt.figure()
        plt.scatter(fracLith, vol, s=200)
        plt.xlabel('fraction lithium')
        plt.ylabel('Volume Per Atom')
        plt.title(i)
        plt.show()




