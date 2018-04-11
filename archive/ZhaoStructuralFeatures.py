import settings
import json
import numpy as np
'''
what is this?
'''
# This, on the face of it, only makes sense if we comparing compounds with the same crystal system
def getStructuralWeightFeatures(picklestruct):
    s2 = settings.WolvertonDatabase
    f = open(s2 + '\\' + 'elemental_features.json', 'r');
    data = json.load(f);
    #store all 56 features as feature (as propertyatom): weighted property
    #first, the dictionar with all features
    featuredict = dict(); answerdict = dict(); test = list()
    normalizer = dict();
    for prop in data['O']:
        featuredict[prop+' StructuralCOM'] = list()
        normalizer[prop+' StructuralCOM'] = list();
        answerdict[prop + ' StructuralCOM'] = list();

    #start constructing the cOM features
    for sites in picklestruct.sites:
        elem = sites.specie.name;
        #get the element from the wolverton
        elementData = data[elem];
        cellPosition =  sites.coords;
        print(cellPosition)
        for property in elementData:
            print(elementData[property]*cellPosition)

            featuredict[property+' StructuralCOM'].append(elementData[property]*cellPosition)
            normalizer[property+' StructuralCOM'].append(elementData[property])

    #calculate the final com
    counter = 0;
    for propertyatom in featuredict:
        print(propertyatom)
        start = np.array([0.0 ,0.0 ,0.0]);
        for vector in featuredict[propertyatom]:
            start += vector;
        answer = [vec/(np.sum(normalizer[propertyatom])) for vec in start]
        print(start)
        print(np.sum(normalizer[propertyatom]))
        answerdict[propertyatom] = answer
        test.append(answer)
        counter+=1;
    return answerdict



