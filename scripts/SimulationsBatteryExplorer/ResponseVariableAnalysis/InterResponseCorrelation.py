import numpy as np

import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle;
import pandas as pd
from pandas.tools.plotting import scatter_matrix


plt.close("all")
[vlabels, Data, X, anisotropylabels] = fle.getLabelsFeatures('AllFeatures');
counter = 0;
X_scaled = preprocessing.scale(X);
varray = list();
for i in vlabels:
    varray.append(vlabels[i])

plt.figure()
corrcoeffmatrix = np.corrcoef(varray)
plt.plot(corrcoeffmatrix)
plt.show()
for i in range(len(corrcoeffmatrix)):
    print(np.max(corrcoeffmatrix[:,i]));
    print(np.mean(abs(corrcoeffmatrix[:,i])))
varray = np.array(varray)
print('feature shape: '+str(X.shape))
counter = 0;
plt.figure()
pandavol = pd.DataFrame(vlabels);
scatter_matrix(pandavol)
plt.show()



