import os
from PySide6.QtWidgets import (QDialog,QLabel,QGridLayout,QLineEdit,QVBoxLayout,
                               QGroupBox,QPushButton,QFileDialog,QMessageBox,QCheckBox,
                               QComboBox,QStyle)

from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt,QCoreApplication

from SWANi.utils.APPLABELS import APPLABELS


class preferencesWindow(QDialog):
    
    def __init__(self,SWANiGlobalConfig,parent=None):
        super(preferencesWindow,self).__init__(parent)
        
        self.SWANiGlobalConfig=SWANiGlobalConfig
        self.restart=False
        self.setWindowTitle(APPLABELS.APPNAME+' - Preferences')
        
        pixmapi = getattr(QStyle, "SP_DirOpenIcon")
        iconOpenDir = self.style().standardIcon(pixmapi)
        
        layout=QVBoxLayout()
        
        groupBox1 = QGroupBox()
        grid1 = QGridLayout()
        groupBox1.setLayout(grid1)
        x=0
        
        self.inputs={}
        
        grid1.addWidget(QLabel("Main working directory"),x,0)
        self.inputs['MAIN.patientsfolder']=QLineEdit()
        self.inputs['MAIN.patientsfolder'].setReadOnly(True)
        self.inputs['MAIN.patientsfolder'].setText(self.SWANiGlobalConfig['MAIN']['patientsfolder'])
        grid1.addWidget(self.inputs['MAIN.patientsfolder'],x,1)
        patientsfolderButton=QPushButton()
        patientsfolderButton.setIcon(iconOpenDir)
        patientsfolderButton.clicked.connect(lambda checked=None, edit=self.inputs['MAIN.patientsfolder'], message="Select the main working directory": self.choseDir(edit,message))
        grid1.addWidget(patientsfolderButton,x,2)
        
        x+=1
        
        grid1.addWidget(QLabel("3D Slicer path"),x,0)
        self.inputs['MAIN.slicerPath']=QLineEdit()
        self.inputs['MAIN.slicerPath'].setReadOnly(True)
        self.inputs['MAIN.slicerPath'].setText(self.SWANiGlobalConfig['MAIN']['slicerPath'])
        grid1.addWidget(self.inputs['MAIN.slicerPath'],x,1)
        slicerfolderButton=QPushButton()
        slicerfolderButton.setIcon(iconOpenDir)
        slicerfolderButton.clicked.connect(lambda checked=None, edit=self.inputs['MAIN.slicerPath'], message="Select 3D Slicer executable": self.choseFile(edit,message))
        grid1.addWidget(slicerfolderButton,x,2)
        x+=1
        
        grid1.addWidget(QLabel("Default workflow"),x,0)
        self.inputs['MAIN.defaultWfType'] = QComboBox(self)
        
        for index, label in enumerate(APPLABELS.WFTYPES):
            self.inputs['MAIN.defaultWfType'].insertItem(index,label)
        
        self.inputs['MAIN.defaultWfType'].setCurrentIndex(self.SWANiGlobalConfig.getint('MAIN','defaultWfType'))
        
        grid1.addWidget(self.inputs['MAIN.defaultWfType'],x,1)
        x+=1
        
        grid1.addWidget(QLabel("Patient tab limit"),x,0)
        self.inputs['MAIN.maxPt']=QLineEdit()
        self.inputs['MAIN.maxPt'].setText(self.SWANiGlobalConfig['MAIN']['maxPt'])
        self.inputs['MAIN.maxPt'].setValidator(QIntValidator(1,4))
        grid1.addWidget(self.inputs['MAIN.maxPt'],x,1)
        x+=1
        
        grid1.addWidget(QLabel("CPU per Patient limit"),x,0)
        self.inputs['MAIN.maxPtCPU']=QLineEdit()
        self.inputs['MAIN.maxPtCPU'].setText(self.SWANiGlobalConfig['MAIN']['maxPtCPU'])
        self.inputs['MAIN.maxPtCPU'].setValidator(QIntValidator(-1,40))
        grid1.addWidget(self.inputs['MAIN.maxPtCPU'],x,1)
        
        
        groupBox2 = QGroupBox()
        grid2 = QGridLayout()
        groupBox2.setLayout(grid2)
        x=0
        
        self.inputs['MAIN.freesurfer']=QCheckBox()
        self.setCheckBox(self.inputs['MAIN.freesurfer'],self.SWANiGlobalConfig.getboolean('MAIN', 'freesurfer'))
        grid2.addWidget(self.inputs['MAIN.freesurfer'],x,0)
        grid2.addWidget(QLabel("FreeSurfer recon-all"),x,1)
        x+=1
        
        self.inputs['MAIN.hippoAmygLabels']=QCheckBox()
        self.setCheckBox(self.inputs['MAIN.hippoAmygLabels'],self.SWANiGlobalConfig.getboolean('MAIN', 'hippoAmygLabels'))
        grid2.addWidget(self.inputs['MAIN.hippoAmygLabels'],x,0)
        grid2.addWidget(QLabel("FreeSurfer hippocampal subfields"),x,1)
        x+=1
        
        self.inputs['MAIN.domap']=QCheckBox()
        self.setCheckBox(self.inputs['MAIN.domap'],self.SWANiGlobalConfig.getboolean('MAIN', 'domap'))
        grid2.addWidget(self.inputs['MAIN.domap'],x,0)
        grid2.addWidget(QLabel("DOmap algorithm"),x,1)
        x+=1
        
        self.inputs['OPTIONAL_SERIES.mr_flair2d']=QCheckBox()
        self.setCheckBox(self.inputs['OPTIONAL_SERIES.mr_flair2d'],self.SWANiGlobalConfig.getboolean('OPTIONAL_SERIES', 'mr_flair2d'))
        self.inputs['OPTIONAL_SERIES.mr_flair2d'].stateChanged.connect(self.setRestart)
        grid2.addWidget(self.inputs['OPTIONAL_SERIES.mr_flair2d'],x,0)
        grid2.addWidget(QLabel("2D Flair"),x,1)
        x+=1
        
        for index,key in enumerate(self.SWANiGlobalConfig.TRACTS):
            self.inputs['DEFAULTTRACTS.'+key]=QCheckBox()
            self.setCheckBox(self.inputs['DEFAULTTRACTS.'+key],self.SWANiGlobalConfig.getboolean('DEFAULTTRACTS', key))
            grid2.addWidget(self.inputs['DEFAULTTRACTS.'+key],x,0)
            grid2.addWidget(QLabel(self.SWANiGlobalConfig.TRACTS[key][0]+" reconstruction"),x,1)
            x+=1
        
        layout.addWidget(groupBox1)
        layout.addWidget(groupBox2)
        
        self.saveButton=QPushButton("Save preferences")
        self.saveButton.clicked.connect(self.savePreferences)
        layout.addWidget(self.saveButton)
        
        self.setLayout(layout)
        
    def choseDir(self,edit,message):
        folderPath = QFileDialog.getExistingDirectory(self, message)
        if not os.path.exists(folderPath):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Directory does not exists!")
            msgBox.exec()
            return
        edit.setText(folderPath)
        self.setRestart()
        
    def choseFile(self,edit,message):
        filePath, filter  = QFileDialog.getOpenFileName(self, message)
        if not os.path.exists(filePath):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("File does not exists!")
            msgBox.exec()
            return
        edit.setText(filePath)
        self.setRestart()
        
    def setCheckBox(self,checkBox,bool):
        if bool:
            checkBox.setCheckState(Qt.Checked)
        else:
            checkBox.setCheckState(Qt.Unchecked)
            
    def setRestart(self):
        self.restart=True
        self.saveButton.setText("Save preferences (SWANi will close and restart)")
            
    def savePreferences(self):
        for index, key in enumerate(self.inputs):
            splitted=key.split(".")
            value=None
            if type(self.inputs[key]) is QLineEdit:
                value=self.inputs[key].text()
            elif type(self.inputs[key]) is QComboBox:
                value=str(self.inputs[key].currentIndex())
            elif type(self.inputs[key]) is QCheckBox:
                if self.inputs[key].checkState()==Qt.Checked:
                    value='true'
                else:
                    value="false"
            
            if value!=None:
                self.SWANiGlobalConfig[splitted[0]][splitted[1]]=value
                
        self.SWANiGlobalConfig.save()
        
        self.accept()
        
        if self.restart:
            QCoreApplication.exit(APPLABELS.EXIT_CODE_REBOOT)    