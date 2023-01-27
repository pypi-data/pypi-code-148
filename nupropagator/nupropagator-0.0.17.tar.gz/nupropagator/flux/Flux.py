import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nudisxs.disxs import *
from scipy.interpolate import interp1d
from scipy.interpolate import interp2d
import math as m
import Global as g
import vegas 

class Flux:
    def __init__(self, model_name, file, dim):
        df = pd.read_csv(file,header=None, sep ='\t')
        self.energy = []
        self.Ncos=11
        if dim == 2:
            self.Ncos=1
            
        self.NPoint=len(df)
        self.cos_theta = [1-float(j)/(self.Ncos-1.) for j in range(0,self.Ncos,1)]
        self.flux = np.zeros((self.Ncos,self.NPoint))
        self.model_name = model_name
        self.dim=dim
        self.energy = np.array(df[0])
        for i in range(self.Ncos):
            self.flux[i]=np.array(df[i+1])/np.array(df[0])/np.array(df[0])
        return
    def flux_x(self,E):
        a=0
        for i in range(self.Ncos):
            a+=2*np.pi*self.flux[i]*0.1
        f = interp1d(self.energy, a, kind='cubic')
        return f(E)
    def get_energy_flux_points_spl(self,cos_theta,N): #it is 1D interpolation for energy (cos is constant. it is one from 11 values)
        f = interp1d(self.energy, self.flux[int(cos_theta*10)], kind='cubic')
        z=[10*10.**((7.*i)/(N)) for i in range(0,N+1,1)]
        return z,f(z)
    
    def get_energy_flux_points_lin(self,cos_theta,N): #it is 1D interpolation for energy (cos is constant. it is one from 11 values)
        f = interp1d(self.energy, self.flux[int(cos_theta*10)], kind='linear')
        z=[10*10.**((7.*i)/(N)) for i in range(0,N+1,1)]
        return z,f(z)
    
    def get_energy_flux_points_spl1(self,cos_theta,z=[]): #it is 1D interpolation for energy (cos is constant. it is one from 11 values)
        f = interp1d(self.energy, self.flux[int(cos_theta*10)], kind='cubic')
        return f(z)
    
    def get_theta_flux_points_spl1(self,e,z=[]): #it is 1D interpolation for energy (cos is constant. it is one from 11 values)
        f = interp1d(self.cos_theta, self.flux[:,int(10*(m.log10(e)-1))], kind='cubic')
        return f(z)
          
    def get_3D_data_points(self):
        return self.flux
    
    def get_3D_splain_points1(self,x_low=10.,x_up=10**8,Nxp=100,y_low=0,y_up=1,Nyp=100):
        I2 = interp2d(self.energy, self.cos_theta, self.flux, kind='cubic')
        z1=np.array([x_low*10**(m.log10(x_up/x_low)*i/Nxp) for i in range(0,Nxp+1,1)])
        z2=np.array([(y_up-y_low)*i/Nyp+y_low for i in range(0, Nyp+1,1)])
        return z1,z2,I2(z1,z2)
        
    def get_3D_splain_points(self,z1,z2):
        I2 = interp2d(self.energy, self.cos_theta, self.flux, kind='cubic')
        self.I2 = I2
        return I2(z1,z2)
    
    def get_3D_linear_points1(self,z1,z2):
        I2 = interp2d(self.energy, self.cos_theta, self.flux, kind='linear')
        return I2(z1,z2)
    
    #@vegas.batchintegrand
    def get_vegas_flux(self,xx):
        #z = self.I2(xx[:,0],xx[:,1])
        #z = xx[:,0]+xx[:,1]
        z = self.get_3D_splain_points(xx[0],xx[1])
        return np.array(z)
    
    def get_spectra_points(self):
        self.integrator = vegas.Integrator([[self.energy.min(),self.energy.max()], [-1,1]], nhcube_batch=2000, sync_ran=False)
        #self.integrator = vegas.Integrator([[self.energy.min(),self.energy.max()], [-1,1]])
        result = self.integrator(self.get_vegas_flux, nitn = 3,neval = 1000)
        print(result.summary)
        E = []
        cos = []
        weight = []
        for x,wgt in self.integrator.random():
            E.append(x[0])
            cos.append(x[1])
            weight.append(wgt)
        E = np.array(E)
        cos = np.array(cos)
        weight = np.array(weight)
        flux = np.zeros(len(E))
        flux = self.I2(E,cos)
        return E,cos,weight,flux


fff = Flux('KM','flux_data/Numu_H3a+KM_E2.DAT',3)
fff.get_3D_splain_points(fff.energy,fff.cos_theta)
a = fff.get_spectra_points()
print(a[0])









