import matplotlib
#from nudisxs.disxs import *
from pdg_constants import *
import matplotlib.pyplot as plt
import Earth as Earth
import Flux as flux
import cross as xs
import Global as g
import FinVtx as fin
import numpy as np
import time as time
import zf as zfactor

mag =  lambda x: np.sqrt(np.sum(x**2))

class NuPropagator:
    def __init__(self,flavor):
        print('Propogator is ready')
        self.flux = flux.Flux('KM','flux_data/Numu_H3a+KM_E2.DAT',3)
        self.i = 0
        self.xs_p=cs.Cross_section(model='CT10nlo',pdg=flavor,n_tt=2212)
        self.xs_n=cs.Cross_section(model='CT10nlo',pdg=flavor,n_tt=2112)

    def set_final_vertex(self,fvertex):
        self.fvertex = fvertex

    def set_event_number(self,i):
        self.i = i
    
    def prepare_propagation(self,i):
        self.earth=Earth.Earth(self.r,'PREM')
        self.spectra = self.flux.get_spectra_points()
        self.zfactor=zfactor.zf()
        self.set_event_number(i)
        self.energy = self.spectra[0][self.i]
        phi = np.random.random()
        cos = self.specta[1][self.i]
        sin = (1-cos**2)**0.5
        self.n = np.array([np.cos(phi)*sin,np.sin(phi)*sin,cos])
        scalar = np.sum(self.fvertex*self.n)
        self.ivertex  = self.fvertex-self.n(scalar+np.sqrt(scalar**2 - np.sum(self.vertex**2)+g.R_E**2))

    
    def probability(self,v1,v2,flavor,energy,N):            
        dep=self.earth.column_depth_vegas(v1,v2,N)
        self.depth=dep
        self.flux = self.spectra[2][self.i] 
        self.weight = self.spectra[3][self.i] 
        self.zf=self.zfactor.f(g.g*dep/g.cm**2,energy)
        prob = np.exp(-(self.Z*self.xs_p.tot(energy)+self.N*self.xs_m.tot(energy))
        prob = prob/(self.Z+self.N)*g.N_A*self.depth/g.g)
        prob_zf=np.exp(-(self.Z*self.xs_p.tot(energy)+self.N*self.xs_n.tot(energy))
        prob_zf = prob_zf/(self.Z+self.N)*(1-self.zf)*g.N_A*self.depth/g.g)
        return prob_zf,self.energy, self.cos, self.flux,self.weight

    def get_dragging(self,self.i,):
        self.prepare_propagation(self.i)
        info = self.probability(self.ivertex,self.fvertex,self.flavor)
        self.set_event_number(self.i+1)
        return info
