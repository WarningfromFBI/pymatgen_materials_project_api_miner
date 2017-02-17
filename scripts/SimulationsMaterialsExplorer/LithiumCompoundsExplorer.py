import json
import os
import time

from pymatgen.matproj.rest import MPRester
from sympy import *

import MaterialsProjectReader as LCSM


#SEARCH THROUGH 12000 LITHIUM COMPOUNDS and generate a list of viable battery candidates
#format is lithiated formula, lithmpid, unlith mpid

def writeCompound(mpid,fname):
    if (os.path.isfile(fname)):
        return;

    data = mpr.get_data(mpid);
    if (len(data) == 0):  # there was one record that did not have any data in it...
        return;
    data = data[0];
    structure = mpr.get_structures(mpid)[0].as_dict();
    jsondat1 = json.dumps(data);
    jsondat2 = json.dumps(structure);
    g = open(fname, 'w');
    g.write(jsondat1);
    g.write('\n')
    g.write(jsondat2);


MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);

f = open('D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataStructureExtractors\LithiumMPIds.txt', 'r')
g = open('D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataStructureExtractors\LithiumMPIdsDict.txt', 'r') #these contain all lithium containing compounds
megabase = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataStructureExtractors\MegaBase';
lithiumBatteryCompounds = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataStructureExtractors\LiCompoundPairs'
currentdir = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataStructureExtractors\\';
counter = 0; #12547 lithium containing compounds
viableBatteryCounter = 0;
viableBatteryList = list();
for line in g:
    name_mpid = line.rstrip().split(", ");
    search = LCSM.parseCompound(name_mpid[0]);
    print(name_mpid[0])
    #we have to do a search with the Li part stripped, but which compound corresponds to which?
    LithStripped = LCSM.LithiumStrip(name_mpid[0]);
    c = True; unviable = 0;
    while c:
        try:
            MAPI_KEY = 'kT08xPXKwuvhfBdb';
            mpr = MPRester(MAPI_KEY);
            data = mpr.get_data(search); #each search produces a family of lithium compounds (ideally)
            print(len(data))
            if(len(data) == 0):
                break;
            else:

                print('number of compounds: '+ str(len(data)))
                viableBatteryCounter += 1;

                for i in range(len(data)):
                    detected = False;
                    lithstripped = LCSM.LithiumStrip(data[i]['pretty_formula']);
                    parsedUnlith = LCSM.parseCompound(lithstripped);
                    print('Stripped:' + lithstripped)
                    family = lithiumBatteryCompounds + '\\' + lithstripped + '.txt'
                    # if (os.path.isfile(family)):
                    #     break;
                    h = open(family, 'a');
                    print(parsedUnlith+'\n')
                    data2 = mpr.get_data(parsedUnlith);
                    detectCount = 0;

                    for j in range(len(data2)):
                        print('data2 formula: '+data2[j]['pretty_formula']+', '+lithstripped)
                        if(data2[j]['pretty_formula'] == lithstripped):
                            if(detectCount == 0):
                                h.write(search + ", " + data[i]['pretty_formula'] + ", " + data[i]['material_id'] +
                                        ', '+str(data[i]['volume'])+'\n');

                            print('MATCH!');
                            h.write(str(j)+': '+data2[j]['pretty_formula']+', '+data2[j]['material_id']+', '+
                                    str(data2[j]['e_above_hull'])+', '+str(data2[j]['volume'])+'\n')
                            #Check if the unlithiated compound is in our megabase...if it is not, add it in.
                            fname = megabase+'\\'+data2[j]['material_id']+'.txt';
                            if(os.path.isfile(fname) == False):
                                print('need to write')
                                writeCompound(data2[j]['material_id'], fname);

                            detected = True;
                            detectCount+=1;
                #we only want to close the file after we exahausted all levels of lithiation
                    h.write('\n')
                    h.close();
                    if(detected == False):
                        unviable+=1;
                        os.remove(family)
                    #print(data)
                c = False #break the loop if we finish the stuff inside spontaneously
        except Exception as e:
            print(e);

            time.sleep(10)
            break;

    counter += 1;
    print(str(counter)+", "+str(viableBatteryCounter));
    # if (counter > 3):
    #     break

