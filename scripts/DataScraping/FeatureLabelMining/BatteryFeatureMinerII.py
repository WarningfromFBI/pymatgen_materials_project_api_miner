import os;
import sys;
import pickle
from multiprocessing import Pool
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import *
import APIMining.MaterialsAPIMiner.AddMPIDToManifest as manifest
from MaterialsProjectReader import BatteryBaseReader as bbr
from MaterialsProjectReader import MegaBaseReader as mbf;
import MinedDataSets.DataReader.ResponsePredictorValidation as rpv
import MinedDataSets.DataReader.FeatureAndLabelExtractor as fle
import settings
plt.close("all")

[data1, X1] = fle.getFeatures('StructureFeatures');
[data2, X2] = fle.getFeatures('SymmetryFeatures');
[data3, X3] = fle.getFeatures('WeightedAtomisticFeatures');
[data4, X4] = fle.getFeatures('MatDataFeatures')

LotFrames = [data1, data2, data3, data4]
#rpv.compareMultiFeatureSets(LotFrames);

totalFrame = rpv.compareMultiFeatureSets(LotFrames);

totalFrame.to_csv(settings.MinedFeatureSets+'\\FeatureSets\\ReducedAllfeatures.csv')

StructureFrames = [data1, data2];
structureFrame = rpv.compareMultiFeatureSets(StructureFrames)
structureFrame.to_csv(settings.MinedFeatureSets+'\\FeatureSets\\AllStructureFeatures.csv')





