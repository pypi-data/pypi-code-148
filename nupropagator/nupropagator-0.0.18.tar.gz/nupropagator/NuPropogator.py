import matplotlib
import XsDIS as xs
from NeutrinoNucleonXsDIS import NeutrinoNucleonXsDIS
from pdg_constants import *
xs.nucleonstructurefunctions(1,1,1,1,1,1,1,1,1)
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import Earth as earth
import Flux as fff
import cross as cs
import Global as g
import FinVtx as fin
import numpy as np
import time as time
from scipy.integrate import*
s=cs.Cross_section(model='CTEQ6.5M',pdg=14,n_tt=1)
s1=cs.Cross_section(model='CTEQ6.5M',pdg=14,n_tt=2)
#import Kinematic as kin
#import Particle as par
import zf as zf1
def initialize(dis,target):
    dis.init_structure_functions_model(2)
    dis.init_neutrino(14)
    dis.init_charged_lepton_polarization(0)
    dis.init_nucleon(target)
    dis.init_Rfunction_model(2,1)
    dis.init_Wcut(1.2*GeV)
    dis.init_FL_model(2)
    dis.init_Q2_fixing(0)
def proba(i,cos,z,nu):
    k=np.int_(z/10.)
    j=np.int_(100*cos+100)
    return nu.prob[i][j][k]
def proba1(i,cos,z,nu):
    k=np.int_(z/10.)
    j=np.int_(100*cos+100)
    return nu.prob1[i][j][k]

def den(z,earth):
    return earth.get_density(g.R_E-z,'PREM')
def fl1(i,cos,f1,e):
    energy=e[i]
    if energy<10**12 and energy>=10. and cos<=1 and cos>=0:
        return f1.get_3D_splain_points(energy,cos)
    else:
        return 0

def fl11(i,cos,z,f1,e):
    a=1-z/g.R_E
    #cos1=((1-2*a*cos+a*a*cos*cos)/(1-2*a*cos+a*a))**0.5
    cos1=(1-a*a+a*a*cos*cos)**0.5
    return fl1(i,cos1,f1,e)


def aaaaaa1(i,cos,z,nu,f1,e):
    a=1-z/g.R_E
    #cos1=((1-2*a*cos+a*a*cos*cos)/(1-2*a*cos+a*a))**0.5
    cos1=(1-a*a+a*a*cos*cos)**0.5
    return fl1(i,cos1,f1,e)*proba(i,cos,z,nu)
def aaaaaa2(i,cos,z,nu,f1,e):
    a=1-z/g.R_E
    #cos1=((1-2*a*cos+a*a*cos*cos)/(1-2*a*cos+a*a))**0.5
    cos1=(1-a*a+a*a*cos*cos)**0.5
    return fl1(i,cos1,f1,e)*proba1(i,cos,z,nu)

def maaaaaa1(i,cos,z,nu,f1,e,kk):
    b=quad(lambda y: aaaaaa1(i-int(np.log10(1-np.exp(y))),cos,z,nu,f1,e)*xs.d2sdiscc_dxdy(e[i],kk,np.exp(y))*10**(-38)*np.exp(y),-10,0)
    print(b[0])
    return 1.678*b[0]
def maaaaaa2(i,cos,z,nu,f1,e,kk):
    b=quad(lambda y: aaaaaa2(i-int(np.log10(1-np.exp(y))),cos,z,nu,f1,e)*xs.d2sdiscc_dxdy(e[i],kk,np.exp(y))*10**(-38)*np.exp(y),-10,0)
    print(b[0])
    return 1.678*b[0]

def omegaxy(energy,x,y):
    return xs.d2sdiscc_dxdy(energy,x,y)**18*1.678*10**(-38)/((10*s.cross_sectioncc(energy)+8*s1.cross_sectioncc(energy)))

def omegay(energy,y):
    b=quad(lambda x: omegaxy(energy,np.exp(x),y)*np.exp(x),-15*np.log(10),0,epsrel=10**(-4))
    return b[0]
