import nugen as nn
from nudisxs.disxs import *
import time as time
import numpy as np
N =100
nun = nn.NuGen()
tt1 = np.zeros(N)
tt2 = np.zeros(N)
for i in range(N):
    tt1[i] = time.time()
    nun.get_event_fix_en()
    tt1[i] = time.time()-tt1[i]
    tt2[i] = time.time()
    nun.get_event()
    tt2[i] = time.time()-tt2[i]

print(tt1.mean())
print(tt2.mean())

