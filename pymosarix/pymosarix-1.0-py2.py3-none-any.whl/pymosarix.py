#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 18:47:48 2021

@author: iyas
"""
# -*- coding: utf-8 -*-
"""
permet d'aficher une image 2D avec les deux projection x, y avec la possibilité 
de choisir un ROI qui sera suivi sur les deux projections

l'histogramme de l'intensité de l'image est caclulé aussi avec la possibilité de choisir
certaine intensités

Iyas ISMAIL, 06 nov 2021
'
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import pyqtgraph.parametertree as ptree
import pyqtgraph.graphicsItems.ScatterPlotItem


import numpy as np
from IPython.display import clear_output, display

import scipy.optimize
#import matplotlib.pyplot as plt
import numpy as np



from scipy.special import wofz , voigt_profile
from scipy import signal 

from scipy.optimize import curve_fit



from pylab import * 

import tables


from time import sleep

import os
from tqdm import tqdm
from scipy import interpolate

import pickle
translate = QtCore.QCoreApplication.translate



class image2D_proj():
    
    def __init__(self, data, extent=None):
        self.nbrofROIS =9
        self.gwidth=[]
    


        # Interpret image data as row-major instead of col-major
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.data=data
        
        self.spectre=[]
        
        pg.mkQApp()
        
        self.win = pg.GraphicsLayoutWidget()
        
        self.label = pg.LabelItem(justify='right') 
        
        
        
        
        
        self.win.show()
        
        self.win2 = pg.GraphicsLayoutWidget()
        
        
        self.win2.show()
        
        #p1 = win.addViewBox(row=1, col=0)
        self.p1 = self.win.addPlot(row=1, col=0)
        
        self.p2 = self.win.addPlot(row=1, col=1)
        self.p3 = self.win.addPlot(row=2, col=0)
        
        self.p333 = self.win2.addPlot(row=1, col=0, colspan=self.nbrofROIS+1)
        self.p332 = self.win2.addPlot(row=4, col =0, colspan=self.nbrofROIS+1)

        self.label333 = pg. LabelItem()
        
        self.label333.setText('HelloIyas')
        
       # self.win2.addItem(self.label333)
        
        
        
        
        self.checkbox_ =[]
        self.couleurs = ['red','blue', 'yellow','darkviolet','white','green','cyan','magenta','orange']

        
        for i in range (self.nbrofROIS):
        
            checkbox = QtWidgets.QCheckBox(str(i))
            checkbox.setPalette(QtGui.QPalette(QtGui.QColor(self.couleurs[i])))# QColor(255,0,0)))

            
            self.checkbox_.append (checkbox)

            proxy = QtWidgets.QGraphicsProxyWidget()

            proxy.setWidget(self.checkbox_[-1])

            self.win2.addItem(proxy, row=0,col=i)
            
            
       
        checkbox = QtWidgets.QCheckBox('fit')
        checkbox.setPalette(QtGui.QPalette(QtGui.QColor('greenyellow')))# QColor(255,0,0)))

            
        self.checkbox_.append (checkbox)

        proxy = QtWidgets.QGraphicsProxyWidget()

        proxy.setWidget(self.checkbox_[-1])
        

        self.win2.addItem(proxy, row=0,col=i+1)
        
        
        self.button1 =  QtWidgets.QPushButton('reset')


        self.button1.setPalette(QtGui.QPalette(QtGui.QColor('greenyellow')))# QColor(255,0,0)))

            

        proxy = QtWidgets.QGraphicsProxyWidget()

        proxy.setWidget(self.button1)
        

        self.win2.addItem(proxy, row=4,col=i+2)
        
            
        self.p333.setLabel( 'left', 'Counts') 
        self.p333.setLabel('bottom', 'pixel', units='eV')
            
        self.p332.setLabel( 'left', 'Counts') 
        self.p332.setLabel('bottom', 'pixel', units='eV')
        
            
            
            
            
            



        




        
        self.label = pg.LabelItem(justify="right")
        self.p2.addItem(self.label)
        self.label.setText('Hello')
        
        
        # restrict size of plot areas
        self.win.ci.layout.setColumnMaximumWidth(1, 100)
        self.win.ci.layout.setRowMaximumHeight(2, 100)
        
        # force central viewbox and side plots to have matching coordinate systems
        #self.p2.setXLink(self.p1)  
        #self.p3.setYLink(self.p1)
        
        
        
        
        
        # A plot area (ViewBox + axes) for displaying the image
        
        # Item for displaying image data
        self.img = pg.ImageItem()
        self.p1.addItem(self.img, axisOrder='row-major')
        #from pgcolorbar.colorlegend import ColorLegendItem
        
       # from pgcolorbar.colorlegend import ColorLegendItem
        
        
        
        self.text0 = pg.LabelItem("this is a LabelItem", color='w')
        self.text0.setPos(0, 0)  # <---- These are coords within the IMAGE
        self.win.addItem(self.text0, row=0, col=0)
        
        
        self.text1 = pg.LabelItem("this is a LabelItem", color='w')
        self.text1.setPos(0, 0)  # <---- These are coords within the IMAGE
        self.win2.addItem(self.text1, row=3, col=0, colspan=2)
        
        
        
        # Generate image data
        #self.data = np.random.normal(size=(200, 100))+temp
        #self.data[20:80, 20:80] += 2.
        #self.data = pg.gaussianFilter(self.data, (3, 3))
        #self.data += np.random.normal(size=(200, 100)) * 0.1
        self.img.setImage(self.data)
        
        if (extent==None):
            xmin=ymin=0
            xd = self.data.shape[1]
            yd= self.data.shape[0]
            print (xd, yd)
        else:
            xmin=extent[0]
            xmax = extent[1]
            xd = xmax -xmin  # c'est en effet le delta
            
            ymin=extent[2]
            ymax=extent[3]
            yd = ymax-ymin
        
        self.img.setRect(QtCore.QRectF(0, 0, 195, 487  ))
        self.ROIS = []
        
        
        
        # Custom ROI for selecting an image region
       # roi = pg.ROI([xmin, ymin],[195, 487 ], pen='r') 
        
       # self.ROIS.append(roi)
        
       # col = ['red','blue', 'yellow','darkviolet','white','green','cyan','magenta','orange']

        
        for i in range (self.nbrofROIS):
            
        
        
            roi2 = pg.ROI([xmin, 4+ymin+i* 487/10],[195, 487/10 ], pen=self.couleurs[i]) 


            roi2.addScaleHandle([0.5, 1], [0.5, 0.5])
            roi2.addScaleHandle([0, 0.5], [0.5, 0.5])
            roi2.addRotateHandle([1, 1], [0.5, 0.5])
            self.p1.addItem(roi2)
            roi2.setZValue(20)  # make sure ROI is drawn above image
            roi2.sigRegionChanged.connect(self.updatePlot)

            self.ROIS.append(roi2)
            
        for i in range (self.nbrofROIS+1):

            self.checkbox_[i].stateChanged.connect(self.updatePlot)


        #self.roi = pg.ROI([0, 0], [ self.img.width(), self.img.height()]) 
        #self.ROIS[0].addScaleHandle([0.5, 1], [0.5, 0.5])
        #self.ROIS[0].addScaleHandle([0, 0.5], [0.5, 0.5])
        #self.ROIS[0].addRotateHandle([1, 1], [0.5, 0.5])
        #self.p1.addItem(roi)
        #self.ROIS[0].setZValue(10)  # make sure ROI is drawn above image
        
        # Isocurve drawing
        self.iso = pg.IsocurveItem(level=0.8, pen='g')
        self.iso.setParentItem(self.img)
        self.iso.setZValue(5)
        
        # Contrast/color control
        self.hist = pg.HistogramLUTItem()
        
        # Draggable line for setting isocurve level
        #isoLine = pg.InfiniteLine(angle=0, movable=True, pen='g')
        #hist.vb.addItem(isoLine)
        #self.hist.vb.setMouseEnabled(y=False) # makes user interaction a little easier
        #isoLine.setValue(0.8)
        #isoLine.setZValue(1000) # bring iso line above contrast controls
        
        # Another plot area for displaying ROI data
        
        self.hist.setLevels(self.data.min(), self.data.max())

        
        
        self.hist.setImageItem(self.img)
        
        self.hist. disableAutoHistogramRange()
        
        self.hist.gradient.loadPreset('viridis')

        
        self.win.addItem(self.hist,row=1, col=2)
        
        # build isocurves from smoothed data
        #iso.setData(pg.gaussianFilter(data, (2, 2)))
        
        # set position and scale of image
        #tr = QtGui.QTransform()
        #img.setTransform(tr.scale(0.2, 0.2).translate(-50, 0))
        
        # zoom to fit imageo
        self.p1.autoRange()  
        
        self.ROIS[0].sigRegionChanged.connect(self.updatePlot)
        self.updatePlot()
        self.img.hoverEvent = self.imageHoverEvent
        self.hist.sigLookupTableChanged.connect(self.handle_sigLookupTableChanged)
        
        self.button1.clicked.connect(self.remiseazero)
        
        self.win2.setGeometry (200,200, 600, 600)
        
    

    def save_rois(self, roisfilename=None):
        
        

        roissave=[]
        for i in range (len(self.ROIS)):
            roissave.append(self.ROIS[i].pos())
            roissave.append(self.ROIS[i].size())
        if (roisfilename==None):
            roisfilename= 'roissave'
        
        
        np.savetxt(roisfilename, roissave)

    def load_rois(self, roisfilename=None):
        
        
        

        
        print ('load rois')
        if (roisfilename==None):
            roissave=np.loadtxt('roissave')
        else:
             roissave=np.loadtxt(roisfilename)
        for i in range (len(self.ROIS)):

            if (i<len(roissave)//2):
                self.ROIS[i].setPos(roissave[2*i])
                self.ROIS[i].setSize(roissave[2*i+1])
            else:
                self.ROIS[i].setPos(0)
                self.ROIS[i].setSize(0)
                
    def remiseazero(self):
        self.gwidth=[0]
        self.p332. plot( self.gwidth , clear=True)
        
        
        





        
        
        
    def handle_sigLookupTableChanged(self):
        if (0):
            colours = self.hist.getLookupTable(img=self.data)
            cmap = pg.ColorMap(
                pos=np.linspace(*self.hist.getLevels(), len(colours)),
                color=colours,)

        selected = self.ROIS[0].getArrayRegion(self.data, self.img)

        sumyaxis = selected.mean(axis=1)
        sumxaxis = selected.mean(axis=0)

        
        
        c = cmap.map(sumyaxis, "qcolor")
        self.p2.opts["symbolBrush"] = c
        #self.p2.updateItems()
        
        c = cmap.map(sumxaxis, "qcolor")
        self.p3.opts["symbolBrush"] = c
        #self.p3.updateItems()
     
      
      
    def dessinerimage(self, data, extent=None, cscale=None):
        
    
        self.data = data

        # Interpret image data as row-major instead of col-major
        
        
        
        # A plot area (ViewBox + axes) for displaying the image
        
        # Item for displaying image data
         
        self.img.setImage(data, autoRange=False)
        
        if (extent==None):
            xmin=ymin=0
            xd = self.data.shape[0]
            yd= self.data.shape[1]
        else:
            xmin=extent[0]
            xmax = extent[1]
            xd = xmax -xmin  # c'est en effet le delta
            
            ymin=extent[2]
            ymax=extent[3]
            yd = ymax-ymin
        
        self.img.setRect(QtCore.QRectF(0, 0, 195, 487  ))
        
        # Custom ROI for selecting an image region

        #self.roi = pg.ROI([0, 0], [ self.img.width(), self.img.height()]) 
        
       # self.ROIS[0].setPos([0, 0])
       # self.ROIS[1].setPos([0, 0])

        
       # self.ROIS[0].setSize([  195, 487])
       # self.ROIS[1].setSize([ 195, 487])

        
       # self.ROIS[1].setSize([  self.img.height(), self.img.width()/2])

        # Contrast/color control
        
        # Draggable line for setting isocurve level
        #isoLine = pg.InfiniteLine(angle=0, movable=True, pen='g')
        #hist.vb.addItem(isoLine)
        #self.hist.vb.setMouseEnabled(y=False) # makes user interaction a little easier
        #isoLine.setValue(0.8)
        #isoLine.setZValue(1000) # bring iso line above contrast controls
        
        # Another plot area for displaying ROI data
        
        print (self.data.min(), self.data.max())
        #self.hist.setLevels(self.data.min(), self.data.max())
        
        #hist.setLevels(90,102)
        
        self.hist.setImageItem(self.img)
        
        self.updatePlot()
        #if (not(cscale==None)):
        
            #self.hist.setLevels(cscale[0],cscale[1])


        
        # build isocurves from smoothed data
        #iso.setData(pg.gaussianFilter(data, (2, 2)))
        
        # set position and scale of image
        #tr = QtGui.QTransform()
        #img.setTransform(tr.scale(0.2, 0.2).translate(-50, 0))
        
        # zoom to fit imageo
        #self.p1.autoRange()  
        #self.p2.autoRange()  
        #self.p3.autoRange()  


        


    
    # Callbacks for handling user interaction
    def updatePlot(self):
       # global img, roi, data, p2
        self.spectre=[]
        self.selectedt=[]

       
        for i in range (len (self.ROIS)):
                    pos = self.ROIS[i].parentBounds()

                    selected = self.ROIS[i].getArrayRegion(self.data, self.img)
                    self.selectedt.append(selected)
                    s= selected.sum(axis=0)

                    x = np.linspace( int(pos.left()), int(pos.right()),num=len(s))


                    self.spectre.append(np.c_[x,s])
           
        
        
        
        # x = np.arange (pos.left(), pos.right(),1)
        # y = np.arange (pos.top(), pos.bottom(),1)
        
        
            
            
            
            
        
        if (self.checkbox_[0].isChecked()):

            pos = self.ROIS[0].parentBounds()
            selected = self.ROIS[0].getArrayRegion(self.data, self.img)
        else: 
            pos = self.ROIS[1].parentBounds()
            selected = self.ROIS[1].getArrayRegion(self.data, self.img)

            
        xproj=selected.sum(axis=1)
        yproj = selected.sum(axis=0)
        
            
            
        
        
        
        #self.colours = self.hist.getLookupTable(img=self.data)
        #self.cmap = pg.ColorMap(pos=np.linspace(self.hist.getLevels()[0], self.hist.getLevels()[1], len(self.colours)), color=self.colours)
        x = np.linspace( int(pos.left()), int(pos.right()),num=len(selected.mean(axis=0)))
        y = np.linspace( int (pos.top()), int (pos.bottom()),num=len(selected.mean(axis=1)))

        #self.c = self.cmap.map(yproj, 'qcolor')
        #self.c1 = self.cmap.map(xproj, 'qcolor')


        
        
       
        
        self.p2.plot(xproj, y,clear=True, pen=pg.mkPen('b', width=10))
        #self.p2.plot(xproj,y , symbol='o',symbolSize=1, pen=None, clear=True)

       
        #self.p3.plot( x, yproj , symbol='o',symbolSize=1, pen=None, clear=True)
        self.p3.plot( x, yproj , clear=True, pen=pg.mkPen('r', width=10))
        
        first = True
        #col = ['r','b', 'y','k','w','g','c','m','b']
        #col = ['red','blue', 'yellow','darkviolet','white','green','cyan','magenta','orange']

        for i in range (self.nbrofROIS):
            if (self.checkbox_[i].isChecked()) :
                pos = self.ROIS[i].parentBounds()
                selected = self.ROIS[i].getArrayRegion(self.data, self.img)
                
                xproj=selected.sum(axis=1)
                yproj = selected.sum(axis=0)
        
            
            
        
        
        
                #self.colours = self.hist.getLookupTable(img=self.data)
                #self.cmap = pg.ColorMap(pos=np.linspace(self.hist.getLevels()[0], self.hist.getLevels()[1], len(self.colours)), color=self.colours)
                x = np.linspace( int(pos.left()), int(pos.right()),num=len(selected.mean(axis=0)))
                y = np.linspace( int (pos.top()), int (pos.bottom()),num=len(selected.mean(axis=1)))
               
                if (first):
                    self.p333.plot( x, yproj , clear=True, pen=pg.mkPen(self.couleurs[i], width=10))
                    
                    
                    if (self.checkbox_[-1].isChecked()):
                        self.p332.show()
                        self.button1.show()
                        g1= self.fitme(x, yproj) [2]
                        
                        g2= self.fitme(x, yproj) [1]

 
                        self.text1.setText( 'FWHM ' +"{:10.2f}".format(g1) +'; pos'+"{:10.2f}".format(g2) )
                        self.gwidth.append (g1)
                    else:
                        self.p332.hide()
                        self.button1.hide()
        

                    first = False
                else:
                    self.p333.plot( x, yproj , clear=False, pen=pg.mkPen(self.couleurs[i], width=10))

                self.p332.plot( self.gwidth , clear=False, pen=pg.mkPen(self.couleurs[i], width=10))
    


        #self.hist.setLevels(self.data.min(), self.data.max())
     
        #self.hist.setImageItem(self.img)
        
        #self.p1.autoRange()  
        #self.p2.autoRange()  
        #self.p3.autoRange()  


        
        # self.p2.plot(selected.mean(axis=1), np.arange(len(selected.mean(axis=1))),clear=True, pen=pg.mkPen('b', width=15))
       
        # self.p3.plot(selected.mean(axis=0), clear=True,  pen=pg.mkPen('w', width=15))
        

        
    
    
    
    
    def imageHoverEvent(self,event):
        """Show the position, pixel, and value under the mouse cursor.
        
        """
       # global p1
        if event.isExit():
            #p1.setTitle("")
            return
        pos = event.pos()
        i, j = pos.y(), pos.x()
        i = int(np.clip(i, 0, self.data.shape[0] - 1))
        j = int(np.clip(j, 0, self.data.shape[1] - 1))
        val = self.data[i, j]
       # ppos = self.img.mapToParent(pos)
        #x, y = ppos.x(), ppos.y()
        #self.text0.setText("pos: (%0.1f, %0.1f)  pixel: (%d, %d)  value: %.3g" % (x, y, i, j, val))
        
        self.text0.setText(" pixel: (%d, %d)  value: %.3g" % ( j, i, val))
        # self.p1.autoRange()  
        # self.p2.autoRange()  
        # self.p3.autoRange()  
    def fitGauss(self, x,y,p0, plotting = True, verbose = True) :
        '''
        Fits a gaussian profile to a peak. 
        format: fitGauss(x,y,p0)
        where x and y are the x and y arrays of the data coordiantes respectively.
        p0 is an array specifiying the initial values of Amplitude,Position,Sigma and Background of the Gaussian profile.
        example: fitGauss(x,y,[1000,0.2,1.5,10]) 
        ''' 
        fitfunc=lambda A,x: A[0]*np.exp(-((x-A[1])**2)/2/A[2]**2)+A[3]
        errfunc=lambda A,x,y:fitfunc(A,x)-y
        result,success=scipy.optimize.leastsq(errfunc,p0,args=((x,y))) 
        if plotting:
            plt.plot(x,fitfunc(result,x),'r-')
            self.p333.plot( x,fitfunc(result,x), clear=False, pen=pg.mkPen('white', width=4))
            
            
        if verbose:
            print('Amplitude = %f \nPosition = %f \nFWHM = %f\nBackground = %f' %(result[0],result[1],result[2]*2.35482,result[3]))
        return np.array([result[0],result[1],result[2],result[3]])

    def fitme(self, x = [], y = [], fun='gauss', plotting = True, verbose=True):
        '''
        Fits a Gaussian profile to a peak. It automatically calculates the initial values for the Amplitude, Position, FWHM and Background of the Gaussian profime.
        It uses the fitGauss function.
        format: fitme(x,y)
        fun : gauss / lorenz / pseudovoigt
        where x and y are the x and y arrays of the data coordiantes respectively.
        '''

        if x == [] and y == [] :
            ax = plt.gca()
            line = ax.get_lines()[-1]
            x = line.get_xdata()
            y = line.get_ydata()
        else :
            x = x
            y = y
            plotting = True

        if np.average(np.gradient(x)) < 0 : 
            x = x[::-1]
            y = y[::-1]

        xn = (x - np.min(x)) / float(np.max(x - np.min(x)))
        yn = (y - np.min(y)) / float(np.max(y - np.min(y)))

        step = np.round(np.abs(min(xn)-max(xn))/len(xn),4)

        ene = np.arange(0,1,step/2)
        yi = np.interp(ene,xn,yn)

        w1 = np.min(ene[np.argwhere(np.abs(yi-0.5)<0.15)])
        w2 = np.max(ene[np.argwhere(np.abs(yi-0.5)<0.15)])
        width = np.abs(w2-w1)*np.max(x - np.min(x))
        p0=[np.max(y),x[np.argmax(y)],width/2.35482,np.min(y)]    

        if fun=='gauss':
            r = self.fitGauss(x,y,p0, plotting, verbose)
        elif fun =='lorenz':
            r = self.fitLorenz(x,y,p0,verbose)
        elif fun =='pseudovoigt':
            r = self.fitPseudoVoigt(x,y,[p0[0]/2,p0[1],p0[2],p0[3],p0[0]/2,p0[2],0.5],verbose)
        return r






    def G(self,x,x0, alpha):
    #""" Return Gaussian line shape at x with HWHM alpha """ 
        return np.sqrt(np.log(2) / np.pi) / alpha\
        * np.exp(-((x-x0) / alpha)**2 * np.log(2)) # """ Return Lorentzian line shape at x with HWHM gamma """ 

    def L(self,x,x0, gamma):
        return gamma / np.pi / ((x-x0)**2 + gamma**2) 

    def V1(self,x,x0, alpha, gamma): 

       # Return the Voigt line shape at x with Lorentzian component HWHM gamma
       # and Gaussian component HWHM alpha.

        sigma = alpha/ np.sqrt(2 * np.log(2))
        return np.real(wofz(((x-x0) + 1j*gamma)/sigma/np.sqrt(2))) / sigma\
                /np.sqrt(2*np.pi)

    def V(self,x,x0, alpha, gamma): 

       # Return the Voigt line shape at x with Lorentzian component HWHM gamma
       # and Gaussian component HWHM alpha.

        sigma = alpha/ np.sqrt(2 * np.log(2))

        # Normal distribution with standard deviation sigma
        #1-D Cauchy distribution with half-width at half-maximum gamma.



        return self.voigt_profile(x-x0,sigma, gamma)


    # Gtest2, image 257

    #Gtest1, im 470
    # resolution avec Kalpha

    # a good one with 2 Voigts and fixed positions

    plt.figure(figsize=(10,5))


    txt2 = '2vgts_Pfixed'

    def fit_func(self, x,A0,A1,off,alpha,x0,x1):
        gamma0 = 0.612/2 # Kavcic et al. 2021

        return A0* self.V(x,x0, alpha, gamma0)+ A1* V(x,x1, alpha, gamma0) +off 


    # these are the same as the scipy defaults

    #p1 = [21000.1,1]


    def fitmeV(self,x_,y_,xlim0,xlim1, x0,x1):
        # fit avec 2 voigts defini dans fit_func


        initialParameters = [2/3, 1/3,0,1, x0, x1]
        i=4
        #plt.plot ( en[i]/2, s[i]/s[i].max())


        selx = np.where ( (x_>(xlim0))& (x_<(xlim1)) )  
        x = x_[selx]
        y = y_[selx]/y_[selx].max()


        # curve fit the test data
        fittedParameters, pcov = curve_fit(self.fit_func, xdata= x, ydata=(y), p0=initialParameters)
        plt.rcParams['font.size'] = 12

        plt.plot (x,y, label ='exp, Gtest2, im 257', linewidth=4)


        #A 0,A1,off,alpha,x0,x1

        A0= fittedParameters[0]
        A1 = fittedParameters[1]
        off = fittedParameters[2]

        alpha= fittedParameters[3]
        x0 = fittedParameters[4]
        x1 = fittedParameters[5]


        plt.plot (x,self.fit_func(x,*fittedParameters),label = 'fit sum' )

        plt.plot (x, A0*V (x,x0,alpha, 0.612/2 ) , label='voigt0')
        plt.plot (x, A1*V (x,x1,alpha, 0.612/2 ) , label='voigt1')



        print ('FWHM Gaussian',2*alpha)
        #Kalp =0.67

        resol = 2*alpha
        print ('spectro resolution', f' resol: {resol:.2f} eV' )

        print (f'resolving power : {2300/resol:.2f}' )
        plt.xlabel('energy eV')

        print('intensity ratio ',A1/A0)

        plt.ylabel('Intensity arr. unit')


        plt.legend()
        return fittedParameters, 2*fittedParameters







# Monkey-patch the image to use our custom hover function. 
# This is generally discouraged (you should subclass ImageItem instead),
# but it works for a very simple use like this. 





class pymosarix( image2D_proj):
    def __init__(self):
        self.cutv =1e3


        self. app = pg.mkQApp('MOSARIX')
        
        
        
        
        self.foldername = '/Users/iyas/LCPMR/LCPMR/Galaxies dec 2021/images/'

        try:
            self.cal = np.loadtxt('cal')
        except:
            self.cal=0
            
        
        self.timer2 = pg.QtCore.QTimer()
                
        self.P={'energy':3000, 'theta':30,'deuxtheta':60, 'Ldet':500,'Lcry': 300, 'Phidet':0, 'offsetdet':30,'offsetcry':40, 'cry1':[20,20,90]}

    
    
        self.param = ptree.Parameter.create(name=translate('ScatterPlot', 'Parameters Detecteur'), type='group', children=[
        dict(name='record', title=translate('ScatterPlot', 'Paused:    '), type='bool', value=False),
        dict(name='filename', title=translate('ScatterPlot', 'Filename:'), type='str', value='Filename'),
        dict(name='pathname', title=translate('ScatterPlot', 'Root folder:    '), type='str', value=self.foldername ),

        dict(name='index', title=translate('ScatterPlot', 'image index:    '), type='int', value=0), 
        dict(name='ExposureTime', title=translate('ScatterPlot', 'ExposureTime:    '), type='float', limits=[None, None], value=1, step=0.1,decimals=5),
        dict(name='ExposurePeriod', title=translate('ScatterPlot', 'ExposurePeriod:    '), type='float', limits=[1, None], value=1.05, step=1, decimals=5),
        
        dict(name='MultiImages', title=translate('ScatterPlot', 'MultiImages:    '), type='bool',  value=False, step=1),
    
        dict(name='NumberofImages', title=translate('ScatterPlot', 'Number of Images:    '), type='int', limits=[1, None], value=1, step=1),
        dict(name='Z', title=translate('ScatterPlot', 'Zscale:    '), type='bool', value=False),
        dict(name='minZ', title=translate('ScatterPlot', 'Minz:    '), type='int', limits=[None, None], value=1, step=1),
        dict(name='maxZ', title=translate('ScatterPlot', 'maxZ:    '), type='int', limits=[None, None], value=1, step=1),
    
        dict(name='mode', title=translate('ScatterPlot', 'Mode:    '), type='list', limits={translate('ScatterPlot', 'New Item'): 'newItem', translate('ScatterPlot', 'Reuse Item'): 'reuseItem', translate('ScatterPlot', 'Simulate Pan/Zoom'): 'panZoom', translate('ScatterPlot', 'Simulate Hover'): 'hover'}, value='reuseItem'),
            

    ])
        
        
        self.param2 = ptree.Parameter.create(name=translate('ScatterPlot2', 'Autocalibration:'), type='group', children=[
        dict(name='firstfile', title=translate('ScatterPlot2', 'first image index:'), type='int', value=0), 
        dict(name='lastfile', title=translate('ScatterPlot2', 'last image index:'), type='int', value=10), 
        dict(name='firstenergy', title=translate('ScatterPlot2', 'first energy:'), type='float', limits=[0, None], value=2300, step=0.1,decimals=5),
        dict(name='lastenergy', title=translate('ScatterPlot2', 'last energy:'), type='float', limits=[0, None], value=2500, step=0.1,decimals=5),
        dict(name='energystep', title=translate('ScatterPlot2', 'step energy:'), type='float', limits=[None, None], value=1, step=0.1,decimals=5)])
        

        self.load_paramters()
        
        for c in self.param.children():
            c.setDefault(c.value())
        
        #self.saveBtn = QtGui.QPushButton('expose')
        #self.saveBtn.clicked.connect(self.expose)
        
        #self.saveBtn_0 = QtGui.QPushButton('start live')
        #self.saveBtn_0.clicked.connect(self.startlive)
        
        #self.saveBtn_1 = QtGui.QPushButton('stop live')
        #self.saveBtn_1.clicked.connect(self.stoplive)


        
        #self.saveBtn2 = QtGui.QPushButton('open')
        #self.saveBtn2.clicked.connect(self.openfile)
        
        self.saveBtn22 = QtWidgets.QPushButton('open #i image')
        

        self.saveBtn22.clicked.connect(self.openfileoffline)
        
        
        self.saveBtn222 = QtWidgets.QPushButton('open nxs file')
        self.saveBtn222.clicked.connect(self.openfileoffline22)
        
        self.saveBtn222.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')


       # self.saveBtn3 = QtGui.QPushButton('refresh')
        #self.saveBtn3.clicked.connect(self.refreshimage)

        
        
       # self.saveBtn4 = QtGui.QPushButton('disconnect')
        #self.saveBtn4.clicked.connect(self.close)

        
        self.saveBtn6 = QtWidgets.QPushButton('Auto Calibration')
        self.saveBtn6.clicked.connect(self.auto_calibbtn)

        
        
        
        #self.saveBtn5 = QtGui.QPushButton('Get Temp')
        #self.saveBtn5.clicked.connect(self.update_temp)

        
        
        
        self.pt = ptree.ParameterTree(showHeader=False)
        self.pt.setParameters(self.param)
        self.pt.addParameters(self.param2)

        
        
       
        
        #w.resize(100, 100)
        #w.show()
        
        self.w1 = pg.LayoutWidget()
        
        
        self.label1 = QtWidgets.QLabel('Temps en °C')
        
        self.label1.setText('Hello')
        
        #w1 = QtWidgets.QSplitter()
        self.w1.addWidget(self.pt, row=0, col=0)
        #self.w1.addWidget(self.pt2, row=1, col=0)

        #w1.addWidget(p)
        
        self.p3 = self.w1.addLayout(row=1+1, col=0)
        self.p4 = self.w1.addLayout(row=2+1, col=0)
        
        
        
        #self.p3.addWidget(self.saveBtn, row=0+1, col=0)
        
        #self.p3.addWidget(self.saveBtn_0, row=3+1, col=0)
        #self.p3.addWidget(self.saveBtn_1, row=3+1, col=1)


        #self.p3.addWidget(self.saveBtn2, row=1+1, col=0)
        self.p3.addWidget(self.saveBtn22, row=2, col=0)
        self.p3.addWidget(self.saveBtn222, row=1, col=0)

       # self.p3.addWidget(self.saveBtn3, row=0+1, col=1)
        
       # self.p3.addWidget(self.saveBtn4, row=1+1, col=1)
        
        self.p3.addWidget(self.saveBtn6, row=1+1, col=3, colspan=2)
        
        
        
        
        #self. p4.addWidget(self.saveBtn5, row=0+1, col=0)
        
        self.p4.addWidget(self.label1, row=0+1, col=1)
        
        
        
        self.w = pg.GraphicsLayoutWidget( show=True, border=0.5, size=(5,5) )
        
        self.w1.show()
        
        self.timer = QtCore.QTimer()
    
        self.timer.timeout.connect(self.update)
    
        for c in self.param.children():
            c.setDefault(c.value())
        
        
        
        for c in self.param.children():
           
            self.param.child(c.name()).sigValueChanged.connect(self.update)
            
        
        self.param.child('index').sigValueChanged.connect(self.openfileoffline )
        
        # Generate image data
        data = np.random.normal(size=(200, 100))+100
        data[20:80, 20:80] += 2.
        data = pg.gaussianFilter(data, (3, 3))
        data += np.random.normal(size=(200, 100)) * 0.1
        
        self.data=data
                
        self.cubedata = []
        self.energies = []
        
        extent =[0,100,0,100]
        self.img2D= image2D_proj(data)
        
        self.saveBtn61 = QtWidgets.QPushButton('save ROIS')
        self.saveBtn61.clicked.connect(lambda:self.img2D.save_rois(QtWidgets.QFileDialog.getSaveFileName(None,"Save rois file", "","rois (*.rois)")[0]))
        
        
        
        
        self.saveBtn62 = QtWidgets.QPushButton('load ROIS')
        
        self.saveBtn62.clicked.connect(lambda:self.img2D.load_rois ((QtWidgets.QFileDialog.getOpenFileName (None,"Open rois file", "","rois (*.rois)"))[0]))
        
        self.saveBtn63 = QtWidgets.QPushButton('save cal')
        self.saveBtn63.clicked.connect(lambda:self.save_calib(QtWidgets.QFileDialog.getSaveFileName(None,"Save cal file", "","cal (*.cal)")[0]))
        
        self.saveBtn64 = QtWidgets.QPushButton('load cal')
        
        self.saveBtn64.clicked.connect(lambda:self.load_calib ((QtWidgets.QFileDialog.getOpenFileName (None,"Open cal file", "","cal (*.cal)"))[0]))
        
        self.saveBtn65 = QtWidgets.QPushButton('change root folder')
        
        self.saveBtn65.clicked.connect(lambda:self.change_folder (str(QtWidgets.QFileDialog.getExistingDirectory(self.w1, "Select Directory"))))
 
        self.saveBtn66 = QtWidgets.QPushButton('save parametres')
        
        self.saveBtn66.clicked.connect(self.save_parameters)
     
        
        self.saveBtn67 = QtWidgets.QPushButton('load parametres')
        
        self.saveBtn67.clicked.connect(self.load_paramters)
     
    
        self.p3.addWidget(self.saveBtn61, row=1, col=3)
        self.p3.addWidget(self.saveBtn62, row=1, col=4)
        
        self.p3.addWidget(self.saveBtn63, row=3, col=3)
        self.p3.addWidget(self.saveBtn64, row=3, col=4)
        self.p3.addWidget(self.saveBtn65, row=4, col=3)
        
        self.p3.addWidget(self.saveBtn66, row=5, col=3)
        self.p3.addWidget(self.saveBtn67, row=5, col=4)



        
        
            
        self.win22 = pg.GraphicsLayoutWidget()
        
        self.win22.setGeometry (1800,400, 699, 311)
        self.w1.setGeometry (100,400, 300, 800)

        self.win22.show()
        
        
        
        self.p333 = self.win22.addPlot(row=1, colspan=self.img2D.nbrofROIS+1)
        self.label333 = pg. LabelItem()
        

        self.checkbox_ =[]

        
        for i in range (self.img2D.nbrofROIS):
        
            checkbox = QtWidgets.QCheckBox(str(i))
            checkbox.setPalette(QtGui.QPalette(QtGui.QColor(self.img2D.couleurs[i])))# QColor(255,0,0)))

            
            self.checkbox_.append (checkbox)

            proxy = QtWidgets.QGraphicsProxyWidget()

            proxy.setWidget(self.checkbox_[-1])

            self.win22.addItem(proxy, row=0,col=i)
        checkbox = QtWidgets.QCheckBox('tot')
        checkbox.setPalette(QtGui.QPalette(QtGui.QColor('greenyellow')))# QColor(255,0,0)))

            
        self.checkbox_.append (checkbox)

        proxy = QtWidgets.QGraphicsProxyWidget()

        proxy.setWidget(self.checkbox_[-1])

        self.win22.addItem(proxy, row=0,col=i+1)
        self.p333.setLabel( 'left', 'Counts') 
        self.p333.setLabel('bottom', 'Energy', units='eV')
            
        
        for i in range (self.img2D. nbrofROIS +1):

            self.checkbox_[i].stateChanged.connect(self.Interpolate_spectres_visu )
    def save_calib(self, roisfilename=None):
        
        if (roisfilename==None):
            roisfilename= 'calib.cal'
        
        
        np.savetxt(roisfilename, self.cal)
        
    def load_calib(self, roisfilename=None):
        
        

        
        if (roisfilename==None):
            roisfilename= 'calib.cal'
        print ('load cal', roisfilename)
        
        
        self.cal =np.loadtxt(roisfilename)
    def change_folder(self,foldername):
        self.foldername = foldername
        self.param['pathname'] =foldername
        
    
    def save_parameters(self):
        l =[] 
        for c in self.param.children():
                    l.append (c.value())
        for c in self.param2.children():
                    l.append (c.value())


        with open("param", "wb") as fp:   #Pickling
            pickle.dump(l, fp)


    def load_paramters(self):
        with open("param", "rb") as fp:   # Unpickling
             l = pickle.load(fp)

        i=0
        for c in self.param.children():
                    c.setValue(l[i])
                    i+=1
        for c in self.param2.children():
                    c.setValue(l[i])
                    i+=1




    def openfileoffline(self):
        
       
        

        index = self.param['index']

        self.img2D.data= self.cubedata [index,:,:]
        
        
        self.img2D.data[self.img2D.data>self.cutv]=0

        self.img2D.dessinerimage( self.img2D.data)
        
        return 
        
        
    def openfileoffline22(self):
        
        tmp_, _ = QtWidgets.QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")

        self.param['filename'] =tmp_
        self.label1.setText(str(self.param['filename']))
        print(self.param['filename'])
        
        
        images =[self.param['filename']]
        
       
       
        
        fileim = tables.open_file(tmp_)
        energies = fileim.get_node('/root.spyc.config1d_RIXS_0001/GALAXIES/i07-c-c02-op-mono/energy').read()
        cubedata= fileim.get_node('/root.spyc.config1d_RIXS_0001/scan_data/merlin_quad_image').read()

        self.cubedata = np.array(  cubedata )
        self.energies =  np.array(  energies )
        index = self.param['index']

        self.img2D.data= self.cubedata [index,:,:]

        
        self.img2D.data[self.img2D.data>self.cutv]=0
        if self.param['Z']:
            self.img2D.dessinerimage( self.img2D.data, cscale=[self.param['minZ'], self.param['maxZ']])
        
        else:

            self.img2D.dessinerimage( self.img2D.data)
        
        
        
    
        

        

    def Open2Dmap(self,filename, first=None, last=None):
        """permet de lire les fichiers d'un scan RIXS 2D 
        entrées: nome du repertoire où sont stockées les images, 
        les indices de la premiere et derniere image 



        """
        S = []
        if first ==None:
            first=0
        if last ==None:
            last=1000
        self.param['filename'] = filename

        for i in tqdm(np.arange (first, last,1)):
            self.param['index'] = i
            print (self.param['index'])

            try:
                self.openfileoffline()
                S.append(self.img2D.spectre)
            except:
                print ('error',i)
        return np.array(S)
    
    
    

    def calibration_automatique(self,energy_range, filename, first, last,  Zbrmin , Zbrmax):

        """Zbrmin, Zbrmax zone à exclure du fit à cause du bruit detecteur """
        

        S = []
        self.param['filename'] = filename



        for i in tqdm( np.arange (first, last,1)):
            self.param['index'] = i

            try:
                self.openfileoffline()

                ss = self.img2D.spectre
                S.append(ss)

            except:
                print ('error',i)
            plt.figure(figsize=(10,10))
            g=[]

            for i in np.arange (0,len(S),1):
                plt.figure(figsize=(10,10))
                plt.xlim(0,200)
                gg=[]
                s2=S[i]


                for j in range (len(s2)) : 
                    s3=S[i][j]
                    plt.plot(s3.T[0], j*0.5+ s3.T[1]/((s3.T[1]).max()), label = str(j))
                    plt.title('energy'+str(first+i))
                    plt.legend()

                    if i>1000:


                        gg.append( self.img2D.fitme(s3.T[0][100:], j*0.5+s3.T[1][100:]/((s3.T[1][100:]).max()), verbose=False)[1]); # position
                    else:
                        gg.append( self.img2D.fitme(s3.T[0], j*0.5+s3.T[1]/((s3.T[1]).max()), verbose=False)[1]); # position
                
                g.append(gg)


            plt.legend()
            print (len(g), len(S))
            plt.xlim(0,200)



        cal=[]

        g =np.array(g)
        plt.figure (figsize=(10,10))





            # energies
        x= energy_range #=np.arange (4580,4625,5) # energy

        for i in np.arange (0, 9,1):
            selg=np.where((g[:,i] < Zbrmin)|(g[:,i]>Zbrmax)) 
            plt.figure (figsize=(5,5))
            m,b = polyfit(x[selg],g[:,i][selg], 1)  #pente offset
            cal.append ([m,b]) 
            plot(x[selg], g[:,i][selg], '.', x, m*x+b, '--') 
            plt.legend()

        return cal
    
    def toEn(self,z,n):
        return (z-self.cal[n][1])/self.cal[n][0]


    def Interpolate_spectres(self,crys=None, isplot=True):
        # automatique robuste


        # pour ajouter les spectres avec 2 methodes; 
        #  en faisant une interpolation de chaque sepctre et faire la sommes des fonctions interpolé

        #calib = [[2.6543,-12170],[2.8334,-12961],[2.9824,-13631],[2.7372,-12516],[2.861,-13055],[2.9664,-13549],[2.7356,-12476],[2.8226,-12884],[2.9512,-13487] ]# pente, offset





        s1 = self.img2D.spectre
        if (crys==None):

                crys =range( len(s1))
                
            
        z=[]
        s=[]
        en=[]
        minen =[]
        maxen =[]

        for i in crys: #range (len(s1)):
            z.append (s1[i].T[0])
            en1 = self.toEn(s1[i].T[0],i)
            en.append (en1)
            s.append (s1[i].T[1])
            minen.append ( en1.min())
            maxen.append ( en1.max())




        ispf=[]
        isp=[]



        energy = np.arange (max(minen),min(maxen),0.01)


        for i in range(len(crys)): #range (len(s1)):


            f= interpolate.interp1d(en[i], s[i])
            ispf.append( f)
            isp.append( f(energy))



        isp= np.array(isp)             


        if (isplot):
            plt.figure(figsize=(10,10))



            for i in range(len(crys)): #range (len(s1)):
                plt.plot (en[i],s[i]/s[i].max(),'.' ,label =crys[i])
                #plt.plot (entemp[i],stemp[i]/s[i].max(), label =i+10)




                plt.plot (energy,isp[i]/isp[i].max(), label = crys[i] )
                
                

                plt.legend()
                plt.grid()


                #plt.xlim(4620-3,4623)
                plt.ylim(0,1.2)


        return energy,isp
    
    def Interpolate_spectres_visu(self ):
        # automatique robuste


        # pour ajouter les spectres avec 2 methodes; 
        #  en faisant une interpolation de chaque sepctre et faire la sommes des fonctions interpolé

        #calib = [[2.6543,-12170],[2.8334,-12961],[2.9824,-13631],[2.7372,-12516],[2.861,-13055],[2.9664,-13549],[2.7356,-12476],[2.8226,-12884],[2.9512,-13487] ]# pente, offset



        isplot=True

        s1 = self.img2D.spectre
        if (1):

                #crys =range( len(s1))
                crys=[]
                
                for i in range ( self.img2D.nbrofROIS):
                    if (self.checkbox_[i].isChecked()):
                        
                        crys.append (i)
                if len (crys)==0:
                    crys.append (0)
            
        z=[]
        s=[]
        en=[]
        minen =[]
        maxen =[]

        for i in crys: #range (len(s1)):
            z.append (s1[i].T[0])
            en1 = self.toEn(s1[i].T[0],i)
            en.append (en1)
            s.append (s1[i].T[1])
            minen.append ( en1.min())
            maxen.append ( en1.max())




        ispf=[]
        isp=[]



        energy = np.arange (max(minen),min(maxen),0.01)


        for i in range(len(crys)): #range (len(s1)):


            f= interpolate.interp1d(en[i], s[i])
            ispf.append( f)
            isp.append( f(energy))



        isp= np.array(isp)             

        first =True
        if (isplot):
            plt.figure(figsize=(10,10))



            for i in range(len(crys)): #range (len(s1)):
                


                plt.plot (energy,isp[i]/isp[i].max(), label = crys[i] )
                
                if first:
                    self.p333.plot(energy,isp[i]/isp[i].max(), clear = True, pen=pg.mkPen(self.img2D.couleurs[crys[i]], width=10))
                    first = False
                else:
                    self.p333.plot(energy,isp[i]/isp[i].max(), clear = False, pen=pg.mkPen(self.img2D.couleurs[crys[i]], width=10))
           
            if self.checkbox_[-1].isChecked():   
            
                self.p333.plot(energy,isp.sum(0)/isp.sum(0).max(), clear = False, pen=pg.mkPen('greenyellow', width=10))

                


                



    
    def Open2Dmap_interp(self, filename, first=None, last=None):
            """permet de lire les fichiers d'un scan RIXS 2D 
            entrées: nome du repertoire où sont stockées les images, 
            les indices de la premiere et derniere image 



            """
            S = []
            if first ==None:
                first=0
            if last ==None:
                last=1000
            self.param['filename'] = filename

            for i in tqdm(np.arange (first, last,1), position=0,leave=True):
                self.param['index'] = i

                try:
                    print (i)
                    self.openfileoffline()

                    op = self.Interpolate_spectres(isplot=False)
                    en = op[0]
                    S.append(op[1])
                except:
                    print ('error',i)
            return en, np.array(S)
    # Make 2D map suite 2/2
    #
    def Make_2DImage_interp(self,en, S1, En_in, crys=None):

        # S interoplated spectra
        #En_in = [start, end, step]

        #En_in = [2468, 2496, 0.1]
        if (crys==None):

            crys =range(S1.shape[1])#[0,1]

        intens = np.zeros((S1.shape[0],S1.shape[2]))

        thlist = np.arange (En_in[0], En_in[1],En_in[2]) # photon energies
        x  = en# np.arange (S1.shape[2])# pixels 

        for cry in crys:

            n=0
            for s1 in (S1):
                try:
                    intens[n,:] = s1[cry]
                    n+=1
                except:
                    pass

            plt.figure(figsize=(10,5))
            plt.clf()
            plt.pcolormesh(x, thlist, intens, cmap ='terrain')
            plt.axis('tight')
            plt.ylabel('photon in energy (eV)')
            plt.xlabel(' photon out energy eV')
            plt.title('cry'+str(cry))

            plt.colorbar()
            plt.grid()

        # image somme!
        intens2 = np.zeros((S1.shape[0],S1.shape[2]))


        n=0
        for s1 in (S1):
                try:
                    intens2[n,:] = s1[crys].sum(0)
                    n+=1
                except:
                    pass

        plt.figure(figsize=(10,5))
        plt.clf()
        plt.pcolormesh(x, thlist, intens2, cmap ='terrain')
        plt.axis('tight')
        plt.ylabel('photon energy (eV)')
        plt.title('SOMME')
        plt.xlabel(' distance pixel')
        plt.colorbar()
        plt.grid()
        
        
        return x, thlist, intens2
    
    def Make_2DImage(self, S1, En_in, crys=None, vl=None):

        thlist = np.arange (En_in[0], En_in[1],En_in[2]) # photon energies

      
        if (crys==None):

                crys =range(S1.shape[1])


                #thlist = np.arange (En_in[0], En_in[1],En_in[2]) # photon energies
                #thlist = np.arange (2468, 2496, 0.1) # photon energies

        for cry in crys:
            intens = np.zeros((len(S1),len(S1[2][cry].T[1])))

            #thlist = np.arange (len(S1)) # photon energies




            n=0
            for s1 in (S1):
                try:
                    x = s1[cry].T[0]
                    intens[n,:] = s1[cry].T[1]
                    n+=1
                except:
                    pass

            plt.figure(figsize=(10,5))
            plt.clf()
            if (vl==None):
                plt.pcolormesh(x, thlist, intens, cmap ='terrain')
            else:
                plt.pcolormesh(x, thlist, intens, cmap ='terrain', vmin=vl[0], vmax=vl[1])

            
            
            
            plt.axis('tight')
            plt.ylabel('photon energy (eV)')
            plt.xlabel(' distance pixel')
            plt.title('cry'+str(cry))
            plt.colorbar()
            #plt.grid()
    def Make_2DImageP( self, S1, En_in, crys=None, vl=None):

        thlist = np.arange (En_in[0], En_in[1],En_in[2]) # photon energies

      
        if (crys==None):

                crys =range(S1.shape[1])


                #thlist = np.arange (En_in[0], En_in[1],En_in[2]) # photon energies
                #thlist = np.arange (2468, 2496, 0.1) # photon energies

        for cry in crys:
            intens = np.zeros((len(S1),len(S1[2][cry].T[1])))

            #thlist = np.arange (len(S1)) # photon energies




            n=0
            for s1 in (S1):
                try:
                    x = s1[cry].T[0]
                    intens[n,:] = s1[cry].T[1]
                    n+=1
                except:
                    pass

            #if (vl==None):
                #plt.pcolormesh(x, thlist, intens, cmap ='terrain')
            #else:
                #plt.pcolormesh(x, thlist, intens, cmap ='terrain', vmin=vl[0], vmax=vl[1])

            #from scipy.interpolate import griddata

    

        
            #del ZZ
            
            
           
            ZZ =intens.T.reshape(len(x),len(thlist))
            
            if (vl==None):
                plt.figure(figsize=(10,5))
                plt.imshow(np.rot90( ZZ), extent=[x.min(),x.max(),thlist.min(),thlist.max()], vmax=1e4,aspect='auto',cmap ='terrain')#,origin ='lower', extent=[xu.min(),xu.max(),500,700],vmin=-0.005,vmax=0,aspect = (1/2))

            else:
            
                plt.imshow(np.rot90( ZZ), extent=[x.min(),x.max(),thlist.min(),thlist.max()], aspect='auto', vmin=vl[0], vmax=vl[1],cmap ='terrain')#,origin ='lower', extent=[xu.min(),xu.max(),500,700],vmin=-0.005,vmax=0,aspect = (1/2))

            plt.axis('tight')
            plt.ylabel('photon energy (eV)')
            plt.xlabel(' distance pixel')
            plt.title('cry'+str(cry))
            

            return  x, thlist, ZZ

            
            
            #plt.grid()


        







        
   
        




    def update(self):
        
        i=2

       # global  param
        # if phase % (8*np.pi) > 4*np.pi:
        #     m1['angle'] = 315 + 1.5*np.sin(phase)
        #     m1a['angle'] = 315 + 1.5*np.sin(phase)
        # else:
        #     m2['angle'] = 135 + 1.5*np.sin(phase)
        #     m2a['angle'] = 135 + 1.5*np.sin(phase)
       # m1['angle'] = param['count']-90
       
    
    def auto_calibbtn(self):
        #self.mosarix.writehd5(self.param['filename']+str (self.param['index']-1))
        
        i1 = self.param2['firstfile']
        i2 = self.param2['lastfile']
        e1 = self.param2['firstenergy']
        e2 = self.param2['lastenergy']
        e3 = self.param2['lastenergy']
        de = self.param2['energystep']

        fi_name = self.param['filename']


        #energy_range=np.arange (4580,4625,5)


        #p.cal=p.calibration_automatique(energy_range, 'Gtest1', first=509, last = 518, Zbrmin=60, Zbrmax=100);

        energy_range=np.arange (e1,e2,de)
        self.cal=self.calibration_automatique(energy_range, fi_name, first=i1, last = i2, Zbrmin=1000, Zbrmax=0);
        
        
        
        
         
         #self.w1.update()
    
    
    
        
    
    def plotspectres( self,crys=None, isplot=True):
        
        


        s1 = self.img2D.spectre
        if (crys==None):

            crys =range( len(s1)) 

        if isplot:
            plt.figure(figsize=(10,10))

        
            for i in  (crys):
            
            
                    plt.plot (s1[i].T[0],s1[i].T[1] , label ='cry'+str (i))
            plt.legend()



        


        return s1
        
        
    
        


        


        
        

        
        
    

       
       
       
        
    




#param.child('record').sigValueChanged.connect(lambda _, v: timer.stop() if v else timer.start())