def omegax(energy,x):
    b=quad(lambda y: omegaxy(energy,x,np.exp(y))*np.exp(y),-10,0,epsrel=10**(-4))
    return b[0]

def omega(energy):
    c=quad(lambda y:omegay(energy/(1-np.exp(y)),np.exp(y))*np.exp(y),-15,0 )
    return c[0]
def omega1(energy,cos,z,nu,f1,e):
    c=dblquad(lambda y,x: aaaaaa1(int(np.log10(energy/(1-np.exp(y)))),cos,z,nu,f1,e)*omegaxy(energy/(1-np.exp(y)),np.exp(x),np.exp(y))*np.exp(x+y), -15,0,-10,0,epsrel=10**(-3))
    print('integral ',c[0])
    return c[0]

def lll(ne,ny):
    dis = NeutrinoNucleonXsDIS()
    initialize(dis,2212)
    aaa1=np.zeros([ne,ny])
    aaa3=np.zeros([ne,ny])
    aaa2=np.zeros([ne,ny])
    aaa4=np.zeros([ne,ny])
    bbb1=np.zeros([ne,ny])
    bbb2=np.zeros([ne,ny])
    e=np.array([10**(10*i/float(ne-1)) for i in range(ne)])
    y1=np.logspace(-10,-3,num=ny)
    y2=np.linspace(0.001,1,num=ny)
    for i in range(ne):
        for j in range(ny):
            aaa1[i][j]=omegay(e[i],y1[j])
            print('p ',i,j)
    initialize(dis,2112)
    for i in range(ne):
        for j in range(ny):
            aaa2[i][j]=omegay(e[i],y1[j])
            print('n ',i,j)
    initialize(dis,2212)
    for i in range(ne):
        for j in range(ny):
            aaa3[i][j]=omegay(e[i],y2[j])
            print('p ',i,j)
    initialize(dis,2112)
    for i in range(ne):
        for j in range(ny):
            aaa4[i][j]=omegay(e[i],y2[j])
            print('n ',i,j)

    fil=open('ydis3.dat','w')
    bbb1=aaa1+aaa2
    bbb2=aaa3+aaa4
    for i in range(ne):
        for j in range(ny):
            fil.write(str(e[i])+'\t'+str(y1[j])+'\t'+str(bbb1[i][j])+'\n')
    for i in range(ne):
        for j in range(ny):
            fil.write(str(e[i])+'\t'+str(y2[j])+'\t'+str(bbb2[i][j])+'\n')

    fil.close()

    return y1,bbb1

def lllx(ne,nx):
    dis = NeutrinoNucleonXsDIS()
    initialize(dis,2212)
    aaa1=np.zeros([ne,nx])
    aaa2=np.zeros([ne,nx])
    bbb=np.zeros([ne,nx])
    e=np.array([10**(10*i/float(ne-1)) for i in range(ne)])
    x=np.array([10**(15*(i/float(nx-1)-1)) for i in range(nx) ])
    for i in range(ne):
        for j in range(nx):
            aaa1[i][j]=omegax(e[i],x[j])
            print('p ',i,j)
    initialize(dis,2112)
    for i in range(ne):
        for j in range(nx):
            aaa2[i][j]=omegax(e[i],x[j])
            print('n ',i,j)
    fil=open('xdis.dat','w')
    bbb=aaa1+aaa2
    for i in range(ne):
        for j in range(nx):
            fil.write(str(e[i])+'\t'+str(x[j])+'\t'+str(bbb[i][j])+'\n')
    fil.close()

    return x,bbb


def lllm():
    fig=plt.figure()
    for j in range(10):
        a=lll(10**(j))
        plt.scatter(a[0],a[1],label='E = '+str('{:1.1e}'.format(10**j)))
    plt.xlabel('y')
    plt.ylabel('distribution')
    plt.title(r'$\frac{d\sigma}{dy}(E,y)$')
    plt.grid(True)
    plt.xscale('log')
    plt.legend()
    plt.show()

