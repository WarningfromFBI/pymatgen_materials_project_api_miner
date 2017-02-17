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

def get_battery_data(formula_or_batt_id):
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


def parseCompound(formula):
    if(len(formula) <= 2 or formula == 'Li'):
        return " "
    elemSymbols = " ".join(re.findall("[a-zA-Z]+", formula));
    elemSymbols = elemSymbols.replace(' ', '');
    elements = BatterySearchGenerator(elemSymbols);
    return elements;

#function which strips out lithium from compound name
def LithiumStrip(formula):
    #first locate index of 'Li'
    #check if there is a numeric index after it, if there is remove it as well
    Lindex = formula.find('Li');
    endstrip = 2;
    #print(Lindex);
    while(Lindex+endstrip < len(formula) and formula[Lindex+endstrip].isdigit() ):
        #print(endstrip+Lindex)
        endstrip+=1;

    answer = formula[:Lindex] + formula[Lindex+endstrip:];
    return answer;