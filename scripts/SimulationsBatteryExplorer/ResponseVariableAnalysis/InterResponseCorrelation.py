import numpy as np

import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle;
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import MinedDataSets.DataReader.ResponsePredictorValidation as rpv


plt.close("all")
vlabels = fle.getLabels('volumeLabels');
[X, Xarr] = fle.getFeatures('ReducedAllFeatures')
[X, vlabels] = rpv.compareFeatureSets(X, vlabels);

counter = 0;
X_scaled = preprocessing.scale(X);

plt.figure()
corrcoeffmatrix = np.corrcoef(vlabels)
plt.plot(corrcoeffmatrix)
plt.show()
for i in range(len(corrcoeffmatrix)):
    print(np.max(corrcoeffmatrix[:,i]));
    print(np.mean(abs(corrcoeffmatrix[:,i])))
print('feature shape: '+str(X.shape))

plt.figure()
scatter_matrix(vlabels)




