from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QWidget, QTableWidget, QComboBox, QVBoxLayout
import sys

class comboCompanies(QComboBox):
    def __init__(self,parent,LABEL_CATEGORY):
        super().__init__(parent)
        self.setStyleSheet('font-size: 15px')
        self.addItems(LABEL_CATEGORY)
        self.currentIndexChanged.connect(self.getComboValue)
        
    def getComboValue(self):
        print(self.currentText())
        
class TableWidget(QTableWidget):
    def __init__(self,df,LABEL_CATEGORY):
        super().__init__(1,3)
        
        self.setHorizontalHeaderLabels(['image','prediction','probability'])
        self.setColumnWidth(3,100)
        self.verticalHeader().setDefaultSectionSize(20)
        self.horizontalHeader().setDefaultSectionSize(150)
        self.les_classes = LABEL_CATEGORY
        self.dico_ = df
        self.load_data()
        
    def load_data(self):
        self.setRowCount(len(self.dico_['nom']))
        self.row=0
        for idx in range(len(self.dico_['nom'])):
            self.setItem(self.row,0,QTableWidgetItem(self.dico_['nom'][idx]))
            self.combo = comboCompanies(self,self.les_classes)
            self.setCellWidget(self.row,1,self.combo)
            self.combo.setCurrentText(self.dico_['prediction'][idx])
            self.setItem(self.row,2,QTableWidgetItem(str(self.dico_['prob'][idx])))
            self.row+=1