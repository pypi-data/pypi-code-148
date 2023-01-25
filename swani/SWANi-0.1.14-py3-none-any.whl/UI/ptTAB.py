import os, shutil
from threading import Thread
from PySide6.QtWidgets import (QTabWidget, QWidget, QGridLayout, QLabel,
                                QPushButton, QSizePolicy, QHBoxLayout,
                                QGroupBox, QVBoxLayout,QMessageBox,QListWidget,
                                QFileDialog, QTreeWidget, QErrorMessage,QFileSystemModel,
                                QTreeView,QComboBox)
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtGui import QFont

from PySide6.QtSvgWidgets import QSvgWidget

import pydicom
import configparser
from multiprocessing import Pipe

from SWANi.UI.persistentProgressDialog import persistentProgressDialog
from SWANi.UI.customTreeWidgetItem import customTreeWidgetItem
from SWANi.UI.verticalScrollArea import verticalScrollArea

from SWANi.SWANiWorkflow.workflowThread import gen_SWANi_wf_worker, SWANi_wf_process, logReceiver_worker
from SWANi.SWANiWorkflow.mainWorkflow import SWANi_wf

from SWANi.SWANiSlicer.SWANiSlicer import SWANiSlicer

from SWANi.utils.dicomSearch import dicomSearch
from SWANi.utils.APPLABELS import APPLABELS

