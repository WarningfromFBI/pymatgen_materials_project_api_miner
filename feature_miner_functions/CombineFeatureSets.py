import pandas as pd
import MinedDataSets.DataReader.ResponsePredictorValidation as rpv

def combinefeatureSets(X1, X2): #inputs are dataframes
    [X1, X2] = rpv.compareFeatureSets(X1, X2);
    answer = pd.concat((X1, X2), axis=1);
    return answer;