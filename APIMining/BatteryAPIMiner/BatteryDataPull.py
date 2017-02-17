import time
import pymatgen as mg
import numpy as np
import scipy
import matplotlib.pyplot as plt
import pandas as pd
from sympy import *
import os
import string
from pymatgen.matproj.rest import MPRester
from pymatgen.phasediagram.maker import PhaseDiagram
from pymatgen.electronic_structure.plotter import BSPlotter;
from pymatgen import core
from mpl_toolkits.mplot3d import Axes3D;
import requests;
import math
import re; import csv
import json

#GENERATE A TEXT FILE DATABASE OF ALL VIABLE LITHIUM CONTAINING BATTERY COMPOUNDS
#this is partially deprecated, please see version two of this code

MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);
def get_battery_data(formula_or_batt_id):
    """Returns batteries from a batt id or formula
    Examples:
        get_battery("mp-300585433")
        get_battery("LiFePO4")
    """
    return mpr._make_request('/battery/%s' % formula_or_batt_id)

def BatterySearchGenerator(elements):
    counter = 0; hyphenIndices = list();
    for i in range(len(elements)-1):
        if(elements[i].islower()):
            hyphenIndices.append(counter);
        elif(elements[i+1].isupper()):
            hyphenIndices.append(counter);
        counter+=1;
    c2 = 0; #this accounts for the fact that the string grows every time we put in a '-'
    for i in hyphenIndices:
        elements = elements[:i+c2+1]+'-'+elements[i+c2+1:]
        c2 +=1;
    return elements;


f = open('D:\\Nathan\Documents\StanfordYearOne\Reed Group\MaterialsProject\MP_data\LithiumMPIdsDict.txt', 'r')
counter = 0;
BatteryBase = list();
databasedir = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\MaterialsProject\MP_data\lithiumBatteryDatabase\\';
batterycounter = 0;
for i in f:
    BatteryIDs = dict();
    compoundDat = (i.rstrip().split(', '))
    formula = compoundDat[0];
    if(len(formula) <= 2 or formula == 'Li'):
        continue;
    elemSymbols = " ".join(re.findall("[a-zA-Z]+", formula));
    # print(elemSymbols)
    elemSymbols = elemSymbols.replace(' ', '');
    elements = BatterySearchGenerator(elemSymbols);
    print(formula); print(counter)
    gotData = True;
    while gotData:
        try:
            battery = mpr.get_battery_data = get_battery_data(formula);
            gotData = False;
        except TimeoutError:
            continue;
        break
    print(battery)
    if (len(battery) == 0):
        continue;
    else:
        batterycounter+=1;
        print(batterycounter);
    for batt in battery:
        name = batt['adj_pairs'][0]['formula_discharge']+".txt";
        #Check if the name is already in the database:
        if(os.path.isfile(databasedir+name)):
            continue;
        if(batt['working_ion'] != 'Li'): #getting non-lithium materials...skip them
            continue;
        h = open('D:\\Nathan\Documents\StanfordYearOne\Reed Group\MaterialsProject\MP_data\lithiumBatteryDatabase'+'\\+'+name, 'w')
        #convert the data into json object
        jsonbat = json.dumps(batt); #jsonbat is a string
        h.write(jsonbat);
        h.close();

    BatteryIDs['battid'] = battery[0]['battid'];
    BatteryIDs['components'] = battery[0]['adj_pairs'][0]['material_ids']
    BatteryBase.append(BatteryIDs);
    counter += 1;
    if(counter%200 == 0):
        time.sleep(10)


g = open('D:\\Nathan\Documents\StanfordYearOne\Reed Group\MaterialsProject\MP_data\LithiumBatteryData.txt', 'w')
for i in BatteryBase:
    for keys in i:
        g.write(keys + "," + "".join(i[keys]) + " ");
    g.write('\n')
g.close();