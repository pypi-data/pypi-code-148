from PyQt5.QtWidgets import *
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PyQt5.QtGui import (QFont)
import API


class Ui_Dialog(object):
    def setupUi(self, Dialog, manager,modelList):
        if Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1004, 809)
        Dialog.setStyleSheet(u"background-color:#e3ddcf\n"
                             "")
        font = QFont()
        font.setFamily(u"Gisha")
        font.setBold(True)
        font.setWeight(75)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(True)
        self.tableWidget = QTableWidget(Dialog)
        if (self.tableWidget.columnCount() < 7):
            self.tableWidget.setColumnCount(7)
        font1 = QFont()
        font1.setFamily(u"Gisha")
        font1.setBold(True)
        font1.setWeight(75)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font1)
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font1)
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        font2 = QFont()
        font2.setBold(True)
        font2.setWeight(75)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font2)
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font1)
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font2)
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font2)
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setFont(font2)
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tableWidget.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QRect(40, 10, 811, 781))
        self.tableWidget.setFont(font1)
        self.tableWidget.setStyleSheet(u"")
        self.tableWidget.setFrameShape(QFrame.Box)
        self.tableWidget.setLineWidth(2)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tableWidget.setAutoScroll(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(Qt.DashLine)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(20)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setProperty("showSortIndicator", True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setMinimumSectionSize(23)
        self.tableWidget.verticalHeader().setDefaultSectionSize(35)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView:section{Background-color:#db8d39;}")

        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(880, 760, 91, 21))
        self.pushButton.setFont(font)
        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
        self.API = manager
        self.parser(modelList)
        self.pushButton.clicked.connect(Dialog.accept)
        # self.tableWidget.clicked.connect(self.update_models)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"load models", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"ID", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Area", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Fruit type", None))
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Fruit variety", None))
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Soil type", None))
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"Planting year", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"OK", None))

    # retranslateUi
    def parser(self,modelList):
        models = self.API.get_models()
        nb_row = len(models)
        self.tableWidget.setRowCount(nb_row)
        tmp_model=[]
        try:
            for m in enumerate(modelList):
                if not tmp_model.__contains__(m[1]):
                    tmp_model.append(m[1])
        except Exception as e:
            raise Exception('Error in loading models list')
        for index, model in enumerate(models):
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            # depends on state of 'Apply' or non-'Apply
            if tmp_model.__contains__(model.model_id):
                chkBoxItem.setCheckState(True)
            else:
                chkBoxItem.setCheckState(False)
            self.tableWidget.setItem(index, 0, chkBoxItem)
            # push all content into columns
            self.tableWidget.setItem(index, 1, QTableWidgetItem(model.get_model_id()))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(model.get_area().replace("_", " ")))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(model.get_fruit_type().replace("_", " ")))
            self.tableWidget.setItem(index, 4, QTableWidgetItem(model.get_fruit_variety().replace("_", " ")))
            self.tableWidget.setItem(index, 5, QTableWidgetItem(model.get_soil_type().replace("_", " ")))
            self.tableWidget.setItem(index, 6, QTableWidgetItem(model.get_planting_year().replace("_", " ")))

    def save(self):
        models_ids = []
        for row in range(self.tableWidget.rowCount()):
            _id = self.tableWidget.item(row, 1).text()
            if self.tableWidget.item(row, 0).checkState():
                models_ids.append(_id)

        return models_ids