def llll():
    N=1000
    dis = NeutrinoNucleonXsDIS()
    initialize(dis,2212)
    fig=plt.figure()
    bbb=np.zeros(11)
    f1=fff.Flux('KM','flux_data/Numu_H3a+KM_E2.DAT',3)
    aaa=np.zeros([11,21])
    e=np.array([10**(i) for i in range(11)])
    nu=NuPropogator(11,21,1000)
    nu.probability1(N,14,e)
#    y=np.array([10**(10*(i/100.-1)) for i in range(101)])
    for i in range(11):
        for j in range(21):
            a=time.time()
            cos=(-10+j)/10.
            aaa[i][j]=omega1(e[i],cos,1000,nu,f1,e)
            print(time.time()-a)
    for i in range(11):
        bbb[i]=aaa[i].sum()*0.1
    fil = open('muondata1000.dat', 'w')
    for i in range(11):
        fil.write(str(e[i])+'t'+str(bbb[i])+'\n')
    fil.close()


class NuPropogator:
    def __init__(self,m,n,r):
            self.n=n #number of bins for cos\theta
            self.m=m #number of points for energy
            self.r=r #number of points for z
            self.prob=np.zeros([m,n,r])
            self.prob1=np.zeros([m,n,r])
            self.depth=np.zeros([n,r])
            self.zf=np.zeros([m,n,r])
            print('Propogator is ready')
        
    def probability(self,N,flavor,energy,v1,v2):
        a=0
        s=cs.Cross_section(model='CTEQ6.5M',pdg=14,n_tt=1)
        s1=cs.Cross_section(model='CTEQ6.5M',pdg=14,n_tt=2)
        erth=earth.Earth(self.r,'PREM')
        dep=np.zeros([self.n,self.r])
        for j in range(self.n):
            x=time.time()
            dep[j]=erth.column_depth(v1,v2,N)
            a=a+time.time()-x
            print(j,time.time()-x)
        print(a)
        for i in range(self.m):
            self.prob[i]=np.exp(-(s.tot(energy[i])+s1.tot(energy[i]))*g.cm**2*g.N_A*dep/g.g)
    
