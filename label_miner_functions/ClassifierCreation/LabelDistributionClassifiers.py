import numpy as np

def createBinaryClassifierbyMean(y):
    classifiers = list();
    for j in y:
        if(j > np.mean(y)):
            classifiers.append(1)
        else:
            classifiers.append(0)
    return classifiers

def createTernaryClassifier(y, bottom = 25, top  = 75):
    classifiers = list();
    for j in y:
        if(j > np.percentile(y, top)):
            classifiers.append(2)
        elif (j <np.percentile(y, bottom)):
            classifiers.append(0)
        else:
            classifiers.append(1)
    return classifiers;