import os, glob
import scipy.ndimage
import numpy as np

def sorted_list(path):

    tmplist = glob.glob(path)
    tmplist.sort()

    return tmplist

def min_max_norm(x, batch=False):

    if(not(batch)):
        min_x, max_x = x.min(), x.max()
    else:
        xflat = x.reshape((x.shape[0], -1))
        min_x, max_x = xflat.min(axis=1), xflat.max(axis=1)
        min_x, max_x = np.expand_dims(min_x, axis=(1, 2, 3)), np.expand_dims(max_x, axis=(1, 2, 3))

    return (x - min_x + 1e-12) / (max_x - min_x + 1e-12)

def zoom(x, ratio=[4, 4, 1]):

    return scipy.ndimage.zoom(x, ratio, order=3, mode='nearest')
