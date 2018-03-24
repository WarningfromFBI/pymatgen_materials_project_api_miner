import json;
import numpy as np;
import settings

def getAllSummaryStats(unit_cell_formula):
    s2 = settings.WolvertonDatabase
    f = open(s2 + '\\' + 'elemental_features.json', 'r');
    data = json.load(f);
    statTypeLabel = ['unwmean', 'unwstd', 'min', 'max', 'range'];
    totalLabel = list();
    totalunweight = list();
    labelCounter = 0;

    for elem in unit_cell_formula: #the unit_cell_formula only iterates through elements with no weights (
        #the unit cell formula is a dictionary with element: no of elements
        element = data[elem];
        unweightedDat = list(); #this is a list containing ALL the individual elemental features
        for key in element:
            if(labelCounter == 0):
                for j in range(len(statTypeLabel)):
                    totalLabel.append(key+' '+statTypeLabel[j]);
            number = element[key];
            unweightedDat.append(number);
        totalunweight.append(unweightedDat); #this is the total data array, which will contain a 56 element unweighted data
        #array for every atom in the unit cell.
        labelCounter+=1;

    t1 = np.array(totalunweight); #t1 is formatted so that you have elements on rows, features on columns
    d1 = t1.shape;
    finalAns = list();
    for i in range(d1[1]):
        avg = np.mean(t1[:,i])
        std = np.std(t1[:,i])
        min = np.min(t1[:,i])
        max = np.max(t1[:,i])
        spread = max-min;
        answer = [avg, std, min, max, spread];
        finalAns += (answer)
    finalAns = np.array(finalAns)
    d = finalAns.shape;
    finalAns = np.reshape(finalAns, np.prod(d), 1)
    return [finalAns, totalLabel]; #this final answer should be of length 5*56 = 280

def getReducedSummaryStats(unit_cell_formula):
    s2 = settings.WolvertonDatabase
    f = open(s2 + '\\' + 'elemental_features.json', 'r');
    data = json.load(f);
    statTypeLabel = ['unwmean', 'unwstd'];
    totalLabel = list();
    totalunweight = list();
    labelCounter = 0;

    for elem in unit_cell_formula: #the unit_cell_formula only iterates through elements with no weights (
        #the unit cell formula is a dictionary with element: no of elements
        element = data[elem];
        unweightedDat = list(); #this is a list containing ALL the individual elemental features
        for key in element:
            if(labelCounter == 0):
                for j in range(len(statTypeLabel)):
                    totalLabel.append(key+' '+statTypeLabel[j]);
            number = element[key];
            unweightedDat.append(number);
        totalunweight.append(unweightedDat); #this is the total data array, which will contain a 56 element unweighted data
        #array for every atom in the unit cell.
        labelCounter+=1;

    t1 = np.array(totalunweight); #t1 is formatted so that you have elements on rows, features on columns
    d1 = t1.shape;
    finalAns = list();
    for i in range(d1[1]):
        avg = np.mean(t1[:,i])
        std = np.std(t1[:,i])
        answer = [avg, std];
        finalAns += (answer)
    finalAns = np.array(finalAns)
    d = finalAns.shape;
    finalAns = np.reshape(finalAns, np.prod(d), 1)
    return [finalAns, totalLabel]; #this final answer should be of length 5*56 = 280



def getWeightedStats(unit_cell_formula):
    s2 = settings.WolvertonDatabase;
    f = open(s2 + '\\' + 'elemental_features.json', 'r');
    data = json.load(f);
    statTypeLabel = ['wmean', 'wstd'];
    totalLabel = list();
    totalweight = dict();
    labelCounter = 0; N = 0;
    for elem in unit_cell_formula: #iterate through cell formula, extract all data entries, 1 value per element
        element = data[elem];
        weightedDat = list();
        properties = len(element); #properties
        numAt = unit_cell_formula[elem]; #of atoms in the unit cell with the identity of elem
        for key in element:
            if (labelCounter == 0):
                for j in range(len(statTypeLabel)):
                    totalLabel.append(key + ' ' + statTypeLabel[j]);
            number = element[key];
            weightedDat.append(number);
        totalweight[elem] = (weightedDat);
        labelCounter += 1;
        N += numAt;

    #totalweight formatted so that you have elements on rows, features on columns
    finalAns = list();
    weightdata = list();
    for i in totalweight.keys(): #iterate through all the elements found in the unit cell
        #this is where we do the weighting
        data = (unit_cell_formula[i]/N)*np.array(totalweight[i]); #this is an array with data for every property for the given element
        weightdata.append(data);
    weightdata = np.array(weightdata);
    d = weightdata.shape;
    for i in range(d[1]):
        finalAns.append(np.mean(weightdata[:, i]));
        finalAns.append(np.std(weightdata[:,i]))
    finalAns = np.array(finalAns)
    finalAns = np.reshape(finalAns, (len(statTypeLabel)*d[1], 1))
    return [finalAns, totalLabel];
