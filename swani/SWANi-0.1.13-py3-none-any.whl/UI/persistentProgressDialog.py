from PySide6.QtWidgets import QProgressDialog
from PySide6.QtCore import Qt

class persistentProgressDialog(QProgressDialog):

    def __init__ (self, labelText, minimum, maximum, parent=None):
        super(persistentProgressDialog,self).__init__(labelText, None, minimum, maximum, parent, Qt.WindowFlags())
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.WindowModal)
        self.setMinimumDuration(0)
        
    def keyPressEvent(self, event):
        if event.key() != Qt.Key_Escape:
            super(persistentProgressDialog,self).keyPressEvent(event)
            
    def increaseValue(self,x):
        if self.value()==0 and self.maximum()>1: 
            x=x+1
        self.setValue(self.value()+x)
        
    def closeEvent(self,event):
        event.ignore()

        