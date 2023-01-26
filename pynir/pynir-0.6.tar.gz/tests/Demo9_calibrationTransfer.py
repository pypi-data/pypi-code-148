from pynir.utils import simulateNIR_calibrationTransfer
from pynir.Calibration import pls, regresssionReport
from pynir.CalibrationTransfer import PDS,SST, BS
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split

# Simulate NIR spectra for calibration transfer
nSample = 100
X1, X2, y, wv = simulateNIR_calibrationTransfer(nSample=nSample,nComp=10,shifts=5e1)
idxTrain,idxTest = train_test_split(np.arange(nSample),test_size=0.6)
idxTransfer,idxTest = train_test_split(idxTest,test_size=0.5)


fig, ax = plt.subplots(2,sharex=True)
ax[0].plot(wv, np.transpose(X1))
ax[0].set_title("First")

ax[1].plot(wv, np.transpose(X2))
ax[1].set_title("Second")

fig.supxlabel("Wavelength (nm)")
fig.supylabel("Intensity(A.U.)")
plt.show()

# Multivariate calibration
nComp = 7
plsModel1 = pls(nComp=nComp).fit(X1[idxTrain,:], y[idxTrain])

yhat1 = plsModel1.predict(X1[idxTest,:],nComp=nComp)
yhat2= plsModel1.predict(X2[idxTest,:],nComp=nComp)

fig, ax = plt.subplots(2,sharex=True,figsize=(8,16))
plsModel1.plot_prediction(y[idxTest], yhat1,title = "First", ax = ax[0])
plsModel1.plot_prediction(y[idxTest], yhat2, title= "Second", ax = ax[1])

# Calibration transfer on spectra
## PDS
X2_PDS = PDS(halfWindowSize=3).fit(X1[idxTransfer,:], X2[idxTransfer,:]).transform(X2[idxTest,:])
yhat2_PDS= plsModel1.predict(X2_PDS,nComp=nComp)
plsModel1.plot_prediction(y[idxTest], yhat2_PDS, title= "PDS")

fig, ax = plt.subplots()
ax.plot(wv, np.transpose(X2_PDS))


## SST
X2_SST = SST(nComp=nComp).fit(X1[idxTransfer,:], X2[idxTransfer,:]).transform(X2[idxTest,:])
yhat2_SST= plsModel1.predict(X2_SST,nComp=nComp)
plsModel1.plot_prediction(y[idxTest], yhat2_SST, title= "SST")

fig, ax = plt.subplots()
ax.plot(wv, np.transpose(X2_SST))


# Calibration transfer on prediction
## BS
yhat2_BS = BS().fit(yhat1, yhat2).transform(yhat2)
plsModel1.plot_prediction(y[idxTest], yhat2_BS, title= "BS")