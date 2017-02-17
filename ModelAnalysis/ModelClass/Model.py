import pandas as pd

class Model:
    def __init__(self, X, y):
        #check type of the input(X and y), they should be pandaframes
        if (~isinstance(X, pd.DataFrame) or ~isinstance(y, pd.DataFrame)):
            print('problem')
        else:
            self.Features = X;
            self.Labels = y;
            self.statistics = dict();

    def runModel(self, logistic):
        return None;

    def updateFeatures(self):
        return None

    def updateLabels(self):
        return None

    def getLabel(self, name):
        return self.Labels[name]