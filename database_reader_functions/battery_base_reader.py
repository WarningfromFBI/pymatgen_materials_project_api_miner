
import os
import json
import settings

'''
functions for reading the battery explorer, which are json structured text files
'''

def GetAllBatteries(directory = os.path.join(settings.ROOT_DIR, 'Battery_Explorer')):
    '''
    extracts every battery in the directory
    :param directory:
    :return:
    '''
    batterylist = list();
    directory_search = os.path.join(settings.ROOT_DIR, directory);
    for filename in os.listdir(directory_search):
        file = open(os.path.join(directory_search, filename), 'r')
        data = "";
        for line in file:
            data = json.loads(line);
        batterylist.append(data);
    return batterylist;

def readBattery(filename, directory = os.path.join(settings.ROOT_DIR, 'Battery_Explorer')):
    '''
    :param filename:
    :return:
    reads a single battery
    '''
    file = open(os.path.join(directory, filename), 'r');
    data = "";
    for line in file:
        data = json.loads(line);
    return data;


