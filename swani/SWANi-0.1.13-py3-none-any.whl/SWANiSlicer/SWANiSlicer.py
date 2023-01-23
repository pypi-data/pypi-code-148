from PySide6.QtCore import QThread, Signal, QObject
import os, subprocess

class SWANiSlicer_Signaler(QObject):
        export = Signal(str)        
        
class SWANiSlicer(QThread):    
    def __init__(self, slicerPath, parent = None):
        super(SWANiSlicer,self).__init__(parent)
        self.signal=SWANiSlicer_Signaler()
        self.slicerPath=slicerPath
        
    def run(self):
    
        #hasattr(slicer.moduleNames,'FreeSurferImporter')
        #######LIBGL_ALWAYS_SOFTWARE=true GALLIUM_DRIVER=llvmpipe#############
        
        cmd=self.slicerPath+" --no-splash --no-main-window --python-script "+os.path.join(os.path.dirname(__file__),"slicerScript.py")
        #cmd="LIBGL_ALWAYS_SOFTWARE=true GALLIUM_DRIVER=llvmpipe "+self.slicerPath+" --python-script "+os.path.join(os.path.dirname(__file__),"slicerScript.py")
        
        popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            print(stdout_line)
            if stdout_line.startswith('SLICERSWANLOADER: '):
                self.signal.export.emit(stdout_line.replace('SLICERSWANLOADER: ','').replace('\n',''))
        popen.stdout.close()
        popen.wait()
        self.signal.export.emit("ENDLOADING")