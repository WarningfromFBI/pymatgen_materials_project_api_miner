import json;

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import settings
import os
import pandas as pd
''' 
volume label miner, though this will eventually become a holistic label miner
output should be csv file of the labels that we need for the ML model
'''

plt.close("all")
structureclasses = os.path.join(settings.basedirectory,'structure_database')
batteries = os.path.join(settings.basedirectory, 'Battery_Explorer'); ## note you might have to change this last name
testcounter = 0;

rownames= list();


battery_labels = pd.DataFrame();
## battery data lists
battery_data = list();
indices = list();
for filename in os.listdir(batteries): # LIST ALL THE FILES IN THE BATTERY EXPLORER
    testcounter += 1;
    file = open(os.path.join(batteries, filename), 'r')
    data = "";
    for line in file: # there appears to be some data-repetition which wasn't dealt with in the original miner... not a huge problem though
        # print('here')
        # print(line)
        data = json.loads(line);
    print(data)
    maxVol = 0;
    battid = filename.strip('.txt')
    ## for each battery element, we need to iterate through all the battery stages, each one is a separate compound pair
    #mine out the battery labels
    for i in range(len(data['adj_pairs'])):
        voltage_pair = data['adj_pairs'][i];
        avg_voltage = voltage_pair['average_voltage'];
        capacity = voltage_pair['capacity_vol']
        energy_density = voltage_pair['energy_vol']
        capacity_grav = voltage_pair['capacity_grav']
        energy_grav = voltage_pair['energy_grav']
        unlith = voltage_pair['formula_charge'];
        lith = voltage_pair['formula_discharge'];
        unlith_mpid = voltage_pair['id_charge'];
        lith_mpid = voltage_pair['id_discharge'];
        vol_change = voltage_pair['max_delta_volume']
        battery_data.append([avg_voltage, capacity, energy_density, capacity_grav, energy_grav, vol_change])
        indices.append(battid+', '+unlith+', '+lith+ ', '+unlith_mpid+', '+lith_mpid);
    ## ================================================================================================================

    for i in range(len(data['adj_pairs'])):
        dischargeState = data['adj_pairs'][i];
        if(dischargeState['max_delta_volume'] > maxVol):
            maxVol = dischargeState['max_delta_volume'];
        if(data['adj_pairs'][i]['max_delta_volume'] == 0):
            print(data['battid']);
            continue;
        #Now we can perform whatever analysis we want
        # now we can extract all the dat
        unlithiatedmpid = data['adj_pairs'][i]['id_charge'];
        lithiatedmpid = data['adj_pairs'][i]['id_discharge']
        batterydict = data['adj_pairs'][i];


battery_labels = pd.DataFrame(battery_data, index = indices, columns = ['avg_voltage', 'capacity_vol', 'energy_vol', 'capacity_grav', 'energy_grav', 'max_delta_vol']);
battery_labels.to_csv('battery_labels.csv')



