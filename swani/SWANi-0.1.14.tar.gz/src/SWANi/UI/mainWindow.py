from PySide6.QtWidgets import (QMainWindow, QMessageBox, QFileDialog, QInputDialog, QLineEdit, QTabWidget,
                                QGridLayout, QLabel, QSizePolicy, QSpacerItem, QWidget, QTabBar)
from SWANi.utils.check_dependency import check_dcm2niix, check_fsl, check_freesurfer, check_graphviz, check_python_lib, check_slicer
from PySide6.QtGui import QAction, QIcon, QPixmap, QFont
from PySide6 import QtCore
from PySide6.QtSvgWidgets import QSvgWidget
import os, shutil,sys
import pyshortcuts
from pyshortcuts.shortcut import shortcut as shcdef
from pyshortcuts.shortcut import Shortcut

from SWANi.UI.ptTAB import ptTAB
from SWANi.UI.preferencesWindow import preferencesWindow
import SWANi_supplement
from SWANi.utils.APPLABELS import APPLABELS

class mainWindow(QMainWindow):
    ptDirPath=""
    tabWidget=None

    def __init__(self, SWANiGlobalConfig):

        self.SWANiGlobalConfig=SWANiGlobalConfig

        super(mainWindow,self).__init__()

        self.okIcon_file=SWANi_supplement.okIcon_file
        self.errorIcon_file=SWANi_supplement.errorIcon_file
        self.warnIcon_file=SWANi_supplement.warnIcon_file
        self.loadingMovie_file = SWANi_supplement.loadingMovie_file
        self.voidsvg_file = SWANi_supplement.voidsvg_file

        self.okIcon=QPixmap(self.okIcon_file)
        self.errorIcon=QPixmap(self.errorIcon_file)
        self.warnIcon=QPixmap(self.warnIcon_file)

        while self.SWANiGlobalConfig.getPatientsFolder()=="" or not os.path.exists(self.SWANiGlobalConfig.getPatientsFolder()):
            msgBox = QMessageBox()
            msgBox.setText("Choose the main working directory before start to use this application")
            msgBox.exec()
            self.setPatientsFolder()

        os.chdir(self.SWANiGlobalConfig.getPatientsFolder())

        self.inizializeUI()

        #controllo che eventuali shortcut salvati esistano
        if self.SWANiGlobalConfig['MAIN']['shortcutPath']!='':
            targets=self.SWANiGlobalConfig['MAIN']['shortcutPath'].split("|")
            newPath=''
            change=False
            for fil in targets:
                if "SWANi" in fil and os.path.exists(fil):
                    if newPath!='': newPath=newPath+"|"
                    newPath=newPath+fil
                else:
                    change=True
            if change:
                self.SWANiGlobalConfig['MAIN']['shortcutPath']=newPath
                self.SWANiGlobalConfig.save()

    def openPtDir(self,folderPath):
        thistab = ptTAB(self.SWANiGlobalConfig,folderPath,self,parent=self.mainTAB)
        self.ptTabsArray.append(thistab)

        self.mainTAB.addTab(thistab,os.path.basename(folderPath))
        self.mainTAB.setCurrentWidget(thistab)
        thistab.loadPt()


    @QtCore.Slot()
    def searchPtDir(self):
        if self.SWANiGlobalConfig.getint('MAIN','maxPt')>0 and len(self.ptTabsArray)>=self.SWANiGlobalConfig.getint('MAIN','maxPt'):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Max patient tab limit reached!")
            msgBox.exec()
            return
        
        fileDialog=QFileDialog()
        fileDialog.setDirectory(self.SWANiGlobalConfig.getPatientsFolder())
        folderPath = fileDialog.getExistingDirectory(self, 'Select a patient folder')
        if not os.path.exists(folderPath):
            return
        
        if not os.path.abspath(folderPath).startswith(os.path.abspath(self.SWANiGlobalConfig.getPatientsFolder())+os.sep):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("The selected folder is not in "+APPLABELS.APPNAME+" main working directory!")
            msgBox.exec()
            return  

        for pt in self.ptTabsArray:
            if pt.ptFolder==folderPath:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("The selected patient was already loaded in "+APPLABELS.APPNAME+"!")
                msgBox.exec()
                return

        if not self.checkPtDir(folderPath):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("The selected folder does not contains valid patient data!")
            msgBox.exec()

            msgBox2 = QMessageBox()
            msgBox2.setInformativeText("If you are SURE you selected a patient folder, "+APPLABELS.APPNAME+" can try to update it.\nDo you want to update selected patient folder?")
            msgBox2.setIcon(QMessageBox.Warning)
            msgBox2.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox2.button(QMessageBox.Yes).setText("Yes")
            msgBox2.button(QMessageBox.No).setText("No")
            msgBox2.setDefaultButton(QMessageBox.No)
            ret = msgBox2.exec()
            if ret==QMessageBox.Yes:
                self.updatePtDir(folderPath)
            else:
                return
        self.openPtDir(folderPath)


    def getSuggestedPatientName(self):
        import re
        regex = re.compile('^'+self.SWANiGlobalConfig.getConfig("MAIN","patientsprefix")+'\d+$')
        fileList=[]
        for thisDir in os.listdir(self.SWANiGlobalConfig.getPatientsFolder()):
            if regex.match(thisDir): fileList.append(int(thisDir.replace(self.SWANiGlobalConfig['MAIN']['patientsprefix'],"")))

        if len(fileList)==0: return self.SWANiGlobalConfig['MAIN']['patientsprefix']+"1"
        return self.SWANiGlobalConfig['MAIN']['patientsprefix']+str(max(fileList)+1)


    def choseNewPtDir(self):
        text, ok = QInputDialog.getText(self, 'New patient',
            'Write the name of the new patient:', QLineEdit.Normal, self.getSuggestedPatientName())

        if not ok: return

        ptName=str(text)

        if ptName=="":
            msgBox = QMessageBox()
            msgBox.setText("Nome non valido: "+ptName)
            msgBox.exec()
            return

        if os.path.exists(os.path.join(self.SWANiGlobalConfig.getPatientsFolder(),ptName)):
            msgBox = QMessageBox()
            msgBox.setText("Esiste già un paziente con nome: "+ptName)
            msgBox.exec()
            return

        self.createNewPtDir(ptName)


    def setPatientsFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, 'Select the main working directory')
        if not os.path.exists(folderPath):
            return
        self.SWANiGlobalConfig.setConfig("MAIN","PatientsFolder",os.path.abspath(folderPath))
        self.SWANiGlobalConfig.save()
        os.chdir(folderPath)

    def createNewPtDir(self,ptName):
        baseFolder=os.path.abspath(os.path.join(self.SWANiGlobalConfig.getPatientsFolder(),ptName))

        for folder in self.SWANiGlobalConfig["DEFAULTFOLDERS"]:
            os.makedirs(os.path.join(baseFolder,self.SWANiGlobalConfig['DEFAULTFOLDERS'][folder]),exist_ok=True)

        msgBox = QMessageBox()
        msgBox.setText("New patient created in: "+baseFolder)
        msgBox.exec()

        self.openPtDir(baseFolder)

    def checkPtDir(self,dirPath):
        for folder in self.SWANiGlobalConfig["DEFAULTFOLDERS"]:
            if not os.path.exists(os.path.join(dirPath,self.SWANiGlobalConfig["DEFAULTFOLDERS"][folder])):
               return False
        return True

    def updatePtDir(self,dirPath):
        for folder in self.SWANiGlobalConfig["DEFAULTFOLDERS"]:
            if not os.path.exists(os.path.join(dirPath,self.SWANiGlobalConfig["DEFAULTFOLDERS"][folder])):
               os.makedirs(os.path.join(dirPath,self.SWANiGlobalConfig['DEFAULTFOLDERS'][folder]),exist_ok=True)

    def editConfig(self):
        if self.check_running_wfs():
            msgBox = QMessageBox()
            msgBox.setText("Prefecences disabled during workflow execution!")
            msgBox.exec()
            return
        self.w=preferencesWindow(self.SWANiGlobalConfig,self)
        self.w.exec()
        self.reset_wfs()


    def check_running_wfs(self):
        for pt in self.ptTabsArray:
            if hasattr(pt,"wf_process") and pt.wf_process.is_alive():
                return True
        return False

    def reset_wfs(self):
        for pt in self.ptTabsArray:
            pt.reset_wf()

    def toggleShortcut(self):
        if self.SWANiGlobalConfig['MAIN']['shortcutPath']=="":
            
            setattr(pyshortcuts.shortcut,"shortcut",my_shortcut)
            
            if pyshortcuts.platform.startswith('darwin'):
                setattr(pyshortcuts.darwin,"shortcut",my_shortcut)
                iconFile=SWANi_supplement.appIcns_file
            else:
                iconFile=SWANi_supplement.appIcon_file
                setattr(pyshortcuts.linux,"shortcut",my_shortcut)
            
            scut = pyshortcuts.make_shortcut(APPLABELS.APPNAME, name=APPLABELS.APPNAME, icon=iconFile, terminal=False, executable=sys.executable+" -m")
            targets  = [os.path.join(f, scut.target) for f in (scut.desktop_dir, scut.startmenu_dir)]
            self.SWANiGlobalConfig['MAIN']['shortcutPath']="|".join(targets)
            msgBox = QMessageBox()
            msgBox.setText("Shortcut created!")
            msgBox.exec()
        else:
            targets=self.SWANiGlobalConfig['MAIN']['shortcutPath'].split("|")
            for fil in targets:
                if "SWANi" in fil and os.path.exists(fil):
                    if os.path.isdir(fil):
                        shutil.rmtree(fil,ignore_errors=True)
                    else:
                        os.remove(fil)
            self.SWANiGlobalConfig['MAIN']['shortcutPath']=""
            msgBox = QMessageBox()
            msgBox.setText("Shortcut removed!")
            msgBox.exec()
        self.SWANiGlobalConfig.save()

    def inizializeUI(self):
        self.resize(800,600)
        self.setWindowTitle('SWANi - Standardized Workflow for Advanced Neuro-imaging')


        self.statusBar().showMessage('')

        button_action = QAction(QIcon.fromTheme("document-open"),"Load existing patient", self)
        button_action.setStatusTip("Load patient data from the main working directory")
        button_action.triggered.connect(self.searchPtDir)

        button_action2 = QAction(QIcon.fromTheme("document-new"),"Create new patient", self)
        button_action2.setStatusTip("Add a new patient in the main working directory")
        button_action2.triggered.connect(self.choseNewPtDir)

        button_action3 = QAction(QIcon.fromTheme("application-exit"),"Exit "+APPLABELS.APPNAME, self)
        button_action3.triggered.connect(self.close)        

        button_action4 = QAction(QIcon.fromTheme("preferences-other"),"Preferences", self)
        button_action4.setStatusTip("Edit "+APPLABELS.APPNAME+" precerences")
        button_action4.triggered.connect(self.editConfig)

        button_action5 = QAction("Shortcut", self)
        button_action5.setStatusTip("Add/Remove "+APPLABELS.APPNAME+" shortcut")
        button_action5.triggered.connect(self.toggleShortcut)

        menu = self.menuBar()
        menu.setNativeMenuBar(False)
        file_menu = menu.addMenu("File")
        file_menu.addAction(button_action)
        file_menu.addAction(button_action2)
        file_menu.addAction(button_action3)
        tool_menu = menu.addMenu("Tools")
        tool_menu.addAction(button_action4)
        tool_menu.addAction(button_action5)


        self.mainTAB=QTabWidget(parent=self)
        self.mainTAB.setTabsClosable(True)
        self.mainTAB.tabCloseRequested.connect(self.closePt)
        self.setCentralWidget(self.mainTAB)
        self.homeTab = QWidget()

        self.mainTAB.addTab(self.homeTab,"Home")

        #rimozione tasto chiusura da tab home, a destra o sinistra in base allo stile
        self.mainTAB.tabBar().setTabButton(0, QTabBar.LeftSide,None)
        self.mainTAB.tabBar().setTabButton(0, QTabBar.RightSide,None)

        self.homeTabUI()

        self.ptTabsArray=[]

        self.setWindowIcon(QIcon(QPixmap(os.path.join(os.path.dirname(__file__),"icons/swan.png"))))

        self.show()

    def closePt(self,index):
        if index == -1: return

        tabItem = self.mainTAB.widget(index)
        if hasattr(tabItem,"wf_process") and tabItem.wf_process.is_alive():
            msgBox = QMessageBox()
            msgBox.setText("Cannot close a patient during workflow execution!")
            msgBox.exec()
            return

        tabItem.closeRoutine()
        self.ptTabsArray.remove(tabItem)
        self.mainTAB.removeTab(index)
        tabItem = None;

    def closeEvent(self, event):
        # evito la chiusura se il wf è in esecuzione
        if not self.check_running_wfs():
            return super(mainWindow,self).closeEvent(event)
        else:
            msgBox = QMessageBox()
            msgBox.setText("Cannot close SWANi during workflow execution!")
            msgBox.exec()
            event.ignore()

    def homeTabUI(self):
        layout = QGridLayout()

        boldFont=QFont()
        boldFont.setBold(True)
        titleFont=QFont()
        titleFont.setBold(True)
        titleFont.setPointSize(titleFont.pointSize()*1.5)
        x=0

        label_welcome1=QLabel("Welcome to SWANi!")
        label_welcome1.setFont(titleFont)
        label_welcome2=QLabel("SWANi (Standardized Workflow for Advanced Neuro-imaging) is a graphic tools for modular neuroimaging processing. With SWANi you can easily import and organize DICOM files from multiple sources, generate a pipeline based on available imaging modalities and export results in a multimodal scene.")
        label_welcome2.setWordWrap(True)
        label_welcome3=QLabel("SWANi does NOT implement processing software but integrates in a user-friendly interface many external applications, so make sure the check the following dependencies.")
        label_welcome3.setWordWrap(True)
        #label_welcome4=QLabel("To start, load an existing patient folder or create a new one.\n")
        label_welcome5=QLabel("SWANi is not meant for clinical use!\n\n")
        label_welcome5.setFont(boldFont)

        layout.addWidget(label_welcome1,x,0,1,2)
        x+=1
        layout.addWidget(label_welcome2,x,0,1,2)
        x+=1
        layout.addWidget(label_welcome3,x,0,1,2)
        x+=1
        #layout.addWidget(label_welcome4,x,0,1,2)
        #x+=1
        layout.addWidget(label_welcome5,x,0,1,2)
        x+=1

        label_main_dep=QLabel("External applications dependencies:")
        label_main_dep.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        label_main_dep.setFont(boldFont)
        layout.addWidget(label_main_dep,x,0,1,2)
        x+=1

        msg,self.dcm2niix=check_dcm2niix()
        x=self.add_home_entry(layout,msg,self.dcm2niix,x)

        msg,self.fsl=check_fsl()
        x=self.add_home_entry(layout,msg,self.fsl,x)

        msg,self.freesurfer=check_freesurfer()
        x=self.add_home_entry(layout,msg,self.freesurfer,x)

        msg,self.graphviz=check_graphviz()
        x=self.add_home_entry(layout,msg,self.graphviz,x)

        if self.SWANiGlobalConfig['MAIN']['slicerPath'] == '' or not os.path.exists(self.SWANiGlobalConfig['MAIN']['slicerPath']):
            self.slicerlabel_icon=QSvgWidget()
            self.slicerlabel_icon.setFixedSize(25,25)
            self.slicerlabel_icon.load(self.loadingMovie_file)
            layout.addWidget(self.slicerlabel_icon,x,0)
            self.slicerlabel=QLabel("Searching Slicer installation...")
            self.slicerlabel.setOpenExternalLinks(True)
            self.slicerlabel.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
            layout.addWidget(self.slicerlabel,x,1)
            x+=1

            self.SWANiGlobalConfig['MAIN']['slicerPath'] = ''
            slicerrun= check_slicer(x,parent=self)
            slicerrun.start()
            slicerrun.signal.slicer.connect(self.slicerrow)
        else:
            self.add_home_entry(layout,"Slicer detected",True,x)
        x+=1

        label_py_dep=QLabel("Python libraries dependencies:")
        label_py_dep.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        label_py_dep.setFont(boldFont)
        layout.addWidget(label_py_dep,x,0,1,2)
        x+=1

        requested_lib=['nipype','PySide6','pydicom','logging','configparser','psutil']

        for thislib in requested_lib:
            x=self.add_home_entry(layout,thislib,check_python_lib(thislib),x)

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(verticalSpacer,x,0,1,2)

        self.homeTab.setLayout(layout)

    def add_home_entry(self,gridlayout,msg,icon,x):
        label_icon=QLabel()
        label_icon.setFixedSize(25,25)
        label_icon.setScaledContents(True)
        if icon: label_icon.setPixmap(self.okIcon)
        else: label_icon.setPixmap(self.errorIcon)
        gridlayout.addWidget(label_icon,x,0)
        label=QLabel(msg)
        label.setOpenExternalLinks(True)
        label.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        gridlayout.addWidget(label,x,1)
        return (x+1)

    def slicerrow(self,cmd,msg,found,x):
        if found:
            self.SWANiGlobalConfig['MAIN']['slicerPath']=cmd
            self.SWANiGlobalConfig.save()
            self.slicerlabel_icon.load(self.okIcon_file)
        else:
            self.slicerlabel_icon.load(self.errorIcon_file)
        self.slicerlabel.setText(msg)


orig_shortcut=shcdef
def my_shortcut(script, userfolders, name=None, description=None, folder=None, working_dir=None,icon=None):
    r=orig_shortcut(script, userfolders, name=name, description=description, folder=folder, working_dir=working_dir,icon=icon)
    return Shortcut(APPLABELS.APPNAME, APPLABELS.APPNAME, r.icon, r.target, 
                                         working_dir, APPLABELS.APPNAME, APPLABELS.APPNAME,r.arguments, 
                                         r.desktop_dir, r.startmenu_dir)