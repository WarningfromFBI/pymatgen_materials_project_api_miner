
import os
import json
directory2 = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\MaterialsProject\LithiumBatteryBase'; #contains data from BATTERY EXPLORER

def GetAllBatteries():
    batterylist = list();
    for filename in os.listdir(directory2):
        file = open(directory2+"\\"+filename, 'r')
        data = "";
        for line in file:
            data = json.loads(line);
        batterylist.append(data);
    return batterylist;

def readBattery(file):
    data = "";
    for line in file:
        data = json.loads(line);
    return data;


