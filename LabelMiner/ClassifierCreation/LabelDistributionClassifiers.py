import numpy as np

def createBinaryClassifierbyMean(y):
    classifiers = list();
    for j in y:
        if(j > np.mean(y)):
            classifiers.append(1)
        else:
            classifiers.append(0)
    return classifiers
