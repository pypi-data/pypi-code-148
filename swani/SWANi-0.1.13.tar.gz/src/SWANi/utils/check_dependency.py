from nipype.interfaces import dcm2nii, fsl, freesurfer
from PySide6.QtCore import QThread, Signal, QObject
from shutil import which
import os, sys, subprocess

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None

def check_dcm2niix():
    version=dcm2nii.Info.version()
    if version==None:
        return "dcm2niix not detected (<a href=\'https://github.com/rordenlab/dcm2niix#Install\'>installation info</a>)",False
    else:
        return ("dcm2niix detected ("+str(version)+")"),True

def check_fsl():
    version=fsl.base.Info.version()
    if version==None:
        return "FSL not detected (<a href='https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation'>installation info</a>)",False
    else:
        return ("FSL detected ("+str(version)+")"),True

def check_freesurfer():
    if freesurfer.base.Info.version()==None:
        return "FreeSurfer not detected (<a href='https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall'>installation info</a>)",False
    else:
        version=freesurfer.base.Info.looseversion()
        if not "FREESURFER_HOME" in os.environ:
            return ("FreeSurfer detected ("+str(version)+") but without environment configuration"),False
        file = os.path.join(os.environ["FREESURFER_HOME"],"license.txt")
        if os.path.exists(file):
            return ("FreeSurfer detected ("+str(version)+")"),True
        else:
            return ("FreeSurfer detected ("+str(version)+") but without a license key (<a href='https://surfer.nmr.mgh.harvard.edu/registration.html'>registration instruction</a>)"),False

def check_graphviz():
    if which("dot")==None:
        return "Graphviz not detected (<a href='https://graphviz.org/download/'>Installation info</a>)",False
    else:
        return ("Graphviz detected"),True

def check_python_lib(libname):
    return libname in sys.modules



class slicer_Signaler(QObject):
        slicer = Signal(str,str,bool,int)

class check_slicer(QThread):
    def __init__(self, x, parent = None):
        super(check_slicer,self).__init__(parent)
        self.signal=slicer_Signaler()
        self.x=x

    def run(self):
        import platform
        if platform.system()=="Darwin":
            findcmd="find /Applications -type f -wholename *app/Contents/bin/PythonSlicer -print 2>/dev/null"
            relpath="../MacOS/Slicer"
        elif platform.system()=="Linux":
            findcmd="find / -executable -type f -wholename *bin/PythonSlicer -print -quit 2>/dev/null"
            relpath="../Slicer"
        output=subprocess.run(findcmd, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        split=output.split("\n")
        cmd=''
        found=False
        for entry in split:
            if entry=='': continue
            cmd=os.path.abspath(os.path.join(os.path.dirname(entry),relpath))
            break
        if cmd == '' or not os.path.exists(cmd):
            msg="Slicer not detected (<a href='https://slicer.readthedocs.io/en/latest/user_guide/getting_started.html#installing-3d-slicer/'>Installation info</a>)"
        else:
            cmd2=cmd+" --no-splash --no-main-window --python-script "+os.path.join(os.path.dirname(__file__),"modulecheck.py")
            output2=subprocess.run(cmd2, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
            if 'MODULE FOUND' in output2:
                found=True
                msg="Slicer detected"
            else:
                msg="Slicer detected but without SlicerFreeSurfer extension (<a href='https://slicer.readthedocs.io/en/latest/user_guide/extensions_manager.html?highlight=extension%20manager'>Exstensions Manager info</a>)"

        self.signal.slicer.emit(cmd,msg,found,self.x)

    def terminate(self):
        return
