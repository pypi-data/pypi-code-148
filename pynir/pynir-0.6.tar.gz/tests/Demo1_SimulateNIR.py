import numpy as np
import matplotlib.pyplot as plt
from pynir.utils import simulateNIR

X,y,wv = simulateNIR(nSample=200,nComp=10,noise=1e-5)

fig, ax = plt.subplots()
ax.plot(wv,np.transpose(X))
ax.set_xlabel("wavelength (nm)")
ax.set_ylabel("Intesntiy (a.u.)")
plt.show()

fig, ax = plt.subplots()
ax.hist(y)
ax.set_xlabel("Reference values")
ax.set_ylabel("Count")
plt.show()