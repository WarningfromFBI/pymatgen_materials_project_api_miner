import settings
import pickle
structureBase = settings.MaterialsProject+'\\StructureBase';

def readStructure(mpid):
    x = pickle.load(open(structureBase+'\\'+mpid+'.p', 'rb'));
    return x;
