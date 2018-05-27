import pymatgen as mg
import numpy as np
from sympy import *
import math
import settings
'''
basic features which are common to all compounds, no calculations required so super fast
'''

## Every function here should return a label telling us exactly what it is
def sphereVol(r):
    return (4/3)*math.pi*r**3;

def AtomTypeCount(unit_cell_formula): #this does not do a good job of uniquely identifying all elements
    #in fact, this variable distinction al
    finalVol = 0;
    elementTypeArray = np.zeros(8);
    for elem in unit_cell_formula:
        el = mg.Element(elem);
        if(el.is_alkaline):
            elementTypeArray[7]+=1; # all compounds will have lithium...so no
        if(el.is_halogen == True):
            elementTypeArray[0]+=1;
        if(el.is_transition_metal):
            elementTypeArray[1]+=1;
        if(el.is_actinoid):
            elementTypeArray[2]+=1;
        if(el.is_chalcogen):
            elementTypeArray[3]+=1;
        if(el.is_metalloid):
            elementTypeArray[4]+=1;
        if(el.is_rare_earth_metal):
            elementTypeArray[5]+=1;
        else:
            elementTypeArray[6]+=1;
    return elementTypeArray;

def ElectronegativeCount(unit_cell_formula): #this does not do a good job of uniquely identifying all elements
    #in fact, this variable distinction al
    finalVol = 0;
    count = 0;
    halogen = 0; transMetal = 0;
    nonMetal = 0;
    for elem in unit_cell_formula:
        el = mg.Element(elem);
        if(el.is_alkali):
            continue;
        if(el.is_halogen == True):
            halogen+=1;
        if(el.is_transition_metal):
            transMetal+=1;
        else:
            nonMetal +=1;
        count+= 1;
    return {'halogen': halogen/count, 'transition': transMetal/count, 'nonmetal': nonMetal/count};

def unitCellMass(unit_cell_formula):
    Mass = 0; label = 'MassUnitcell'
    for elem in unit_cell_formula:
        element = mg.Element(elem);
        masscontribution = element.data['Atomic mass']*unit_cell_formula[elem];
        Mass+=masscontribution;
    return Mass;

def atomicNumber(unit_cell_formula): #remember, mean, mode, std, weighted mean,
    data = list();
    for elem in unit_cell_formula:
        element = mg.Element(elem);
        atmNumber = element.data['Atomic no'];
        for i in range(int(unit_cell_formula[elem])):
            data.append(atmNumber);
    answer = [np.mean(data), np.std(data)];
    return answer;

def ElementNorm(unit_cell_formula, nsites, norm): #nsites comes from materials data
    sum = 0;
    for elem in unit_cell_formula:
        sum+=(unit_cell_formula[elem]/nsites)**norm;
    return [sum**(1/norm)];

#vanderwaals radius defines the distance of closest approach for another atom
def vanderWaalRadius(unit_cell_formula, volume):
    data = list(); Vtot = 0;
    for elem in unit_cell_formula:
        element = mg.Element(elem);
        vanderRad = element.data['Van der waals radius'];
        #if(vanderRad == 'no data'):
        Vtot += sphereVol(vanderRad)
        for i in range(int(unit_cell_formula[elem])):
            data.append(vanderRad);
    #mode = max(set(data), key=data.count);  maxi = np.max(data); min = np.min(data)
    answer =  (volume-Vtot)/volume;
    return answer;


def spacegroup(matdata):
    hall = matdata['spacegroup']['hall']
    cs = matdata['spacegroup']['crystal_system']
    number = matdata['spacegroup']['number']
    point_group = matdata['spacegroup']['point_group']
    return [cs, number, point_group, hall];













