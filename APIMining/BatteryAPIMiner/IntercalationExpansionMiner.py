import pymatgen as mg
import numpy as np
from sklearn import linear_model
from sklearn import svm;
import matplotlib.pyplot as plt
import pandas as pd
from sympy import *
from sklearn import preprocessing
from sklearn import model_selection;
from pymatgen.matproj.rest import MPRester
import math
import pickle
from scipy.stats.stats import pearsonr

## PRELIMINARY SCRIPT TO ANALYZE HOW DIFFERENT FEATURES AFFECT CHANGE IN VOLUME

f = open('D:\\Nathan\Documents\StanfordYearOne\Reed Group\MachineLearningPractice\Datasets\LithiumBattery.csv', 'r')
lithComp = list();
for line in f:
    data = line.split(",")
    print(data)
    lithComp.append(data[0].strip("\""));
#Access battery data
def get_battery_data(formula_or_batt_id):
    """Returns batteries from a batt id or formula
    Examples:
        get_battery("mp-300585433")
        get_battery("LiFePO4")
    """
    return mpr._make_request('/battery/%s' % formula_or_batt_id)

MAPI_KEY = 'kT08xPXKwuvhfBdb';
MP_ID = 'mp-19017';
mpr = MPRester(MAPI_KEY);
deltaVol = dict(); energy = list(); frac = list();
compoundNames = list(); lithId = dict(); unlithId = dict();
cin = 0;
for compound in lithComp:
    if(compound == "Battid"): #there are often several entries for a given material composition
        continue;
    results = mpr.get_battery_data = get_battery_data(compound)
    print(compound)
    name = results[0]['adj_pairs'][0]['formula_discharge']
    deltaVol[name] = (results[0]['adj_pairs'][0]['max_delta_volume'])
    compoundNames.append(name)
    lithId[name] = (results[0]['adj_pairs'][0]['id_discharge'])
    unlithId[name] = (results[0]['adj_pairs'][0]['id_charge']) #id-discharge does not corresond
    cin += 1;
    # if(cin > 20): #data extraction is slow
    #     break;

#deltaVol...visualization
# convert dictionary to list
deltaVolList = list();
for i in deltaVol:
    deltaVolList.append(deltaVol[i])
plt.hist(deltaVolList, 100);
plt.title('Volume Change for Lithium Intercalation Compounds')
plt.xlabel('proportion expansion')
plt.ylabel('counts')

classifiers = list();
for i in range(len(deltaVolList)):
    if(deltaVolList[i] > 0.1):
        classifiers.append(1)
    else:
        classifiers.append(0)

#general script to extract all battery statistics in one pass into a single data structure
BatteryMatrix = list();
for compound in lithComp:
    if(compound == "Battid"):
        continue;
    results = mpr.get_battery_data = get_battery_data(compound)
    print(compound)
    l1 = list();
    for i in results[0]:
        l1.append(results[0][i]);
    BatteryMatrix.append(l1)

S = np.array(BatteryMatrix);
volunlith = list();
vollith = list();
vollithdict = dict(); densitylithdict = dict();
volunlithdict = dict(); densityunlithdict = dict();
unitcelldict = dict();
energyperatomunlith = list();
counter = 0;

for comp in compoundNames:
    print(comp+", "+str(counter));
    lith = mpr.get_data(lithId[comp]);
    unlith = mpr.get_data(unlithId[comp]);
    lithstruct = mpr.get_structures(comp);
    energyperatomunlith.append(unlith[0]['energy_per_atom']);

    vollith.append(lith[0]['volume'])
    volunlith.append(unlith[0]['volume'])
    volunlithdict[comp] = unlith[0]['volume']
    vollithdict[comp] = lith[0]['volume']
    unitcelldict[comp] = lith[0]['unit_cell_formula']
    densitylithdict[comp] = lith[0]['density']
    densityunlithdict[comp] = unlith[0]['density'] #this is a normally distributed variable, YAY!!!!
    counter += 1;
    # if(counter > 20):
    #     break;

#write data to datafile for future access
f1 = open('D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataSets\VolumeChange.txt', 'w')
f1.write("compound, volume_lith, volume_unlith, density_lith, density_unlith")
for i in (vollithdict):
    f1.write(i+", "+str(vollithdict[i])+", "+str(vollithdict[i])+", "+str(densitylithdict[i])+", "+str(densityunlithdict[i]));
    f1.write('\n')
f1.close();

plt.scatter(vollith, volunlith, s = 100)
plt.xlabel('lithiated volume')
plt.ylabel('unliathiated volume')
plt.plot([0,1000], [0, 1000])

plt.figure()
# compare this to the volume change, density tends to look better behaved,
# which may not be good
x = list(densitylithdict.items())
y = list(densityunlithdict.items())
density = list();
for i in range(len(densitylithdict)):
    plt.scatter(x[i][1], y[i][1], s = 100)
    density.append([x[i][1],y[i][1]])
