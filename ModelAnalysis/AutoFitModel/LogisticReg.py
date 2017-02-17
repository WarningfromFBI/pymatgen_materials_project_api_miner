from sklearn.model_selection import train_test_split;
from sklearn.metrics import confusion_matrix
from sklearn import linear_model
import numpy as np

def runLogReg(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    clf = linear_model.LogisticRegression()
    clf.fit(X_train, y_train);
    pred = clf.predict(X_test);
    miscal = np.count_nonzero(pred.reshape(len(pred), 1) - y_test) / len(pred)
    scoresamp = clf.score(X_test, y_test);
    print(confusion_matrix(pred, y_test));
    print(scoresamp)
    print('number of positive: ' + str(np.count_nonzero(y_test)))
    print('proportion of positive: '+ str(np.count_nonzero(y_test)/len(y_test)))
    print(miscal)

