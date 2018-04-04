import settings
import pickle
structureBase = settings.MaterialsProject+'\\structure_database';

def readStructure(mpid):
    x = pickle.load(open(structureBase+'\\'+mpid+'.p', 'rb'));
    return x;