plt.plot([0,10],[0,10])

deltaVolCalc = list(); #these are raw volume differences, not normalized to #unit formulas per unit cell
classif2 = list();
for i in vollithdict:
    #we have to scale all the volumes by the number of formula units per unit cell
    delta = (vollithdict[i] -volunlithdict[i])/volunlithdict[i];
    deltaVolCalc.append(delta)
    if(delta > 0.2):
        classif2.append(1);
    else:
        classif2.append(0);
    print(i+": "+str(delta) +", expected: "+str(deltaVol[i]));
classif22 = np.array(classifiers[:291]);
classif22 = np.reshape(classif22, (291,1))
for i in vollithdict:
    if(vollithdict[i] - volunlithdict[i] < 0):
        print(i)

## Test of Feature Space Mining
def sphereVol(r):
    return (4/3)*math.pi*r**3;

def FreeSpaceVolume(unit_cell_formula, Volume):
    finalVol = 0;
    for elem in unit_cell_formula:
        el = mg.Element(elem);
        unitVol = sphereVol(el.average_ionic_radius);
        totalVol = unit_cell_formula[elem]*unitVol;
        finalVol += totalVol;
    return Volume - finalVol; #this is like a deltavolume...

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
    return [halogen/count, transMetal/count, nonMetal/count];

freespaceVol = list(); freespaceDict = dict(); electronegProp = list();
for i in unitcelldict:
    volume = volunlithdict[i];
    freevol = FreeSpaceVolume(unitcelldict[i], volume);
    print('atomic volume: '+str(volume)+' free space: '+ str(freevol));
    freespaceVol.append(freevol);
    freespaceDict[i] = freevol;
    electronegProp.append(ElectronegativeCount(unitcelldict[i]));
fsV = freespaceVol;
freespaceVol = np.array(freespaceVol);
freespaceVol = np.reshape(freespaceVol, (len(freespaceVol),1))
electronegProp = np.array(electronegProp)
## TESTING SOME MODELS: have to be careful here...you can't use volume to fit a model that's
# trying to predict volumes... if you use density, you have to use density of the unlithiated material
DeltaVolCalc = np.array(deltaVolCalc)
DeltaVolCalc = DeltaVolCalc.reshape((len(DeltaVolCalc),1))
classif21 = np.array(classif2);
classif2 = classif21.reshape((len(DeltaVolCalc),1))

density = np.array(density); #unlithiated density is a poor predictor by itself, which is not entirely surprising
unlithdens = np.reshape(density[:,1], (len(density), 1))
lithdens = np.reshape(density[:,0], (len(density), 1))
plt.figure()
plt.scatter(unlithdens, freespaceVol, s = 400, c = classif2, cmap = 'viridis')
plt.xlabel('unlithiated density')
plt.ylabel('Free Space Volume')
plt.title(' Distribution of 340 Lithium Compounds')


#logisticRegression
clf = linear_model.LogisticRegression()
# Variables in general tend to look too much skewed right
#Let's combine the freepsace volume and the unlithiated material density
energyatom = np.reshape(np.array(energyperatomunlith), (len(energyperatomunlith), 1));
DatDensityFreeSpace = np.concatenate((freespaceVol, unlithdens, energyatom[0:291]), axis = 1)
test_errors = list();
DatDensityElectro = np.concatenate((freespaceVol, unlithdens, np.reshape(electronegProp[:,0],(291,1))), axis = 1)
svmach = svm.SVC(kernel = 'linear'); #linear kernel works better?
for i in range(100):
    sizeFrac = np.random.uniform(0.5,0.9);
    X_train, X_test, y_train, y_test = model_selection.train_test_split(DatDensityFreeSpace, classif2, test_size=sizeFrac, random_state=0)
    clf.fit(X_train, y_train);
    predictions = clf.predict(X_test);
    predictions = np.reshape(predictions,(len(y_test),1))
    err = np.count_nonzero(predictions-y_test)/len(y_test);
    test_errors.append(err); #average test errors is 15.5%



# 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(unlithdens, freespaceVol, electronegProp, s = 200, c = classif2)
plt.xlabel('density');
plt.ylabel('free space');
plt.zlabel('energy')
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)
## Let's do a little cross validation:
scores = model_selection.cross_val_score(clf, DatDensityFreeSpace, classif21, cv = 5)

afile = open(r'D:\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataSets\unitcelldict.pkl', 'wb');
pickle.dump(unitcelldict, afile);
afile.close();
file2 = open(r'D:\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\DataSets\unitcelldict.pkl', 'rb')
new_d = pickle.load(file2)
file2.close()

#Check the Pearson R coefficients
for i in range(3):
    a = np.corrcoef(DatDensityFreeSpace[:291, i], deltaVolCalc) #almost no correlation
    print(a[0][1]);
