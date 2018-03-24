import json;
import os;
import sys;
import settings

def readCompound(filename):
    try:  # access the individual compound data files
        with open(settings.MaterialsProject+'\\MegaBase'+'\\'+filename, 'r') as x:
            # We have to do the volume things from the battery data here since there could be some gaps in the materials database
            matdata = "";
            structuredata = "";
            counter = 0;
            for line in x:  # iterate through mat
                if (counter == 0):  # BASE MATERIAL DATA
                    matdata = json.loads(line)

                if (counter == 1):  # STRUCTURE
                    structuredata = json.loads(line);
                counter += 1;
        return [matdata, structuredata];
    except Exception as e:
        print('error in readCompound')
        print(e)