#    def get_product(self,flavor,P):
#        s=cc.CC()
#        r=kin.Kinematic()
#        final=r.cc_scatter(flavor,P,s)
#        print('lepton: ',final[0])
#        print('hadron',final[1])
        
        
    def probability1(self,N,flavor,energy):
        a=0
        zz=zf1.zf()
        s=cs.Cross_section(model='CTEQ6.5M',pdg=14,n_tt=1)
        s1=cs.Cross_section(model='CTEQ6.5M',pdg=14,n_tt=2)
        erth=earth.Earth(self.r,'PREM')
        dep=np.zeros([self.n,self.r])
        x2=np.zeros(self.r)
        y2=np.zeros(self.r)
        z2=np.array([g.R_E-10*g.m*i for i in range(self.r)])
        for j in range(self.n):
            x=time.time()
            cos=(-(self.n-1.)/2+j)/((self.n-1.)/2)
            x1=np.array([g.R_E*(1-cos**2)**0.5 for i in range(self.r)])
            y1=np.zeros(self.r)
            z1=np.array([g.R_E*cos for i in range(self.r)])
            v1=fin.FinVtx(x1,y1,z1)
            v2=fin.FinVtx(x2,y2,z2)
            dep[j]=erth.column_depth(v1,v2,N)
            a=a+time.time()-x
            print(j,time.time()-x)
        print(a)
        self.depth=dep
        for i in range(self.m):
            for j in range(self.n):
                for k in range(self.r):
                    self.zf[i,j,k]=zz.f(g.g*dep[j][k]/g.cm**2,energy[i])
                print(i,j)


        for i in range(self.m):
            self.prob[i]=np.exp(-(s.tot(energy[i])+s1.tot(energy[i]))*g.cm**2*g.N_A*dep/g.g)
            self.prob1[i]=np.exp(-(s.tot(energy[i])+s1.tot(energy[i]))*(1-self.zf[i])*g.cm**2*g.N_A*dep/g.g)
        
    
    def test(self):
        N=1000
        print('Hello')
        e=np.logspace(1,8,num=self.m)
        self.probability1(N,14,e)
        cos=np.array([(-(self.n-1.)/2+j)/((self.n-1.)/2) for j in range(self.n)])
        for i in range(8):
            fig = plt.figure(figsize=(18,12))
            plt.plot(cos,self.prob[i,:,10],label='without regeneration')
            plt.plot(cos,self.prob1[i,:,10],label='Z-factor regeneration')
            plt.title(' Probability of propogating netrino from surface to z = '+str(100)+'m for E = '+'{:1.1e}'.format(e[i]))
            plt.ylabel(r'$log_{10}(P_{\nu})$')
            plt.xlabel(r'$cos\theta$')
            if(i>=5):
                plt.yscale('log')
            plt.legend()
            plt.grid(True)
            plt.savefig(str(i)+'prob_z.png')
            plt.show()
            plt.close()
    

    def test1(self):
        N=1000
        nuflux=np.zeros([self.m,self.n,self.r])
        print('Hello')
        e=np.array([10**(i/100000.)*g.GeV for i in range(self.m)])
        cos=1.
        x1=np.zeros(self.r)
        x2=np.zeros(self.r)
        y1=np.zeros(self.r)
        y2=np.zeros(self.r)
        z1=np.array([g.R_E for i in range(self.r)])
        z2=np.array([g.R_E-600*g.m*i for i in range(self.r)])
        v1=fin.FinVtx(x1,y1,z1)
        v2=fin.FinVtx(x2,y2,z2)
        self.probability(N,14,e,v1,v2)
        for i in range(10):
            k=10*i
            fig = plt.figure()
            plt.plot(z1-z2,np.log10(self.prob[k,0]),label=r'$E_{\nu}$ = '+str('{:1.2e}'.format(10**(k/10.))))
            plt.ylabel(r'$log_{10}(P_{\nu})$')
            plt.xlabel(r'$cos\theta$')
            plt.legend()
            plt.grid(True)
            plt.savefig('probability/probenergy'+str(k)+'.png')
            plt.show()
            plt.close()


    def testnuflux(self,z):
        N=1000
        e=np.logspace(1,8,num=self.m)
        xxx=np.zeros([self.m,self.n])
        xxx1=np.zeros([self.m,self.n])
        xxx2=np.zeros([self.m,self.n])
        print('Hello')
        self.probability1(N,14,e)
        f1=fff.Flux('KM','flux_data/Numu_H3a+KM_E2.DAT',3)
        cos=np.array([(-(self.n-1.)/2+j)/((self.n-1.)/2) for j in range(self.n)])
        z1=np.array([g.R_E for i in range(self.r)])
        z2=np.array([g.R_E-10*g.m*i for i in range(self.r)])
        for i in range((self.m)):
            for j in range((self.n)):
                k=int(z/10.)
                xxx[i][j]=aaaaaa1(i,cos[j],z1[k]-z2[k],self,f1,e)
                xxx1[i][j]=aaaaaa2(i,cos[j],z1[k]-z2[k],self,f1,e)
                xxx2[i][j]=fl11(i,cos[j],z1[k]-z2[k],f1,e)
                print(i,j,xxx[i][j]-xxx1[i][j])
        for i in [0,50,100,150,200]:
            fig = plt.figure(figsize=(18,12))
            plt.plot(e,xxx[:,i]*e*e,label=r'without regeneration $\cos\theta = $'+str(cos[i]))
            plt.plot(e,xxx1[:,i]*e*e,label=r'Z-factor regeneration $\cos\theta = $'+str(cos[i]))
            plt.plot(e,xxx2[:,i]*e*e,label=r'$F_{\nu}(x=0,E)$ for $\cos\theta$ = '+str(cos[i]))
            #plt.title('Flux of netrino in z = '+str(100)+'m for E = '+'{:1.1e}'.format(e[i]))
            plt.title('Flux of netrino in z = '+str(z)+'m' )
            plt.ylabel(r'$F_{\nu}(x,E)\cdot E_{\nu}^2$,$GeV\cdot cm^2\cdot s^{-1}\cdot sr^{-2}$')
            plt.xlabel(r'$E_{\nu}$, GeV')
            #if i>3:
            plt.yscale('log')
            plt.legend()
            plt.xscale('log')
            plt.grid(True)
            plt.savefig('cos='+str(i)+'flux_z'+str(z)+'.png')
            plt.show()
            plt.close()

        fil=open('prop'+str(z)+'.dat','w')
        fil1=open('prop0.dat','w')
        for i in range(self.m):
            for j in range(self.n):
                fil.write(str(e[i])+'\t'+str(cos[j])+'\t'+str(xxx1[i][j])+'\n')
                fil1.write(str(e[i])+'\t'+str(cos[j])+'\t'+str(xxx[i][j])+'\n')
        fil.close()
