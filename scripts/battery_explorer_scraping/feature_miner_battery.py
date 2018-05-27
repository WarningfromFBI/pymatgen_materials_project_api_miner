
import pandas as pd
import settings
import matplotlib.pyplot as plt
import os
import settings

'''
These scripts extracts the features for the battery explorer elements using the pre-mined materials_project
'''

plt.close("all")
## step 1) : get all battery mpids
battery_labels = os.path.join(settings.ROOT_DIR, 'scripts', 'battery_explorer_scraping', 'battery_labels.csv');
data = pd.read_csv(battery_labels, index_col = 0)
materials_project = os.path.join(settings.ROOT_DIR, 'data_dump', 'materials_project.csv');

unlith_indices = list(); unlith_mpids = list();
simple_to_batt_dict = dict();
for index in data.index:
    print(index)
    [battid, unlith, lith, unlithmpid, lithmpid] = index.split(', ')
    if('Li' not in unlith):
        unlith_indices.append(unlith + ', ' + unlithmpid);
        unlith_mpids.append(unlithmpid)
        simple_to_batt_dict[unlith + ', ' + unlithmpid] = index;
print(len(unlith_indices)); #1357 training points at most
print(unlith_mpids)
#open the new structure features
structure_dat = os.path.join(settings.ROOT_DIR, 'data_dump', 'mp_new_structure_features.csv');
struct_dat = pd.read_csv(structure_dat, index_col = 0);
counter = 0;
for index in unlith_indices :
    if(index in struct_dat.index):
        counter+=1;
print('match: '+str(counter))


# now get these from the materials project;
MP = pd.read_csv(materials_project, index_col = 0);
training_indices = list();
for index in MP.index:
    if(index in unlith_indices):
        training_indices.append(index)

print(len(training_indices)); #... only 1281
training_data = MP.T[training_indices].T;
print(training_data.shape)

## we should always produce the X_battery and ylabels in tandem


ydata = data.T[list(simple_to_batt_dict.values())].T;
print(ydata.shape)

training_data.to_csv('X_battery_3.csv')
ydata.to_csv('ydata_3.csv')


# battery_exp_dir = os.path.join(settings.ROOT_DIR,'Battery_Explorer')
# for file in os.listdir(battery_exp_dir):
#     mpid = file.strip('.txt')



