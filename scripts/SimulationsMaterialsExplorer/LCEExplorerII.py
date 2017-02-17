#analysis packages
import sys

import matplotlib.pyplot as plt

import MaterialsProjectReader as mbf

plt.close("all")

#ATTEMPT 2 TO MINE COMPOUNDS FROM MATERIALS EXPLORER AS VIABLE BATTERY COMPOUNDS

currentdir = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataStructureExtractors';
sys.path.append(currentdir);
counter = 0;

file = 'LithiumMpIDsDict.txt';

f = open(currentdir+'\\'+file, 'r');
for line in f:

    if(line == "\n"):
        continue;
    if(len(line.rstrip().split(', ')) == 1):
        continue;

    data = line.rstrip().split(', ');
    print(data)
    lithfile = megabase+'\\'+data[1]+'.txt';
    [matdata, structuredata] = mbf.readCompound(lithfile)
    print(matdata)