import numpy as np
import scipy
from sklearn.datasets import load_digits
from sklearn.datasets import load_iris
from sklearn.datasets import load_breast_cancer;
from sklearn.datasets import load_boston;
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn.linear_model import Ridge;
from sklearn import svm;
from sklearn.model_selection import train_test_split;
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations
from sympy import *
import sys
import pylab; from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import confusion_matrix
import numpy as np
import scipy
from sklearn.datasets import load_digits
from sklearn.datasets import load_iris
from sklearn.datasets import load_breast_cancer;
from sklearn.datasets import load_boston;
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn.linear_model import Ridge;
from sklearn import svm;
from sklearn.model_selection import train_test_split;
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations
from sklearn import preprocessing
s = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\MaterialsProject\WolvertonDatabase\DataByFeature'
vol = 'originalDeltaVol'
print('data set is: '+vol)
datafile = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\MinedFeatureSets\IntercalationFeatures_'+vol+'.csv';
data = np.genfromtxt(datafile, delimiter = ',');
print('Data Size' + str(data.shape))

labelleddatafile = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\MinedFeatureSets\LabelledDataSets\IntercalationFeatures.csv'
Wolverton = 'D:\\Nathan\Documents\StanfordYearOne\Reed Group\IntercalationResearch\FeaturesModule'
import WolvertonAtomisticFeatures as waf;

datFrame = pd.read_csv(labelleddatafile);

#Let's do a random sample of our data to see if we can change the distribution of high and low examples
sample = list();
sampleSize = len(data)
for i in range(sampleSize): #data is heavily skewed towards low volume expansion materials
    ind = np.random.choice(sampleSize);
    if(True ):#np.mean(y)):
        sample.append(data[i, :]);
    else:
        if(np.random.choice(100) > 0):
            sample.append(data[i,:]);

clf = linear_model.LogisticRegression()
linreg = linear_model.LinearRegression();
#REMEMBER DATA MAY HAVE MULTIPLE VOLUME METRICS
data = np.array(sample);
pandasData = pd.DataFrame(data)
y = data[:,-1].reshape(len(data),1);
X = data[:,:-1]
X_scaled = preprocessing.scale(X)

classifiers = list();
for i in y:
    if(i > np.mean(y)):
        classifiers.append(1)
    else:
        classifiers.append(0)

yclass = np.array(classifiers).reshape(len(classifiers),1);

pca = PCA(n_components = 2);
ans = pca.fit(X_scaled[:,:-1]);
Projection = pca.fit_transform(X_scaled[:,:-1])
plt.scatter(Projection[:,0], Projection[:,1], s = 200, c = classifiers)
pca3d = PCA(n_components = 3)
ans2 = pca3d.fit(X_scaled);
Projection3D = pca3d.fit_transform(X_scaled);
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(Projection3D[:,0], Projection3D[:,1], Projection3D[:,2], s = 400, c =classifiers)
#
# #histogram all the datasets in multiples of 5
d = X_scaled.shape;
counter = 0;
for key in datFrame:
    if(counter == 0):
        counter+=1;
        continue;
    datatype = key.split(" ")[0];
    series = X_scaled[:, counter];
    try:
        data = list();
        keyfile = s+'\\'+datatype+'.table';
        f = open(keyfile, 'r')
        for line in f:
            point = line.rstrip()
            if(point == 'Missing'):
                data.append(0);
            else:
                data.append(float(point))
        plt.figure()
        #plt.plot(data);
        plt.plot(series)
        plt.show()
        #now get the same data from the database
        # plt.hist(series, 100)
        # plt.legend(['mean', 'std', 'max', 'min', 'range'])
        # plt.title(key)
        counter+=1;
    except Exception as e:
        print(e);
        counter+=1;
        continue;