#        print('heyyyyyy  ',z/1000.)
#        for i in range(10):
#            fig, (ax0) = plt.figure()
#            fig = plt.figure()
#            k=i
#            for j in range(10):
#                t=40*j+10
#                levels = MaxNLocator(nbins=1000).tick_values(np.log10(self.prob[10*i,:,:]).min(),np.log10(self.prob[10*i,:,:]).max())
#                cmap = plt.get_cmap('inferno')
#                norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
#            im = ax0.pcolormesh(z1-z2,cos, np.log10(self.prob[10*i,:,:]), cmap=cmap, norm=norm)
#            fig.colorbar(im, ax=ax0)
#                plt.scatter(cos,np.log10(xxx[k,:,int(t/10)]),label=r'$h$ = '+str('{:1.2e}'.format(t))+' meters')
#            plt.ylabel(r'$log_{10}(E_{\nu_{mu}})$')
#                ax0.set_title('Probability of propogating netrino from surface to z= '+str(t)+'meters')
#            plt.title('Probability of propogating netrino from surface to h for E= '+str('{:1.1e}'.format(10**(i+1)))+' GeV')
#            plt.ylabel(r'$log_{10}(P_{\nu})$')
#            plt.xlabel(r'$cos\theta$')
#            plt.legend()
#            plt.grid(True)
#            plt.savefig('flux/nuflux'+str(i)+'.png')
#            plt.show()
#            plt.close()

    def testmuflux(self):
        N=1000
        s=cs.Cross_section(model='CTEQ6.5M',pdg=14,n_tt=1)
        s1=cs.Cross_section(model='CTEQ6.5M',pdg=14,n_tt=2)

        dis = NeutrinoNucleonXsDIS()
        dis1 = NeutrinoNucleonXsDIS()
        initialize(dis,2212)
        xxx=np.zeros([self.m,self.n,self.r,101])
        print('Hello')
        e=np.array([10**(i+1)*g.GeV for i in range(self.m)])
        self.probability1(N,14,e)
        f1=fff.Flux('KM','flux_data/Numu_H3a+KM_E2.DAT',3)
        cos=np.array([(-(self.n-1.)/2+j)/((self.n-1.)/2) for j in range(self.n)])
        z1=np.array([g.R_E for i in range(self.r)])
        z2=np.array([g.R_E-10*g.m*i for i in range(self.r)])

        for i in range((self.m)):
            for j in range((self.n)):
                for k in range(self.r):
                    for kk in range(16):
                        xxx[i][j][k][kk]=maaaaaa1(i,cos[j],z1[k]-z2[k],self,f1,e,10**(15*(kk/15.-1)))/((s.cross_sectiontot(e[i])+s1.cross_sectiontot(e[i]))*g.cm**2)
                        xxx[i][j][k][kk]=maaaaaa1(i,cos[j],z1[k]-z2[k],self,f1,e,10**(15*(kk/15.-1)))/((s.cross_sectiontot(e[i])+s1.cross_sectiontot(e[i]))*g.cm**2)
                print(i,j)
