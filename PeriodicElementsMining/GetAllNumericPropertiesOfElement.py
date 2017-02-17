import sys
import csv
import numpy as np;
from scipy import stats

wolverton = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\MaterialsProject\WolvertonDatabase\MaterialsAndElements.csv'

def getElementsData():
    f = open(wolverton, 'r')
    reader = csv.reader(f)
    counter = 0;
    ElementDict = dict();
    for row in reader:
        if(len(row[0]) <= 3): #elements are all A1 or Aa1
            #print(row)
            counter+=1;
            name = row[0][:-1]; fillrow = True;
            data = list();
            for k in range(1, len(row)):
                if(row[k] == 'None'):
                    data.append(0); #magnetic moment
                    continue;
                data.append(float(row[k]));

            if(name in ElementDict.keys()):
                ElementDict[name].append(row[1:]);
            else:
                ElementDict[name] = list();
                ElementDict[name].append(data)
    print(counter)
    return ElementDict;

def getElementalAverages(unit_cell_formula, Elements):
    total = list(); defaultlabels = ['energy_pa', 'volume_pa', 'bandgap','magnetization', 'delta_e', 'stability'];
    for i in unit_cell_formula.keys():
        data = Elements[i][0]; #
        index = 0;
        while ('None' in Elements[i][0] and index < len(Elements[i])):
            data = Elements[i][index];
            index+=1;
        for j in range(int(unit_cell_formula[i])):
            total.append(data);
    total = np.array(total);
    answer = list();
    d = total.shape;
    #print('data shape: '+str(d))
    statisticLab = ['mean', 'std', 'max', 'min', 'range']; totalLabels = list();
    for i in statisticLab:
        for j in defaultlabels:
            lab = j+', '+i;
            totalLabels.append(lab);
    vec = list();
    for i in range(d[1]):
        #print(total[:,i])
        maximum = np.max(total[:,i])
        minimum =  np.min(total[:,i]);
        Range= maximum - minimum
        vec+=([np.mean(total[:,i]), np.std(total[:,i]), maximum, minimum, Range]);
    return [vec, totalLabels];


# x = getElementsData()
# print(x)
# print(len(x))