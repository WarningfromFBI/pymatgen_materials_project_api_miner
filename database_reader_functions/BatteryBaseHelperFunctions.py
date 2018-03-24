
from sympy import *
import re; import csv

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