#        for i in range(10):
#            fig, (ax0) = plt.figure()
#            fig = plt.figure()
#            k=i
#            for j in range(16):
                
#                levels = MaxNLocator(nbins=1000).tick_values(np.log10(self.prob[10*i,:,:]).min(),np.log10(self.prob[10*i,:,:]).max())
#                cmap = plt.get_cmap('inferno')
#                norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
#            im = ax0.pcolormesh(z1-z2,cos, np.log10(self.prob[10*i,:,:]), cmap=cmap, norm=norm)
#            fig.colorbar(im, ax=ax0)
#                plt.scatter(cos,np.log10(xxx[k,:,5,j]),label=r'$x$ = '+str('{:1.2e}'.format(10**(15*(j/15.-1)))))
#            plt.ylabel(r'$log_{10}(E_{\nu_{mu}})$')
#                ax0.set_title('Probability of propogating netrino from surface to z= '+str(t)+'meters')
#            plt.title('Probability of propogating netrino from surface to h for E= '+str('{:1.1e}'.format(10**(i+1)))+' GeV')
#            plt.ylabel(r'$log_{10}(P_{\nu})$')
#            plt.xlabel(r'$cos\theta$')
#            plt.legend()
#            plt.grid(True) 
#            plt.savefig('flux/muflux'+str(i)+'.png')
#            plt.show()
#            plt.close()

    def testmuflux1(self):
        N=1000
        s=cs.Cross_section(model='CTEQ6.5M',pdg=14,n_tt=1)
        s1=cs.Cross_section(model='CTEQ6.5M',pdg=14,n_tt=2)
        
        dis = NeutrinoNucleonXsDIS()
        dis1 = NeutrinoNucleonXsDIS()
        initialize(dis,2212)
        xxx=np.zeros([self.m,self.n,self.r,101])
        print('Hello')
        e=np.array([10**(i+1)*g.GeV for i in range(self.m)])
        self.probability1(N,14,e)
        f1=fff.Flux('KM','flux_data/Numu_H3a+KM_E2.DAT',3)
        cos=np.array([(-(self.n-1.)/2+j)/((self.n-1.)/2) for j in range(self.n)])
        z1=np.array([g.R_E for i in range(self.r)])
        z2=np.array([g.R_E-1*g.m*i for i in range(self.r)])
        for i in range((self.m)):
            for j in range((self.n)):
                for k in range(self.r):
                    for kk in range(11):
                        xxx[i][j][k][kk]=maaaaaa1(i,cos[j],z1[k]-z2[k],self,f1,e,10**(15*(kk/100.-1)))/(s.cross_sectiontot(e[i])+s1.cross_sectiontot(e[i]))
                print('cccccccccccccccccccc',i,j)
        for i in range(10):
            fig = plt.figure()
            k=i
            for j in range(10):
                t=40*j+10
                plt.scatter(cos,np.log10(xxx[k,:,int(t/10)]),label=r'$h$ = '+str('{:1.2e}'.format(t))+' meters') 
            plt.title('Probability of propogating netrino from surface to h for E= '+str('{:1.1e}'.format(10**(i+1)))+' GeV')
            plt.ylabel(r'$log_{10}(P_{\nu})$')
            plt.xlabel(r'$cos\theta$')
            plt.legend()
            plt.grid(True)
            plt.savefig('flux/muflux'+str(i)+'.png')
            plt.show()
            plt.close()




nu=NuPropogator(8,201,200)
#nu.test()
#nu.prob
#nu.testnuflux(1000000)
nu.testnuflux(1000)
#lll(111,101)
