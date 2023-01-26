# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 10:42:15 2023

@author: chinn

"""
import numpy as np
from pynir.CalibrationTransfer import cost_MT_PFCE


B = np.array([[10,2,3,4],[11,2.1,3.1,4.1]])
B = B.transpose()
X = [np.array([[2,3,4],[2,3,4]]),np.array([[0.2,0.3,0.4],[0.2,0.3,0.4]])]
y = [np.array([39.2]),np.array([14.49]),]
c = cost_MT_PFCE(B, X, y)

from pynir.CalibrationTransfer import pfce_constr1, pfce_constr2,pfce_constr3
c1 = pfce_constr1(B,0.98)
c2 = pfce_constr2(B,0.98)
c3 = pfce_constr3(B,0.98)
