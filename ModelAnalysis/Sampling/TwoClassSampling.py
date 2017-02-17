
import numpy as np
#method which separates data into a training set with two well separated classes
#test set contains intermediate points

#lower and upper denote the percentages at which to separate the data
def TwoClassSeparatedLabels(X, Y, lower, upper): #data must be a numpy array
    sample = list(); intermed  = list();
    ysample = list(); yintermed = list();
    d = X.shape;
    lowerperc = np.percentile(Y, lower);
    upperperc = np.percentile(Y, upper);
    for i in range(d[0]):
        if(Y[i] < lowerperc or Y[i] > upperperc):
            sample.append(X[i,:])
            ysample.append(Y[i])
        else:
            intermed.append(X[i,:])
            yintermed.append(Y[i]);
    sample = np.array(sample); intermed = np.array(intermed);
    return [sample, intermed, ysample, yintermed];
