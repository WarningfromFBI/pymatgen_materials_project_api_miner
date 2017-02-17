## Every function here should return a label telling us exactly what it is
import math
import numpy as np
def sphereVol(r):
    return (4/3)*math.pi*r**3;

def getDist(r1, r2):
    return (np.dot(r1-r2, r1- r2))**0.5;