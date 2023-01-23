import pydicom
import os
from PySide6.QtCore import Signal, QObject, QThread

class MySignal(QObject):
        sigLoop = Signal(int)
        sigFinish = Signal(object)

class dicomSearch(QThread):  
    
    def __init__(self, dicomPath, parent = None):
        super(dicomSearch,self).__init__(parent)
        if os.path.exists(os.path.abspath(dicomPath)):
            self.dicomPath=os.path.abspath(dicomPath)
            self.unsortedList=[]
        self.signal = MySignal()
    
    def clean_text(self,string):
        # clean and standardize text descriptions, which makes searching files easier
        forbidden_symbols = ["*", ".", ",", "\"", "\\", "/", "|", "[", "]", ":", ";", " "]
        for symbol in forbidden_symbols:
            string = string.replace(symbol, "_") # replace everything with an underscore
        return string.lower()

    def loadDir(self):
        if self.dicomPath=="": 
            return
        for root, dirs, files in os.walk(self.dicomPath):
            for file in files: 
                #if ".dcm" in file:# exclude non-dicoms, good for messy folders
                self.unsortedList.append(os.path.join(root, file))
               
        self.dicomTree={}
          
    def getFilesLen(self):
        if not hasattr(self, 'unsortedList'): return 0
        else: return len(self.unsortedList)
        
    def run(self):
    
        if len(self.unsortedList)==0:
            self.loadDir()
        
        for dicom_loc in self.unsortedList:
            self.signal.sigLoop.emit(1)
            # read the file
            if not os.path.exists(dicom_loc): continue
            ds = pydicom.read_file(dicom_loc, force=True)
           
            patientID = self.clean_text(ds.get("PatientID", "NA"))
            if patientID=="na": continue
        
            #seriesDescription = self.clean_text(ds.get("SeriesDescription", "NA"))
            seriesNumber = ds.get("SeriesNumber", "NA")
            studyInstanceUID = ds.get("StudyInstanceUID","NA")

            #in GE la maggior parte delle ricostruzioni sono DERIVED\SECONDARY
            if hasattr(ds, 'ImageType') and "DERIVED" in ds.ImageType and "SECONDARY" in ds.ImageType and not "ASL" in ds.ImageType: continue
            #in GE e SIEMENS l'immagine anatomica di ASL è ORIGINAL\PRIMARY\ASL    
            if hasattr(ds, 'ImageType') and "ORIGINAL" in ds.ImageType and "PRIMARY" in ds.ImageType and "ASL" in ds.ImageType: continue
            #in Philips e Siemens le ricostruzioni sono PROJECTION IMAGE
            if hasattr(ds, 'ImageType') and "PROJECTION IMAGE" in ds.ImageType: continue
        
                
            if not patientID in self.dicomTree: 
                self.dicomTree[patientID]={}
            if not studyInstanceUID in self.dicomTree[patientID]: 
                self.dicomTree[patientID][studyInstanceUID]={}
            if not seriesNumber in self.dicomTree[patientID][studyInstanceUID]: 
                self.dicomTree[patientID][studyInstanceUID][seriesNumber]=[]
            self.dicomTree[patientID][studyInstanceUID][seriesNumber].append(dicom_loc)
             
        self.signal.sigFinish.emit(self)
        
    def getPatientList(self):
        return list(self.dicomTree.keys())
        
    def getExamList(self,patient):
        if not patient in self.dicomTree: return []
        return list(self.dicomTree[patient].keys())
    
    def getSeriesList(self,patient,exam):
        if not patient in self.dicomTree: return []
        if not exam in self.dicomTree[patient]: return []
        return list(self.dicomTree[patient][exam].keys())
    
    def getSeriesFiles(self,patient,exam,serie):
        if not patient in self.dicomTree: return []
        if not exam in self.dicomTree[patient]: return []
        if not serie in self.dicomTree[patient][exam]: return []
        return list(self.dicomTree[patient][exam][serie])
        
    