class ptTAB(QTabWidget):

    DATATAB=0
    EXECTAB=1
    RESULTTAB=2

    def __init__(self, SWANiGlobalConfig, ptFolder, mainWindow, parent = None):
        super(ptTAB, self).__init__(parent)
        self.SWANiGlobalConfig=SWANiGlobalConfig
        self.ptFolder=ptFolder
        self.ptName=os.path.basename(ptFolder)
        self.mainWindow=mainWindow

        self.dataTab = QWidget()
        self.wfExecTab = QWidget()
        self.slicerTab = QWidget()

        self.addTab(self.dataTab,"Data load")
        self.addTab(self.wfExecTab,"Workflow execution")
        self.addTab(self.slicerTab,"Results export")

        self.start_gen_wf_thread()

        self.dataTabUI()
        self.wfExecTabUI()
        self.slicerTabUI()

        self.setTabEnabled(ptTAB.EXECTAB, False)
        self.setTabEnabled(ptTAB.RESULTTAB, False)

    def updateNodeList(self,msg):
        split=msg.split(".")

        split.pop(0)

        if split[2]==SWANi_wf_process.NODESTARTED:
            icon=self.mainWindow.loadingMovie_file
        elif split[2]==SWANi_wf_process.COMPLETED:
                icon=self.mainWindow.okIcon_file
        else:
            icon=self.mainWindow.errorIcon_file

        self.nodeList[split[0]][split[1]].setArt(icon)

        self.nodeList[split[0]]['customTreeWidgetItem'].setExpanded(True)

        if icon==self.mainWindow.okIcon_file:
            completed=True
            for key in self.nodeList[split[0]].keys():
                if key!='customTreeWidgetItem' and self.nodeList[split[0]][key].art!=self.mainWindow.okIcon_file:
                    completed=False
                    break
            if completed:
                self.nodeList[split[0]]['customTreeWidgetItem'].setArt(self.mainWindow.okIcon_file)
                self.nodeList[split[0]]['customTreeWidgetItem'].setExpanded(False)
                self.nodeList[split[0]]['customTreeWidgetItem'].completed=True
                allfinished=True
                for key in self.nodeList.keys():
                    if not self.nodeList[key]['customTreeWidgetItem'].completed:
                        allfinished=False
                        break
                if allfinished:
                    self.setTabEnabled(ptTAB.DATATAB, True)
                    self.execButton.setText(APPLABELS.APPNAME+" Workflow executed!")
                    self.execButton.setEnabled(False)
                    self.enableTabIfResultDir()

    def removeRunningIcon(self):
        for key1 in self.nodeList.keys():
            for key2 in self.nodeList[key1].keys():
                if self.nodeList[key1][key2].art==self.mainWindow.loadingMovie_file:
                    self.nodeList[key1][key2].setArt(self.mainWindow.voidsvg_file)

    def start_gen_wf_thread(self):
        if not self.mainWindow.fsl:
            return
        gen_SWANi_wf_work= gen_SWANi_wf_worker(self.ptFolder)
        gen_SWANi_wf_work.signal.wf.connect(self.setwf)
        QThreadPool.globalInstance().start(gen_SWANi_wf_work)

    def setwf(self,wf):
        self.wf=wf
        if hasattr(self, 'nodeButton'):
            self.nodeButton.setEnabled(True)
            self.wfTypeCombo.setEnabled(True)

        if hasattr(self, 'check_input') and not '' in self.check_input.values() and self.check_input["mr_t13d"]:
            self.setTabEnabled(ptTAB.EXECTAB, True)



    def dataTabUI(self):
        #LAYOUT ORIZZONTALE
        layout = QHBoxLayout()

        #PRIMA COLONNA: LISTA DEGLI INPUT
        scrollArea= verticalScrollArea()
        folderLayout = QGridLayout()
        scrollArea.m_scrollAreaWidgetContents.setLayout(folderLayout)
        self.inputReport={}

        boldFont=QFont()
        boldFont.setBold(True)
        x=0

        for inputName in self.SWANiGlobalConfig.INPUTLIST:

            if inputName.startswith("op_"):
                split=inputName.split("_")
                if len(split)<3: continue
                if not self.SWANiGlobalConfig.getboolean('OPTIONAL_SERIES', split[1]+"_"+split[2]): continue

            self.inputReport[inputName] = [QSvgWidget(self), QLabel(inputName.replace("op_","")), QLabel(""),QPushButton("Import"),QPushButton("Clear")]
            self.inputReport[inputName][0].load(self.mainWindow.errorIcon_file)
            self.inputReport[inputName][0].setFixedSize(25,25)
            self.inputReport[inputName][1].setFont(boldFont)
            self.inputReport[inputName][1].setAlignment(Qt.AlignLeft|Qt.AlignBottom)
            self.inputReport[inputName][2].setAlignment(Qt.AlignLeft|Qt.AlignTop)
            self.inputReport[inputName][2].setStyleSheet("margin-bottom: 20px")
            self.inputReport[inputName][3].setEnabled(False)
            self.inputReport[inputName][3].clicked.connect(lambda checked=None, x=inputName: self.dicomImport2Folder(x))
            self.inputReport[inputName][3].setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
            self.inputReport[inputName][4].setEnabled(False)
            self.inputReport[inputName][4].clicked.connect(lambda checked=None, x=inputName: self.clearImportFolder(x))
            self.inputReport[inputName][4].setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)

            folderLayout.addWidget(self.inputReport[inputName][0],(x*2),0,2,1)
            folderLayout.addWidget(self.inputReport[inputName][1],(x*2),1)

            folderLayout.addWidget(self.inputReport[inputName][3],(x*2),2)
            folderLayout.addWidget(self.inputReport[inputName][4],(x*2),3)

            folderLayout.addWidget(self.inputReport[inputName][2],(x*2)+1,1,1,3)
            x+=1

        #SECONDA COLONNA: LISTA SERIE DA IMPORTARE
        importGroupBox = QGroupBox()
        importLayout = QVBoxLayout()
        importGroupBox.setLayout(importLayout)

        scanDicomFolderButton = QPushButton("Scan DICOM folder")
        scanDicomFolderButton.clicked.connect(self.scanDicomFolder)

        self.importableSeriesList = QListWidget()
        importLayout.addWidget(scanDicomFolderButton)
        importLayout.addWidget(self.importableSeriesList)

        #AGGIUNGO LE COLONNE AL LAYOUT PRINCIPALE
        layout.addWidget(scrollArea,stretch=1)
        layout.addWidget(importGroupBox,stretch=1)
        self.dataTab.setLayout(layout)

    def dicomImport2Folder(self,inputName):
        if self.importableSeriesList.currentRow()==-1:
            msgBox = QMessageBox()
            msgBox.setText("No series was selected")
            msgBox.exec()
            return

        import shutil
        destPath=os.path.join(self.ptFolder,self.SWANiGlobalConfig['DEFAULTFOLDERS']['default_'+inputName+'_folder'])
        foundMod=self.finalSeriesList[self.importableSeriesList.currentRow()][0].split("-")[1].upper()
        expedctedMod=inputName.upper().replace("op_","").split("_")[0]

        if not expedctedMod in foundMod:
            msgBox = QMessageBox()
            msgBox.setText("You selected "+foundMod+" images while "+expedctedMod+" images were expected.")
            msgBox.setInformativeText("Do you want to continue importing?")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setDefaultButton(QMessageBox.No)
            ret = msgBox.exec()
            if ret==QMessageBox.No: return

        copyList=self.finalSeriesList[self.importableSeriesList.currentRow()][1]

        progress = persistentProgressDialog("Copying DICOM files in patient folder...", 0, len(copyList)+1,self)
        progress.show()

        self.inputReport[inputName][0].load(self.mainWindow.loadingMovie_file)

        for thisFile in copyList:
            if not os.path.isfile(thisFile): continue
            shutil.copy(thisFile, destPath)
            progress.increaseValue(1)

        progress.setRange(0,0)
        progress.setLabelText("Verifying patient folder...")

        self.checkInputFolder(inputName,progress)

        self.reset_wf()

    def scanDicomFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, 'Select a folder to scan for DICOM files')
        if not os.path.exists(folderPath):
            return

        dicomsrc= dicomSearch(folderPath, parent=self)
        dicomsrc.loadDir()


        if dicomsrc.getFilesLen()>1:
            self.importableSeriesList.clear()
            self.finalSeriesList=[]
            progress = persistentProgressDialog("Scanning DICOM folder...", 0, 0)
            progress.show()
            progress.setMaximum(dicomsrc.getFilesLen())
            dicomsrc.signal.sigLoop.connect(lambda i: progress.increaseValue(i))
            dicomsrc.signal.sigFinish.connect(self.showScanResult)
            dicomsrc.start()
        else:
            msgBox = QMessageBox()
            msgBox.setText("No DICOM file in "+folderPath)
            msgBox.exec()

    def wfExecTabUI(self):
        layout = QGridLayout()

        #PRIMA COLONNA: node list
        self.wfTypeCombo = QComboBox(self)

        for index, label in enumerate(APPLABELS.WFTYPES):
            self.wfTypeCombo.insertItem(index,label)

        self.wfTypeCombo.currentIndexChanged.connect(self.onWfTypeChanged)
        layout.addWidget(self.wfTypeCombo,0,1)

        self.nodeButton=QPushButton(APPLABELS.GENBUTTONTEXT)
        self.nodeButton.clicked.connect(self.genWF)
        if not hasattr(self, 'wf'):
            self.nodeButton.setEnabled(False)

        layout.addWidget(self.nodeButton,1,1)

        self.nodeListTreeWidget = QTreeWidget()
        self.nodeListTreeWidget.setHeaderHidden(True)
        self.nodeListTreeWidget.setFixedWidth(320)

        layout.addWidget(self.nodeListTreeWidget,2,1)
        self.nodeListTreeWidget.itemClicked.connect(self.treeItemClicked)

        #SECONDA COLONNA: graph monitor
        self.execButton=QPushButton(APPLABELS.EXECBUTTONTEXT)
        self.execButton.clicked.connect(self.start_SWANi_wf_thread)
        self.execButton.setEnabled(False)

        layout.addWidget(self.execButton,1,2)
        self.execGraph = QSvgWidget()
        layout.addWidget(self.execGraph,2,2)

        self.wfExecTab.setLayout(layout)

    def onWfTypeChanged(self,index):
        self.ptConfig['ptConfig']['wfType']=str(index)
        self.savePatientConfig()
        self.reset_wf()

    def genWF(self):
        if not self.mainWindow.fsl:
            errorDialog=QErrorMessage(parent=self)
            errorDialog.showMessage("FSL is required to generate "+APPLABELS.APPNAME+" Workflow!")
            return

        if not hasattr(self,"wf") or self.wf==None:
            self.wf=SWANi_wf(name=self.ptName+"_nipype",base_dir=self.ptFolder)

        self.wf.add_input_folders(self.SWANiGlobalConfig,self.ptConfig['ptConfig'].getint('wfType'),self.check_input,self.mainWindow.freesurfer)
        self.nodeList=self.wf.get_node_array()
        self.nodeListTreeWidget.clear()

        graphdir=os.path.join(self.ptFolder,"graph/")
        shutil.rmtree(graphdir,ignore_errors=True)
        os.mkdir(graphdir)

        for node in self.nodeList.keys():
            self.nodeList[node]['customTreeWidgetItem']=customTreeWidgetItem(self.nodeListTreeWidget,self.nodeListTreeWidget,node)
            if len(self.nodeList[node].keys())>1:
                if self.mainWindow.graphviz:
                    thread = Thread(target=self.wf.get_node(node).write_graph, kwargs={'graph2use':'colored', 'format':'svg', 'dotfilename':os.path.join(graphdir,'graph_'+node+'.dot')})
                    thread.start()
                for subnode in self.nodeList[node].keys():
                    if subnode!='customTreeWidgetItem':
                        self.nodeList[node][subnode]=customTreeWidgetItem(self.nodeList[node]['customTreeWidgetItem'],self.nodeListTreeWidget,subnode)
        self.execButton.setEnabled(True)
        self.execButton.setText(APPLABELS.EXECBUTTONTEXT)
        self.nodeButton.setEnabled(False)

    def treeItemClicked(self, it, col):
        if self.mainWindow.graphviz and it.parent()==None:
            file=os.path.join(self.ptFolder,"graph",'graph_'+it.getText()+'.svg')
            self.execGraph.load(file)
            self.execGraph.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)

    def noCloseEvent(self, event):
        event.ignore()

    def start_SWANi_wf_thread(self):
        if not hasattr(self,"wf_process") or self.wf_process==None or not self.wf_process.is_alive():
            wfdir=os.path.join(self.ptFolder,self.ptName+"_nipype")
            if os.path.exists(wfdir):
                msgBox = QMessageBox()
                msgBox.setInformativeText("A previus execution of "+APPLABELS.APPNAME+" was detected. Do you want to resume execution or start a new one?")
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msgBox.button(QMessageBox.Yes).setText("Resume execution")
                msgBox.button(QMessageBox.No).setText("New execution")
                msgBox.setDefaultButton(QMessageBox.Yes)
                msgBox.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                msgBox.closeEvent=self.noCloseEvent
                ret = msgBox.exec()
                if ret==QMessageBox.No:
                    shutil.rmtree(wfdir,ignore_errors=True)

            fsdir=os.path.join(self.ptFolder,"FS")
            if os.path.exists(fsdir):
                msgBox = QMessageBox()
                msgBox.setInformativeText("An existing FreeSurfer folder was detected. Do you want to keep or delete the existing folder?")
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msgBox.button(QMessageBox.Yes).setText("Keep folder")
                msgBox.button(QMessageBox.No).setText("Delete folder")
                msgBox.setDefaultButton(QMessageBox.Yes)
                msgBox.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                msgBox.closeEvent=self.noCloseEvent
                ret = msgBox.exec()
                if ret==QMessageBox.No:
                    shutil.rmtree(fsdir,ignore_errors=True)

            pipeReceiver, self.pipeSender = Pipe()  
            
            logReceiver_work=logReceiver_worker(pipeReceiver)
            logReceiver_work.signal.log_msg.connect(self.updateNodeList)            
            QThreadPool.globalInstance().start(logReceiver_work)
            
            self.wf_process=SWANi_wf_process(self.ptName, self.wf, self.pipeSender)
            self.wf_process.start()

            self.execButton.setText(APPLABELS.EXECBUTTONTEXT_STOP)
            self.setTabEnabled(ptTAB.DATATAB, False)
            self.setTabEnabled(ptTAB.RESULTTAB, False)
            self.wfTypeCombo.setEnabled(False)

        else:
            msgBox = QMessageBox()
            msgBox.setInformativeText("Do you REALLY want to stop "+APPLABELS.APPNAME+" Workflow execution?")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setDefaultButton(QMessageBox.No)
            msgBox.closeEvent=self.noCloseEvent
            ret = msgBox.exec()
            if ret==QMessageBox.No: return
            
            self.closePipeSenderAndHandler()
            self.wf_process.stopEvent.set()
            
            self.removeRunningIcon()
            self.execButton.setText(APPLABELS.EXECBUTTONTEXT)
            self.setTabEnabled(ptTAB.DATATAB, True)
            self.reset_wf()
            self.enableTabIfResultDir()

    def slicerTabUI(self):
        slicerTabLayout = QGridLayout()
        self.slicerTab.setLayout(slicerTabLayout)

        self.exportResultsButton=QPushButton("Export results into Slicer scene")
        self.exportResultsButton.clicked.connect(self.SWANiSlicer_thread)
        self.exportResultsButton.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        if self.SWANiGlobalConfig['MAIN']['slicerPath'] == '' or not os.path.exists(self.SWANiGlobalConfig['MAIN']['slicerPath']):
            self.exportResultsButton.setEnabled(False)
        slicerTabLayout.addWidget(self.exportResultsButton,0,0)

        self.resultsModel=QFileSystemModel()
        self.resultTree=QTreeView(parent=self)
        self.resultTree.setModel(self.resultsModel)

        slicerTabLayout.addWidget(self.resultTree,1,0)

    def SWANiSlicer_thread(self):
        progress = persistentProgressDialog("Exporting results into Slicer scene...\nLoading Slicer environment", 0, 0,parent=self)
        progress.show()

        slicerThread=SWANiSlicer(self.SWANiGlobalConfig['MAIN']['slicerPath'],self.ptFolder,parent=self)
        slicerThread.signal.export.connect(lambda msg: self.SWANiSlicer_thread_signal(msg,progress))
        slicerThread.start()

    def SWANiSlicer_thread_signal(self,msg,progress):
        if msg=='ENDLOADING':
                progress.done(1)
        else:
            progress.setLabelText("Exporting results into Slicer scene...\n"+msg)


    def loadPtConfig(self):
        self.ptConfig=configparser.ConfigParser()
        self.patientConfigFile=os.path.join(os.path.join(self.ptFolder,".config"))

        if os.path.exists(self.patientConfigFile):
            self.ptConfig.read(self.patientConfigFile)
        else:
            self.ptConfig['ptConfig']={'wfType': self.SWANiGlobalConfig['MAIN']['defaultWfType']}

    def loadPt(self):
        dicomScanners={}
        self.check_input={}
        totalFiles=0

        #importo la configurazione del tipo di workflow
        self.loadPtConfig()

        #for inputName in self.SWANiGlobalConfig.INPUTLIST:
        for inputName in self.inputReport:
            dicomScanners[inputName]=self.checkInputFolder_step1(inputName)
            totalFiles=totalFiles+dicomScanners[inputName].getFilesLen()
            self.check_input[inputName]=''

        if totalFiles>0:
            progress = persistentProgressDialog("Checking patient DICOM folders...", 0, 0,parent=self.parent())
            progress.show()
            progress.setMaximum(totalFiles)
        else: progress=None

        #for inputName in self.SWANiGlobalConfig.INPUTLIST:
        for inputName in self.inputReport:
            self.inputReport[inputName][0].load(self.mainWindow.loadingMovie_file)
            self.checkInputFolder_step2(inputName, dicomScanners[inputName],progress)

        self.setTabEnabled(ptTAB.DATATAB, True)
        self.setCurrentWidget(self.dataTab)

        #svuoto la lista delle serie importabili
        self.importableSeriesList.clear()
        #reset del workflow
        self.reset_wf()

        self.enableTabIfResultDir()

    def enableTabIfResultDir(self):
        sceneDir=os.path.join(self.ptFolder,"scene")
        if os.path.exists(sceneDir):
            self.setTabEnabled(ptTAB.RESULTTAB, True)
            self.resultsModel.setRootPath(sceneDir)
            indexRoot = self.resultsModel.index(self.resultsModel.rootPath())
            self.resultTree.setRootIndex(indexRoot)
        else:
           self.setTabEnabled(ptTAB.RESULTTAB, False)

    def checkInputFolder_step1(self,inputName):
        srcPath=os.path.join(self.ptFolder,self.SWANiGlobalConfig['DEFAULTFOLDERS']['default_'+inputName+'_folder'])
        dicomsrc= dicomSearch(srcPath, parent=self)
        dicomsrc.loadDir()
        return dicomsrc

    def checkInputFolder_step2(self,inputName, dicomsrc, progress=None):
        dicomsrc.signal.sigFinish.connect(lambda src, name=inputName: self.checkInputFolder_step3(name,src))
        if progress!=None:
            if progress.maximum()==0:
                progress.setMaximum(dicomsrc.getFilesLen())
            dicomsrc.signal.sigLoop.connect(lambda i: progress.increaseValue(i))
        dicomsrc.start()

    def checkInputFolder_step3(self, inputName, dicomsrc):
        srcPath=dicomsrc.dicomPath
        ptList=dicomsrc.getPatientList()
        self.check_input[inputName]=True

        if not '' in self.check_input.values() and self.check_input["mr_t13d"]:
            self.setTabEnabled(ptTAB.EXECTAB, True)

        if len(ptList)==0:
            self.setError(inputName,"No dicom file in "+srcPath)
            self.check_input[inputName]=False
            return

        if len(ptList)>1:
            self.setWarm(inputName,"Dicom file from more than one patient in "+srcPath)
            return
        examList=dicomsrc.getExamList(ptList[0])
        if len(examList)!=1:
            self.setWarm(inputName,"DICOM file from more than one examination in "+srcPath)
            return
        seriesList=dicomsrc.getSeriesList(ptList[0],examList[0])
        if len(seriesList)!=1:
            self.setWarm(inputName,"DICOM file from more than one series in "+srcPath)
            return

        imageList=dicomsrc.getSeriesFiles(ptList[0],examList[0],seriesList[0])
        ds = pydicom.read_file(imageList[0], force=True)
        mod=ds.Modality
        if mod=="PT": mod="PET"
        self.setOk(inputName,str(ds.PatientName)+"-"+mod+"-"+ds.SeriesDescription+": "+str(len(imageList))+" images")

    def checkInputFolder(self,inputName,progress=None):
        dicomsrc= self.checkInputFolder_step1(inputName)
        self.checkInputFolder_step2(inputName, dicomsrc,progress)


    def clearImportFolder(self,inputName):

        wf_names={'mr_t13d':'t13d',
                    'mr_flair3d':'flair',
                    'mr_mdc':'mdc',
                    'mr_venosa':'venosa',
                    'mr_venosa2':'venosa',
                    'mr_dti':'dti_preproc',
                    'mr_asl':'asl',
                    'ct_brain':'pet/pet_ct_conv',
                    'mr_fmri':'',
                    'pet_brain':'pet/pet_brain_conv',
                    'op_mr_flair2d_tra':'flair2d_tra',
                    'op_mr_flair2d_cor':'flair2d_cor',
                    'op_mr_flair2d_sag':'flair2d_sag'}

        srcPath=os.path.join(self.ptFolder,self.SWANiGlobalConfig['DEFAULTFOLDERS']['default_'+inputName+'_folder'])

        progress = persistentProgressDialog("Clearing DICOM files in: "+srcPath, 0, 0,self)
        progress.show()

        import shutil
        shutil.rmtree(srcPath, ignore_errors=True)
        os.makedirs(srcPath,exist_ok=True)

        #reset dei wf in caso di cambio immagini
        if wf_names[inputName]!=None and wf_names[inputName]!='':
            srcPath=os.path.join(os.getcwd(),APPLABELS.APPNAME,wf_names[inputName])
            shutil.rmtree(srcPath, ignore_errors=True)

        self.setError(inputName,"No dicom file in "+srcPath)
        self.check_input[inputName]=False
        if inputName== "mr_t13d":
           self.setTabEnabled(ptTAB.EXECTAB, False)

        progress.accept()
        self.reset_wf()

    def reset_wf(self):
        #SE NON CARICATO UN PAZIENTE, NON FACCIO NULLA
        #if not self.isTabEnabled(1): return

        self.wf=None
        self.nodeListTreeWidget.clear()
        self.execGraph.load(self.mainWindow.voidsvg_file)
        self.execButton.setEnabled(False)
        self.execButton.setText(APPLABELS.EXECBUTTONTEXT)
        self.nodeButton.setEnabled(True)
        self.wfTypeCombo.setEnabled(True)

        self.wfTypeCombo.setCurrentIndex(self.ptConfig['ptConfig'].getint('wfType'))

    def showScanResult(self,dicomsrc):
        folderPath=dicomsrc.dicomPath
        ptList=dicomsrc.getPatientList()

        if len(ptList)==0:
            msgBox = QMessageBox()
            msgBox.setText("No DICOM file in "+folderPath)
            msgBox.exec()
            return
        if len(ptList)>1:
            msgBox = QMessageBox()
            msgBox.setText("DICOM file from more than one patient in "+folderPath)
            msgBox.exec()
            return
        examList=dicomsrc.getExamList(ptList[0])
        for exam in examList:
            seriesList=dicomsrc.getSeriesList(ptList[0],exam)
            for serie in seriesList:
                imageList=dicomsrc.getSeriesFiles(ptList[0],exam,serie)
                ds = pydicom.read_file(imageList[0], force=True)
                #non mostro le serie troppo corte (survey ecc) a meno che non siano mosaici
                if len(imageList)<10 and hasattr(ds, 'ImageType') and not "MOSAIC" in ds.ImageType: continue

                mod=ds.Modality
                if mod=="PT": mod="PET"
                self.finalSeriesList.append([str(ds.PatientName)+"-"+mod+"-"+ds.SeriesDescription+": "+str(len(imageList))+" images", imageList])
                del(imageList)

        for serie in self.finalSeriesList:
            self.importableSeriesList.addItem(serie[0])

    def setWarm(self,inputName,msg):
        self.inputReport[inputName][0].load(self.mainWindow.warnIcon_file)
        self.inputReport[inputName][0].setFixedSize(25,25)
        self.inputReport[inputName][0].setToolTip(msg)
        self.inputReport[inputName][3].setEnabled(False)
        self.inputReport[inputName][4].setEnabled(True)
        self.inputReport[inputName][2].setText("")

    def setError(self,inputName,msg):
        self.inputReport[inputName][0].load(self.mainWindow.errorIcon_file)
        self.inputReport[inputName][0].setFixedSize(25,25)
        self.inputReport[inputName][0].setToolTip(msg)
        self.inputReport[inputName][3].setEnabled(True)
        self.inputReport[inputName][4].setEnabled(False)
        self.inputReport[inputName][2].setText("")

    def setOk(self,inputName,msg):
        self.inputReport[inputName][0].load(self.mainWindow.okIcon_file)
        self.inputReport[inputName][0].setFixedSize(25,25)
        self.inputReport[inputName][0].setToolTip("")
        self.inputReport[inputName][3].setEnabled(False)
        self.inputReport[inputName][4].setEnabled(True)
        self.inputReport[inputName][2].setText(msg)

    def savePatientConfig(self):
        with open(self.patientConfigFile,"w") as openedFile:
            self.ptConfig.write(openedFile)
            
    def closePipeSenderAndHandler(self):
        if hasattr(self,'pipeSender'):
            try: 
                self.pipeSender.send(logReceiver_worker.STOP)
                self.pipeSender.close()
            except:
                self.pipeSender.close()
    
    def closeRoutine(self):
        self.savePatientConfig()
        self.closePipeSenderAndHandler()
