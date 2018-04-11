import settings
import pickle
import os
structureBase = os.path.join(settings.ROOT_DIR,'structure_database');

def readStructure(mpid):
    x = pickle.load(open(os.path.join(structureBase,mpid+'.p'), 'rb'));
    return x;
