import numpy as np

#Layers algorithm works based on channels and each channel is oriented
#in their respective access and required atom coordinates are used
#to calculate the atoms that would be engulfed by a channel
def z_channel(atom1,atom2):
    a=(atom1.coord[0] - atom2.coord[0])**2
    b=(atom1.coord[1] - atom2.coord[1])**2
    return np.sqrt(a+b)

def y_channel(atom1,atom2):
    a = (atom1.coord[0] - atom2.coord[0]) ** 2
    b = (atom1.coord[2] - atom2.coord[2]) ** 2
    return np.sqrt(a + b)

def x_channel(atom1,atom2):
    a = (atom1.coord[1] - atom2.coord[1]) ** 2
    b = (atom1.coord[2] - atom2.coord[2]) ** 2
    return np.sqrt(a + b)
