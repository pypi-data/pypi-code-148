import GUI_loadModels
import GUI_update_message
from Manager import projectsUI, plotsUI
import API
import MplCanvas
# builtin python
# import ray
# from multiprocessing import Pool

import datetime
from os import _exit
from pandas import unique
# Qt
from PyQt5.QtCore import (QCoreApplication, QMetaObject,
                          QRect, QSize, Qt, QDateTime, QDate, QTime)
from PyQt5.QtGui import (QCursor, QFont, QPixmap)
from PyQt5.QtWidgets import *


class Ui_Growth_Tool_main(object):

    def setupUi(self, Growth_Tool_main):
        self.tmp_model_list_change = []
        self.tmp_model_list_load=[]
        self.MainWindow = Growth_Tool_main
        self.shouldReset = True
        self.need=True
        if Growth_Tool_main.objectName():
            Growth_Tool_main.setObjectName(u"Growth_Tool_main")
        Growth_Tool_main.resize(1868, 991)
        Growth_Tool_main.setStyleSheet(u"background-color:#e3ddcf;\n"
                                       "")
        self.centralwidget = QWidget(Growth_Tool_main)
        self.centralwidget.setObjectName(u"centralwidget")

        self.gridLayout_30 = QGridLayout(self.centralwidget)
        self.gridLayout_30.setObjectName(u"gridLayout_30")

        self.font = QFont()
        self.font.setFamily(u"Gisha")
        self.font.setBold(True)
        self.font.setWeight(75)
        self.font1 = QFont()
        self.font1.setFamily(u"Gisha")
        self.font1.setPointSize(10)

        # input for reading block
        self.horizontalGroupBox_4 = QGroupBox(self.centralwidget)
        self.horizontalGroupBox_4.setObjectName(u"horizontalGroupBox_4")
        self.horizontalGroupBox_4.setMinimumSize(QSize(300, 80))
        self.horizontalGroupBox_4.setMaximumSize(QSize(300, 80))
        self.horizontalGroupBox_4.setFont(self.font)
        self.horizontalLayout_34 = QHBoxLayout(self.horizontalGroupBox_4)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setContentsMargins(20, 5, 20, 5)

        self.ScanDateEdit = QDateEdit(self.horizontalGroupBox_4)
        self.ScanDateEdit.setObjectName(u"ScanDateEdit")
        self.font4 = QFont()
        self.font4.setFamily(u"Fugaz One")
        self.ScanDateEdit.setFont(self.font)
        self.ScanDateEdit.setStyleSheet(u"color: black;")
        self.ScanDateEdit.setMinimumDateTime(QDateTime(QDate(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day), QTime(0, 0, 0)))
        self.ScanDateEdit.setMinimumDate(QDate(2010, 1, 1))
        self.ScanDateEdit.setCurrentSection(QDateTimeEdit.DaySection)
        self.ScanDateEdit.setCalendarPopup(True)

        self.horizontalLayout_34.addWidget(self.ScanDateEdit)

        self.comboBox_blockCode = QComboBox(self.horizontalGroupBox_4)
        self.comboBox_blockCode.setObjectName(u"comboBox_blockCode")
        self.comboBox_blockCode.setFont(self.font)
        self.comboBox_blockCode.setFrame(True)

        self.horizontalLayout_34.addWidget(self.comboBox_blockCode)

        self.gridLayout_30.addWidget(self.horizontalGroupBox_4, 2, 5, 1, 1)

        self.label_note = QLabel(self.centralwidget)
        self.label_note.setObjectName(u"label_note")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_note.sizePolicy().hasHeightForWidth())
        self.label_note.setSizePolicy(sizePolicy)
        self.label_note.setMinimumSize(QSize(350, 100))
        self.label_note.setMaximumSize(QSize(600, 100))
        self.label_note.setBaseSize(QSize(306, 0))
        self.label_note.setScaledContents(False)
        self.label_note.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.gridLayout_30.addWidget(self.label_note, 2, 0, 1, 5)

        self.horizontalLayout_43 = QHBoxLayout()
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.horizontalLayout_43.setContentsMargins(0, -1, -1, -1)
        self.apply_pushButton = QPushButton(self.centralwidget)
        self.apply_pushButton.setObjectName(u"apply_pushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(117)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.apply_pushButton.sizePolicy().hasHeightForWidth())
        self.apply_pushButton.setSizePolicy(sizePolicy1)
        self.apply_pushButton.setMinimumSize(QSize(117, 0))
        self.font2 = QFont()
        self.font2.setFamily(u"Gisha")
        self.font2.setPointSize(14)
        self.font2.setBold(False)
        self.font2.setItalic(False)
        self.font2.setUnderline(False)
        self.font2.setWeight(50)
        self.font2.setStrikeOut(False)
        self.font2.setKerning(True)

        self.apply_pushButton.setFont(self.font2)
        self.apply_pushButton.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.apply_pushButton.setAcceptDrops(False)
        self.apply_pushButton.setToolTipDuration(-1)
        self.apply_pushButton.setStyleSheet(u"background-color:#b0a7a2;")
        self.apply_pushButton.setAutoDefault(False)

        self.horizontalLayout_43.addWidget(self.apply_pushButton, alignment=Qt.AlignCenter)

        self.close_pushButton = QPushButton(self.centralwidget)
        self.close_pushButton.setObjectName(u"close_pushButton")
        sizePolicy1.setHeightForWidth(self.close_pushButton.sizePolicy().hasHeightForWidth())
        self.close_pushButton.setSizePolicy(sizePolicy1)
        self.close_pushButton.setMinimumSize(QSize(117, 0))
        self.font3 = QFont()
        self.font3.setFamily(u"Gisha")
        self.font3.setPointSize(14)
        self.close_pushButton.setFont(self.font3)
        self.close_pushButton.setStyleSheet(u"background-color:#b0a7a2;")

        self.horizontalLayout_43.addWidget(self.close_pushButton, alignment=Qt.AlignCenter)

        self.gridLayout_30.addLayout(self.horizontalLayout_43, 2, 6, 1, 1)

        self.logo = QLabel(self.centralwidget)
        self.logo.setObjectName(u"logo")
        self.logo.setEnabled(True)
        self.logo.setMinimumSize(QSize(261, 101))
        self.logo.setMaximumSize(QSize(261, 101))
        self.logo.setPixmap(QPixmap(u"dep/logo-fruitspec.png"))
        self.logo.setScaledContents(True)

        self.gridLayout_30.addWidget(self.logo, 0, 0, 1, 1)

        self.gridGroupBox_1 = QGroupBox(self.centralwidget)
        self.gridGroupBox_1.setObjectName(u"gridGroupBox_1")
        self.gridGroupBox_1.setMinimumSize(QSize(551, 120))
        self.gridGroupBox_1.setMaximumSize(QSize(551, 120))
        self.font5 = QFont()
        self.font5.setFamily(u"Gisha")
        self.font5.setPointSize(11)
        self.font5.setBold(True)
        self.font5.setWeight(75)
        self.gridGroupBox_1.setFont(self.font5)
        self.gridLayout_13 = QGridLayout(self.gridGroupBox_1)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(30, 10, 0, 30)
        self.plantingYear_label_value = QLabel(self.gridGroupBox_1)
        self.plantingYear_label_value.setObjectName(u"plantingYear_label_value")

        self.gridLayout_13.addWidget(self.plantingYear_label_value, 1, 4, 1, 1)

        self.name_label = QLabel(self.gridGroupBox_1)
        self.name_label.setObjectName(u"name_label")
        self.font6 = QFont()
        self.font6.setFamily(u"Gisha")
        self.font6.setPointSize(10)
        self.font6.setBold(True)
        self.font6.setWeight(75)
        self.name_label.setFont(self.font6)

        self.gridLayout_13.addWidget(self.name_label, 0, 0, 1, 1)

        self.fruitType_label = QLabel(self.gridGroupBox_1)
        self.fruitType_label.setObjectName(u"fruitType_label")
        self.fruitType_label.setFont(self.font6)

        self.gridLayout_13.addWidget(self.fruitType_label, 0, 1, 1, 1)

        self.rootstock_label_value = QLabel(self.gridGroupBox_1)
        self.rootstock_label_value.setObjectName(u"rootstock_label_value")

        self.gridLayout_13.addWidget(self.rootstock_label_value, 1, 5, 1, 1)

        self.rootstock_label = QLabel(self.gridGroupBox_1)
        self.rootstock_label.setObjectName(u"rootstock_label")
        self.rootstock_label.setFont(self.font6)

        self.gridLayout_13.addWidget(self.rootstock_label, 0, 5, 1, 1)

        self.soiltype_label_value = QLabel(self.gridGroupBox_1)
        self.soiltype_label_value.setObjectName(u"soiltype_label_value")

        self.gridLayout_13.addWidget(self.soiltype_label_value, 1, 3, 1, 1)

        self.plantingYear_label = QLabel(self.gridGroupBox_1)
        self.plantingYear_label.setObjectName(u"plantingYear_label")
        self.plantingYear_label.setFont(self.font6)

        self.gridLayout_13.addWidget(self.plantingYear_label, 0, 4, 1, 1)

        self.fruitType_label_value = QLabel(self.gridGroupBox_1)
        self.fruitType_label_value.setObjectName(u"fruitType_label_value")

        self.gridLayout_13.addWidget(self.fruitType_label_value, 1, 1, 1, 1)

        self.fruitVariety_label = QLabel(self.gridGroupBox_1)
        self.fruitVariety_label.setObjectName(u"fruitVariety_label")
        self.fruitVariety_label.setFont(self.font6)

        self.gridLayout_13.addWidget(self.fruitVariety_label, 0, 2, 1, 1)

        self.name_label_value = QLabel(self.gridGroupBox_1)
        self.name_label_value.setObjectName(u"name_label_value")

        self.gridLayout_13.addWidget(self.name_label_value, 1, 0, 1, 1)

        self.soilType_label = QLabel(self.gridGroupBox_1)
        self.soilType_label.setObjectName(u"soilType_label")
        self.soilType_label.setFont(self.font6)

        self.gridLayout_13.addWidget(self.soilType_label, 0, 3, 1, 1)

        self.fruitVar_label_value = QLabel(self.gridGroupBox_1)
        self.fruitVar_label_value.setObjectName(u"fruitVar_label_value")

        self.gridLayout_13.addWidget(self.fruitVar_label_value, 1, 2, 1, 1)

        self.gridLayout_30.addWidget(self.gridGroupBox_1, 0, 4, 1, 1)

        self.verticalGroupBox_5 = QGroupBox(self.centralwidget)
        self.verticalGroupBox_5.setObjectName(u"verticalGroupBox_5")
        self.verticalGroupBox_5.setMinimumSize(QSize(251, 120))
        self.verticalGroupBox_5.setMaximumSize(QSize(251, 120))
        self.verticalGroupBox_5.setFont(self.font5)
        self.verticalLayout_53 = QVBoxLayout(self.verticalGroupBox_5)
        self.verticalLayout_53.setObjectName(u"verticalLayout_53")
        self.tableWidget = QTableWidget(self.verticalGroupBox_5)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.tableWidget.rowCount() < 2):
            self.tableWidget.setRowCount(2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tableWidget.setItem(0, 0, __qtablewidgetitem5)
        self.tableWidget.setObjectName(u"tableWidget")
        self.font7 = QFont()
        self.font7.setFamily(u"Gisha")
        self.tableWidget.setFont(self.font7)
        self.tableWidget.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.tableWidget.setAutoFillBackground(True)
        self.tableWidget.setStyleSheet(u"")
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setFrameShadow(QFrame.Plain)
        self.tableWidget.setLineWidth(0)
        self.tableWidget.setMidLineWidth(0)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tableWidget.setAutoScroll(True)
        self.tableWidget.setTextElideMode(Qt.ElideLeft)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(Qt.DashDotLine)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(29)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(55)
        self.tableWidget.verticalHeader().setDefaultSectionSize(23)

        self.verticalLayout_53.addWidget(self.tableWidget)

        self.gridLayout_30.addWidget(self.verticalGroupBox_5, 0, 5, 1, 1)

        # button for models updating
        self.updateModels_pushButton = QPushButton(self.centralwidget)
        self.updateModels_pushButton.setObjectName(u"updateModels_pushButton")
        sizePolicy1.setHeightForWidth(self.updateModels_pushButton.sizePolicy().hasHeightForWidth())
        self.updateModels_pushButton.setSizePolicy(sizePolicy1)
        self.updateModels_pushButton.setMinimumSize(QSize(117, 0))
        self.font3 = QFont()
        self.font3.setFamily(u"Gisha")
        self.font3.setPointSize(14)
        self.updateModels_pushButton.setFont(self.font3)
        self.updateModels_pushButton.setStyleSheet(u"background-color:#b0a7a2;")

        self.gridLayout_30.addWidget(self.updateModels_pushButton, 0, 2, 1, 1)

        # main group of display
        self.toolBox = QToolBox(self.centralwidget)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setEnabled(True)
        self.toolBox.setMinimumSize(QSize(1618, 700))
        # self.toolBox.setMaximumSize(QSize(2000, 700))
        self.toolBox.setBaseSize(QSize(1618, 700))
        self.toolBox.setFont(self.font5)
        self.toolBox.setToolTipDuration(-1)
        self.toolBox.setStyleSheet(u"")
        self.toolBox.setFrameShape(QFrame.WinPanel)
        self.toolBox.setFrameShadow(QFrame.Sunken)
        self.toolBox.setLineWidth(6)
        self.toolBox.setMidLineWidth(11)

        self.manager = QWidget()
        self.manager.setObjectName(u"manager")
        self.manager.setGeometry(QRect(0, 0, 1846, 618))
        self.manager.setStyleSheet(u"background-color:#99ada7;")

        self.formLayout_manager = QGridLayout(self.manager)
        self.formLayout_manager.setObjectName(u"formLayout_manager")
        self.formLayout_manager.setHorizontalSpacing(10)

        self.toolBox.addItem(self.manager, u"Automation manager")

        self.pre = QWidget()
        self.pre.setObjectName(u"pre")
        self.pre.setGeometry(QRect(0, 0, 1846, 680))
        self.pre.setFont(self.font7)
        self.pre.setLayoutDirection(Qt.LeftToRight)
        self.pre.setAutoFillBackground(False)
        self.pre.setStyleSheet(u"background-color:#99ada7;")

        self.formLayout_pre = QGridLayout(self.pre)
        self.formLayout_pre.setObjectName(u"formLayout_pre")
        self.formLayout_pre.setContentsMargins(150, 20, 100, 20)

        self.toolBox.addItem(self.pre, u"Samples check")

        self.A = QWidget()
        self.A.setObjectName(u"A")
        self.A.setGeometry(QRect(0, 0, 1846, 680))
        self.A.setFont(self.font7)
        self.A.setLayoutDirection(Qt.LeftToRight)
        self.A.setAutoFillBackground(False)
        self.A.setStyleSheet(u"background-color:#99ada7;")

        self.formLayout_A = QGridLayout(self.A)
        self.formLayout_A.setObjectName(u"formLayout_A")

        self.loadModels_pushButton = QPushButton(self.A)
        self.loadModels_pushButton.setObjectName(u"loadModels_pushButton")
        self.loadModels_pushButton.setMinimumSize(QSize(120, 31))
        self.loadModels_pushButton.setMaximumSize(QSize(120, 31))
        self.loadModels_pushButton.setFont(self.font2)
        self.loadModels_pushButton.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.loadModels_pushButton.setAcceptDrops(False)
        self.loadModels_pushButton.setToolTipDuration(-1)
        self.loadModels_pushButton.setStyleSheet(u"background-color:#e3ddcf;")
        self.loadModels_pushButton.setAutoDefault(False)

        self.formLayout_A.addWidget(self.loadModels_pushButton, 1, 1)

        self.scrollArea_1 = QScrollArea(self.A)
        self.scrollArea_1.setObjectName(u"scrollArea_1")
        self.scrollArea_1.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea_1.sizePolicy().hasHeightForWidth())
        self.scrollArea_1.setSizePolicy(sizePolicy1)
        self.scrollArea_1.setMinimumSize(QSize(1828, 563))
        # self.scrollArea_1.setMaximumSize(QSize(1828, 563))
        self.scrollArea_1.setWidgetResizable(True)
        self.scrollAreaWidgetContents_1 = QWidget()
        self.scrollAreaWidgetContents_1.setObjectName(u"scrollAreaWidgetContents_1")
        self.scrollAreaWidgetContents_1.setEnabled(True)
        self.scrollAreaWidgetContents_1.setGeometry(QRect(0, 0, 1824, 559))
        # self.scrollAreaWidgetContents_1.setMinimumSize(QSize(1822, 559))
        # self.scrollAreaWidgetContents_1.setMaximumSize(QSize(1824, 559))
        self.gridLayout_1 = QGridLayout(self.scrollAreaWidgetContents_1)
        self.gridLayout_1.setObjectName(u"gridLayout_1")
        self.scrollArea_1.setWidget(self.scrollAreaWidgetContents_1)

        self.formLayout_A.addWidget(self.scrollArea_1, 0, 1)
        self.formLayout_A.setContentsMargins(20, 20, 20, 10)
        self.formLayout_A.setVerticalSpacing(15)
        self.toolBox.addItem(self.A, u"Optimized models")

        self.C = QWidget()
        self.C.setObjectName(u"C")
        self.C.setGeometry(QRect(0, 0, 1846, 618))
        self.C.setStyleSheet(u"background-color:#99ada7;")
        self.formLayout_C = QGridLayout(self.C)
        self.formLayout_C.setObjectName(u"formLayout_C")
        self.scrollArea_2 = QScrollArea(self.C)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy2)
        self.scrollArea_2.setMinimumSize(QSize(1828, 563))
        # self.scrollArea_2.setMaximumSize(QSize(1828, 563))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setEnabled(True)
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 1824, 559))
        # self.scrollAreaWidgetContents_2.setMinimumSize(QSize(1824, 559))
        # self.scrollAreaWidgetContents_2.setMaximumSize(QSize(1824, 559))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.formLayout_C.addWidget(self.scrollArea_2, 0, 0)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")

        self.save_pushButton = QPushButton(self.C)
        self.save_pushButton.setObjectName(u"save_pushButton")
        self.save_pushButton.setMinimumSize(QSize(120, 31))
        self.save_pushButton.setMaximumSize(QSize(120, 31))
        self.save_pushButton.setFont(self.font2)
        self.save_pushButton.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.save_pushButton.setAcceptDrops(False)
        self.save_pushButton.setToolTipDuration(-1)
        self.save_pushButton.setStyleSheet(u"background-color:#e3ddcf;")
        self.save_pushButton.setAutoDefault(False)

        self.horizontalLayout_37.addWidget(self.save_pushButton, alignment=Qt.AlignLeft)

        self.saveS3_pushButton = QPushButton(self.C)
        self.saveS3_pushButton.setObjectName(u"saveS3_pushButton")
        self.saveS3_pushButton.setMinimumSize(QSize(150, 31))
        self.saveS3_pushButton.setMaximumSize(QSize(150, 31))
        self.saveS3_pushButton.setFont(self.font2)
        self.saveS3_pushButton.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.saveS3_pushButton.setAcceptDrops(False)
        self.saveS3_pushButton.setToolTipDuration(-1)
        self.saveS3_pushButton.setStyleSheet(u"background-color:#e3ddcf;")
        self.saveS3_pushButton.setAutoDefault(False)

        self.horizontalLayout_37.addWidget(self.saveS3_pushButton, alignment=Qt.AlignLeft)

        # # combobox of fruit variety to be calculated for weight
        # self.comboBox_varFruit_to_weight = CheckableComboBox(parent=self.C)
        # self.comboBox_varFruit_to_weight.setObjectName(u"comboBox_comboBox_varFruit_to_weight")
        # self.comboBox_varFruit_to_weight.setFont(self.font1)
        # self.comboBox_varFruit_to_weight.setMaximumSize(QSize(160, 20))
        # self.comboBox_varFruit_to_weight.setMinimumSize(QSize(160, 20))
        #
        # self.horizontalLayout_37.addWidget(self.comboBox_varFruit_to_weight, stretch=1, alignment=Qt.AlignLeft)

        self.formLayout_C.addLayout(self.horizontalLayout_37, 1, 0)

        self.formLayout_C.setContentsMargins(20, 20, 20, 10)
        self.formLayout_C.setVerticalSpacing(15)
        self.toolBox.addItem(self.C, u"Report distributions")

        self.gridLayout_30.addWidget(self.toolBox, 1, 0, 1, 7)

        self.toolBox.layout().setSpacing(0)

        Growth_Tool_main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Growth_Tool_main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1868, 21))
        Growth_Tool_main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Growth_Tool_main)
        self.statusbar.setObjectName(u"statusbar")
        Growth_Tool_main.setStatusBar(self.statusbar)

        # implemented
        self.retranslateUi(Growth_Tool_main)
        QMetaObject.connectSlotsByName(Growth_Tool_main)

        self.connectors()
        self.manage_sections(1)
        self.API_manager = API.Manager()

    def retranslateUi(self, Growth_Tool_main):
        self.label_note_set_text('Please select')
        Growth_Tool_main.setWindowTitle(QCoreApplication.translate("Growth_Tool_main", u"Growth Tool", None))
        self.apply_pushButton.setToolTip("")
        self.apply_pushButton.setText(QCoreApplication.translate("Growth_Tool_main", u"Apply", None))
        self.close_pushButton.setText(QCoreApplication.translate("Growth_Tool_main", u"Close", None))
        self.updateModels_pushButton.setText(QCoreApplication.translate("Growth_Tool_main", u"Update models", None))
        self.horizontalGroupBox_4.setTitle(QCoreApplication.translate("Growth_Tool_main", u"Select block ", None))
        self.logo.setText("")
        self.gridGroupBox_1.setTitle(QCoreApplication.translate("Growth_Tool_main", u"Block information", None))
        self.plantingYear_label_value.setText("")
        self.name_label.setText(QCoreApplication.translate("Growth_Tool_main", u"Name", None))
        self.fruitType_label.setText(QCoreApplication.translate("Growth_Tool_main", u"Fruit type", None))
        self.rootstock_label_value.setText("")
        self.rootstock_label.setText(QCoreApplication.translate("Growth_Tool_main", u"Rootstock", None))
        self.soiltype_label_value.setText("")
        self.plantingYear_label.setText(QCoreApplication.translate("Growth_Tool_main", u"Planting year", None))
        self.fruitType_label_value.setText("")
        self.fruitVariety_label.setText(QCoreApplication.translate("Growth_Tool_main", u"Fruit variety", None))
        self.name_label_value.setText("")
        self.soilType_label.setText(QCoreApplication.translate("Growth_Tool_main", u"Soil type", None))
        self.fruitVar_label_value.setText("")
        self.verticalGroupBox_5.setTitle(QCoreApplication.translate("Growth_Tool_main", u"Scan samples", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Growth_Tool_main", u"small", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Growth_Tool_main", u"medium", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Growth_Tool_main", u"large", None))
        ___qtablewidgetitem3 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Growth_Tool_main", u"1st", None))
        ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Growth_Tool_main", u"2nd", None))

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        # if QT_CONFIG(tooltip)
        self.loadModels_pushButton.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.loadModels_pushButton.setText(QCoreApplication.translate("Growth_Tool_main", u"Load models", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.A), QCoreApplication.translate("Growth_Tool_main", u"Optimized models", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.manager), QCoreApplication.translate("Growth_Tool_main", u"Manager", None))
        # if QT_CONFIG(tooltip)
        self.save_pushButton.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.save_pushButton.setText(QCoreApplication.translate("Growth_Tool_main", u"Save", None))
        self.saveS3_pushButton.setText(QCoreApplication.translate("Growth_Tool_main", u"Portal upload", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.C), QCoreApplication.translate("Growth_Tool_main", u"Report distributions", None))

    def load_models_form(self):
        dialog = QDialog()
        dialog.ui = GUI_loadModels.Ui_Dialog()
        dialog.ui.setupUi(dialog,manager = self.API_manager,modelList=self.tmp_model_list_load)
        if dialog.exec_() == QDialog.Accepted:
            try:
                ids = dialog.ui.save()
                for m in enumerate(self.tmp_model_list_load):
                    if not ids.__contains__(m[1]):
                        ids.append(m[1])
                ids = list(set(ids))
                self.shouldReset=True
                self.need=False
                self.set_models_section(ids)
            except Exception as e:
                self.label_note_set_text(str(e))
        dialog.show()

    def update_dialog_message(self):
        dialog = QDialog()
        dialog.ui = GUI_update_message.Ui_Dialog()
        dialog.ui.setupUi(dialog)
        if dialog.exec_() == QDialog.Accepted:
            dialog.ui.update_models()
            self.label_note_set_text('Models have been updated')
        dialog.show()

    def connectors(self):
        self.ScanDateEdit.dateChanged.connect(self.set_block_list)

        self.close_pushButton.clicked.connect(self.exitProgram)

        self.apply_pushButton.clicked.connect(self.set_samples)

        self.toolBox.currentChanged.connect(self.manage_sections)

        self.updateModels_pushButton.clicked.connect(self.update_dialog_message)

        self.loadModels_pushButton.clicked.connect(self.load_models_form)

        self.save_pushButton.clicked.connect(self.save)

        self.saveS3_pushButton.clicked.connect(self.upload_s3)

    def manage_sections(self, i):
        if i == 0:
            self.auto_mode()
            self.toolBox.setItemEnabled(0, True)
            self.toolBox.setItemEnabled(1, True)
            self.apply_pushButton.setEnabled(False)
            self.comboBox_blockCode.setEnabled(False)
            self.ScanDateEdit.setEnabled(False)
            self.toolBox.setItemEnabled(2, False)
            self.toolBox.setItemEnabled(3, False)
            #self.shouldReset=False
        elif i == 1:
            # ray.shutdown()
            self.toolBox.setItemEnabled(0, False)
            self.toolBox.setItemEnabled(2, False)
            self.toolBox.setItemEnabled(3, False)
            self.apply_pushButton.setEnabled(True)
            self.comboBox_blockCode.setEnabled(True)
            self.ScanDateEdit.setEnabled(True)
            self.shouldReset=False

        elif i == 2:
            self.need=True
            self.set_models_section()
            self.toolBox.setItemEnabled(3, True)
        elif i == 3:
            self.set_report_section()
            self.shouldReset=False

    def auto_mode(self):
        # ray.init()
        def emit_plots(i, j):
            self.label_note_set_text()
            # @ray.remote
            # def run_plot(id, logger):
            #     return API.Manager.get_results(id, logger)

            try:
                project = int(self.projects_object.get_table().loc[i, 'project_id'])
                plots_object = plotsUI(self.manager, project)

                # parallel_set = []
                # p = Pool(processes=4)
                ids = plots_object.get_blocks_id()

                for index, id in enumerate(ids):
                    dialog_logger = plots_object.get_dialog_logger(index, id)
                    # parallel_set.append(run_plot.remote(id, dialog_logger.getLogger()))
                    # parallel_set.append([id, dialog_logger.getLogger()])
                    size, redFlag, result, done = API.Manager.get_results(id, dialog_logger.getLogger())
                    plots_object.set_results(index, size, redFlag, result, done)


                # print(datetime.datetime.now())
                # results = p.map(run_plot, parallel_set)
                # results = ray.get(parallel_set)


                # for (index, id), (size, redFlag, result, done) in zip(enumerate(ids), results):
                #     TODO
                    # plots_object.set_results(index, size, redFlag, result, done)

            except Exception as e:
                self.label_note_set_text(repr(e))
                plots_object = plotsUI(self.manager)
            finally:
                plots_table = plots_object.get_Qtable()
                self.formLayout_manager.addWidget(plots_table, 0, 1)

        self.projects_object = projectsUI(self.manager)
        self.projects_table = self.projects_object.get_Qtable()
        self.formLayout_manager.addWidget(self.projects_table, 0, 0)
        self.formLayout_manager.setColumnStretch(0, 2)
        self.formLayout_manager.setColumnStretch(1, 5)

        # connector to emit plots according double click on project
        self.projects_object.connect_project(func=emit_plots)

        # empty plots table format
        plots_object = plotsUI(self.manager)
        plots_table = plots_object.get_Qtable()
        self.formLayout_manager.addWidget(plots_table, 0, 1)

    def set_block_list(self):
        self.comboBox_blockCode.clear()
        date = self.ScanDateEdit.date().toPyDate()
        required_date = '"{0}-{1}-{2}T00:00:00.000Z"'.format(date.year, date.month, date.day)
        self._plots = API.Manager.get_1st_scan_plots(required_date)
        if not self._plots.empty:
            for block_code in self._plots['plot_code']:
                self.comboBox_blockCode.addItem(block_code)
        else:
            self.comboBox_blockCode.clear()

    def set_samples(self):
        def reset():
            # reset graph in bin one
            for k in reversed(range(self.formLayout_pre.count())):
                self.formLayout_pre.itemAt(k).widget().setParent(None)
            self.stdLabels, self.ButtonMean, self.ButtonMode = None, None, None

        reset()
        self.toolBox.setCurrentIndex(1)
        self.shouldReset = True
        self.tmp_model_list_load.clear()
        try:
            if self.comboBox_blockCode.currentText() == '':
                return
            _id_plot = self._plots[self._plots['plot_code'] == self.comboBox_blockCode.currentText()]['project_plot_id'].iloc[0]
            self.API_manager.set_manual_block(_id_plot)
            self.set_graph_model(widget=self.pre, layout=self.formLayout_pre, info=self.API_manager.get_info()['distribution_info']['diameter'].round(), type='bin1')
            self.statistics_ui()
            self.label_note_set_text("")
        except Exception as e:
            self.label_note_set_text(str(e))
        finally:
            # set upper Ui with information of block
            try:
                info = self.API_manager.get_info()
                self.name_label_value.setText(info['block_name'])
                self.fruitType_label_value.setText(info['fruit_type'].replace("_", " "))
                self.fruitVar_label_value.setText(info['fruit_variety'].replace("_", " "))
                self.soiltype_label_value.setText(info['soil_type'].replace("_", " "))
                self.plantingYear_label_value.setText(info['planting_year'])
                self.rootstock_label_value.setText(info['rootstock'].replace("_", " "))
                self.tableWidget.setItem(0, 0, QTableWidgetItem(str(info["scans"]["1st"]["small"])))
                self.tableWidget.setItem(0, 1, QTableWidgetItem(str(round(info["scans"]["1st"]["medium"], 2))))
                self.tableWidget.setItem(0, 2, QTableWidgetItem(str(info["scans"]["1st"]["large"])))
                try:
                    self.tableWidget.setItem(1, 0, QTableWidgetItem(str(info["scans"]["2nd"]["small"])))
                    self.tableWidget.setItem(1, 1, QTableWidgetItem(str(round(info["scans"]["2nd"]["medium"], 2))))
                    self.tableWidget.setItem(1, 2, QTableWidgetItem(str(info["scans"]["2nd"]["large"])))
                except:
                    # only one scan
                    self.tableWidget.setItem(1, 0, QTableWidgetItem(str()))
                    self.tableWidget.setItem(1, 1, QTableWidgetItem(str()))
                    self.tableWidget.setItem(1, 2, QTableWidgetItem(str()))
            except Exception as e:
                self.tableWidget.clearContents()
                self.name_label_value.clear()
                self.fruitType_label_value.clear()
                self.fruitVar_label_value.clear()
                self.soiltype_label_value.clear()
                self.plantingYear_label_value.clear()
                self.rootstock_label_value.clear()
                #self.label_note_set_text(str(e))

    def statistics_ui(self):
        if self.stdLabels is None and self.ButtonMode is None and self.ButtonMean is None:
            self.verticalLayoutWidget = QWidget(self.pre)
            self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
            self.verticalLayoutWidget.setGeometry(QRect(50, 40, 311, 151))

            self.formLayout_pre.addWidget(self.verticalLayoutWidget, 0, 0, 1, 1)

            self.verticalLayoutStat = QVBoxLayout(self.verticalLayoutWidget)
            self.verticalLayoutStat.setObjectName(u"verticalLayout")
            self.verticalLayoutStat.setContentsMargins(0, 0, 0, 0)

            self.stdLabels = QLabel(self.verticalLayoutWidget)
            self.stdLabels.setFont(self.font2)
            self.stdLabels.setObjectName(u"stdLabels")
            self.stdLabels.setMaximumSize(QSize(170, 31))
            self.stdLabels.setStyleSheet(u"background-color:#e3ddcf;")
            self.stdLabels.setAlignment(Qt.AlignCenter)
            self.verticalLayoutStat.addWidget(self.stdLabels)

            self.ButtonMean = QPushButton(self.verticalLayoutWidget)
            self.ButtonMean.setFont(self.font2)
            self.ButtonMean.setObjectName(u"mean")
            self.ButtonMean.setMaximumSize(QSize(170, 31))
            self.ButtonMean.setStyleSheet(u"background-color:#e3ddcf;")
            self.verticalLayoutStat.addWidget(self.ButtonMean)

            self.ButtonMode = QPushButton(self.verticalLayoutWidget)
            self.ButtonMode.setFont(self.font2)
            self.ButtonMode.setObjectName(u"mode")
            self.ButtonMode.setMaximumSize(QSize(170, 31))
            self.ButtonMode.setStyleSheet(u"background-color:#e3ddcf;")
            self.verticalLayoutStat.addWidget(self.ButtonMode)

        # set text
        self.ButtonMean.setText("Mean " + str(round(self.API_manager.get_info()['distribution_info']['mean'], 2)))
        self.ButtonMode.setText("Mode " + str(round(self.API_manager.get_info()['distribution_info']['mode'], 2)))
        self.stdLabels.setText("Std " + str(round(self.API_manager.get_info()['distribution_info']['std'], 2)))

        # connectors
        self.ButtonMean.clicked.connect(self.mode_mean_button)
        self.ButtonMode.clicked.connect(self.mode_mean_button)

    def mode_mean_button(self):
        # backend
        scan_num ,size = self.API_manager.set_size_value(self.MainWindow.sender().objectName())
        # front
        self.tableWidget.setItem(scan_num - 1, 1, QTableWidgetItem(str(round(size,2))))
        self.toolBox.setItemEnabled(2, True)

    def set_models_section(self, ids=None):
        # remove all models in section "optimized model"
        if not self.shouldReset:
            return
        if self.need:
            for k in reversed(range(self.gridLayout_1.count())):
                self.gridLayout_1.itemAt(k).widget().setParent(None)
        i = 0
        j = 0
        model_list, num = self.API_manager.init_models(ids=ids)
        total_match_models = num+len(model_list)
        for m in enumerate(model_list):
            if not self.tmp_model_list_load.__contains__(m[1].model_id):
                self.tmp_model_list_load.append(m[1].model_id)
                self.tmp_model_list_load = list(set(self.tmp_model_list_load))
        for k, model in enumerate(model_list):
            try:
                if self.tmp_model_list_load.__contains__(model):
                  pass
                frameWidget, grid = self.add_widget_model_optimized(i, j, model)
                self.set_graph_model(widget=frameWidget, layout=grid, info=model, type='Single')

                # check box connector
                check_box = grid.itemAt(0).widget()
                check_box.clicked.connect(self.buttons_clicked(model, check_box))
                # picking size connector
                pick_widget = grid.itemAt(2).widget().layout().itemAt(0).widget()
                pick_widget.valueChanged.connect(self.buttons_clicked(model, pick_widget, frameWidget, grid))
                # value of diff days between model sample day and 2nd scan day
                diffDaysBox = grid.itemAt(2).widget().layout().itemAt(1).widget()
                diffDaysBox.valueChanged.connect(self.buttons_clicked(model, diffDaysBox, frameWidget, grid))
                #relevant to multi point selection
                #choose start date from all measurements points
                # pickStartSpin = grid.itemAt(2).widget().layout().itemAt(2).widget()
                # pickStartSpin.currentIndexChanged.connect(self.buttons_clicked(model, pickStartSpin, frameWidget, grid))
                # choose end date from all measurements points
                # pickEndSpin = grid.itemAt(2).widget().layout().itemAt(3).widget()
                # pickEndSpin.currentIndexChanged.connect(self.buttons_clicked(model, pickEndSpin, frameWidget, grid))



                # for set on
                if j == 1:
                    j = 0
                    i += 1
                else:
                    j += 1
            except Exception as e:
                print(f'UI stage: {model.get_model_id()} error: {repr(e)}')
                # remove the k widget and update counter of failed models
                if k in range(self.gridLayout_1.count()):
                    self.gridLayout_1.itemAt(k).widget().setParent(None)
                num += 1
                pass

        # note with report on models
        self.label_note_set_text(f"{total_match_models-num}/{total_match_models} models were loaded successfully ")
        # for m in enumerate(self.tmp_model_list_load):
        #     if not model_list.__contains__(m[1]):
        #         self.tmp_model_list_load.remove(m[1])
        self.tmp_model_list_load.clear()
        for m in enumerate(model_list):
                self.tmp_model_list_load.append(m[1].model_id)
                self.tmp_model_list_load = list(set(self.tmp_model_list_load))

    def set_report_section(self):

        # remove all models in section "report distribution"
        for k in reversed(range(self.gridLayout_3.count())):
            self.gridLayout_3.itemAt(k).widget().setParent(None)
        i = 0
        j = 0
        try:
            for result in self.API_manager.init_results():
                frameWidget, grid = self.add_widget_model_dist(i, j, result)
                self.set_graph_model(widget=frameWidget, layout=grid, info=result, type='Dist')

                # check box connector
                check_box = grid.itemAt(0).widget()
                check_box.clicked.connect(self.buttons_clicked(result, check_box))

                if j == 1:
                    j = 0
                    i += 1
                else:
                    j += 1
        except Exception:
            # remove all models in section "report distribution"
            for k in reversed(range(self.gridLayout_3.count())):
                self.gridLayout_3.itemAt(k).widget().setParent(None)

            self.label_note_set_text('Error in loading distributions occurred')
            #raise Exception('Error in loading distributions occurred')

    def save(self):
        try:
            self.API_manager.save_local()
        except PermissionError:
            self.label_note_set_text('Some file/s in "output" folder is open')
            return
        self.label_note_set_text("Saved localy successfully")

    def upload_s3(self):
        try:
            self.API_manager.upload()
        except Exception as e:
            self.label_note_set_text('Only one model is permitted to upload')
            return
        self.label_note_set_text("Uploaded successfully")

    def add_widget_model_optimized(self, row, col, model):
        #marked code that relevant to multi point selection in the manual box item
        model_optimized = QWidget(self.scrollAreaWidgetContents_1)
        model_optimized.setObjectName(u"model_optimized")
        # model_optimized.setMinimumSize(QSize(750, 600))
        # model_optimized.setMaximumSize(QSize(750, 600))
        # model_optimized.setBaseSize(QSize(750, 600))
        model_optimized.setMinimumSize(QSize(750, 501))
        model_optimized.setMaximumSize(QSize(750, 501))
        model_optimized.setBaseSize(QSize(750, 501))
        gridLayout_112 = QGridLayout(model_optimized)
        gridLayout_112.setObjectName(u"gridLayout")
        model_checkBox = QCheckBox(model_optimized)
        model_checkBox.setObjectName(u"checkBox_up")
        model_checkBox.setFont(self.font5)
        model_checkBox.setIconSize(QSize(30, 20))
        model_checkBox.setTristate(False)
        gridLayout_112.addWidget(model_checkBox, 0, 0, 1, 1)

        GroupBox_info = QGroupBox(model_optimized)
        GroupBox_info.setObjectName(u"GroupBox_info")
        # GroupBox_info.setMinimumSize(QSize(700, 80))
        # GroupBox_info.setMaximumSize(QSize(700, 80))
        GroupBox_info.setMinimumSize(QSize(574, 72))
        GroupBox_info.setMaximumSize(QSize(574, 72))
        GroupBox_info.setFont(self.font5)
        gridLayout_1121 = QGridLayout(GroupBox_info)
        gridLayout_1121.setObjectName(u"gridLayout_1121")

        fruitType_label = QLabel(GroupBox_info)
        fruitType_label.setObjectName(u"fruitType_label")
        fruitType_label.setFont(self.font6)
        gridLayout_1121.addWidget(fruitType_label, 0, 1, 1, 1)
        fruitType_label_value = QLabel(GroupBox_info)
        fruitType_label_value.setObjectName(u"fruitType_label_value")
        gridLayout_1121.addWidget(fruitType_label_value, 1, 1, 1, 1)

        plantingYear_label = QLabel(GroupBox_info)
        plantingYear_label.setObjectName(u"plantingYear_label")
        plantingYear_label.setFont(self.font6)
        gridLayout_1121.addWidget(plantingYear_label, 0, 4, 1, 1)
        plantingYear_label_value = QLabel(GroupBox_info)
        plantingYear_label_value.setObjectName(u"plantingYear_label_value")
        gridLayout_1121.addWidget(plantingYear_label_value, 1, 4, 1, 1)

        rootstock_label = QLabel(GroupBox_info)
        rootstock_label.setObjectName(u"rootstock_label")
        rootstock_label.setFont(self.font6)
        gridLayout_1121.addWidget(rootstock_label, 0, 5, 1, 1)
        rootstock_label_value = QLabel(GroupBox_info)
        rootstock_label_value.setObjectName(u"rootstock_label_value")
        gridLayout_1121.addWidget(rootstock_label_value, 1, 5, 1, 1)

        fruitVariety_label = QLabel(GroupBox_info)
        fruitVariety_label.setObjectName(u"fruitVariety_label")
        fruitVariety_label.setFont(self.font6)
        gridLayout_1121.addWidget(fruitVariety_label, 0, 2, 1, 1)
        fruitVar_label_value = QLabel(GroupBox_info)
        fruitVar_label_value.setObjectName(u"fruitVar_label_value")
        gridLayout_1121.addWidget(fruitVar_label_value, 1, 2, 1, 1)

        soiltype_label_value = QLabel(GroupBox_info)
        soiltype_label_value.setObjectName(u"soiltype_label_value")
        gridLayout_1121.addWidget(soiltype_label_value, 1, 3, 1, 1)
        soilType_label = QLabel(GroupBox_info)
        soilType_label.setObjectName(u"soilType_label")
        soilType_label.setFont(self.font6)
        gridLayout_1121.addWidget(soilType_label, 0, 3, 1, 1)

        area_label = QLabel(GroupBox_info)
        area_label.setObjectName(u"area_label")
        area_label.setFont(self.font6)
        gridLayout_1121.addWidget(area_label, 0, 0, 1, 1)
        area_label_value = QLabel(GroupBox_info)
        area_label_value.setObjectName(u"area_label_value")
        gridLayout_1121.addWidget(area_label_value, 1, 0, 1, 1)

        crop_load_label = QLabel(GroupBox_info)
        crop_load_label.setObjectName(u"crop_load_label")
        crop_load_label.setFont(self.font6)
        gridLayout_1121.addWidget(crop_load_label, 0, 6, 1, 1)
        crop_load_label_value = QLabel(GroupBox_info)
        crop_load_label_value.setObjectName(u"crop_load_label_value")
        gridLayout_1121.addWidget(crop_load_label_value, 1, 6, 1, 1)

        #not relevant to multi points selction
        # DAFB_label = QLabel(GroupBox_info)
        # DAFB_label.setObjectName(u"DAFB_label")
        # DAFB_label.setFont(self.font6)
        # gridLayout_1121.addWidget(DAFB_label, 0, 7, 1, 1)
        # DAFB_label_value = QLabel(GroupBox_info)
        # DAFB_label_value.setObjectName(u"DAFB_label_value")
        # gridLayout_1121.addWidget(DAFB_label_value, 1, 7, 1, 1)

        gridLayout_112.addWidget(GroupBox_info, 2, 0, 1, 1)

        # margin
        gridLayout_1121.setContentsMargins(15, 5, 0, 5)

        # manual!
        # GroupBox_manual = QGroupBox(model_optimized)
        # GroupBox_manual.setObjectName(u"GroupBox_manual_2")
        # GroupBox_manual.setMinimumSize(QSize(700, 80))
        # GroupBox_manual.setMaximumSize(QSize(700, 80))
        # GroupBox_manual.setFont(self.font5)
        # formLayout_2 = QGridLayout(GroupBox_manual)
        # formLayout_2.setObjectName(u"formLayout")
        # formLayout_2.setContentsMargins(3, 2, 5, 2)
        # doubleSpinBox = QDoubleSpinBox(GroupBox_manual)
        # doubleSpinBox.setObjectName(u"doubleSpinBox")
        # doubleSpinBox.setMaximum(250)
        # doubleSpinBox.setFrame(True)
        # doubleSpinBox.setAlignment(Qt.AlignCenter)
        # formLayout_2.addWidget(doubleSpinBox, 1, 0, 1, 1)
        # spinBox = QSpinBox(GroupBox_manual)
        # spinBox.setObjectName(u"spinBox")
        # spinBox.setMinimum(-365)
        # spinBox.setMaximum(365)
        # formLayout_2.addWidget(spinBox, 1, 1, 1, 1)
        # comboBox_start = QComboBox(GroupBox_manual)
        # comboBox_start.setObjectName(u"comboBox_start")
        # comboBox_start.setFont(self.font)
        # comboBox_start.setFrame(True)
        # formLayout_2.addWidget(comboBox_start, 1, 2, 1, 1)
        # comboBox_end = QComboBox(GroupBox_manual)
        # comboBox_end.setObjectName(u"comboBox_end")
        # comboBox_end.setFont(self.font)
        # comboBox_end.setFrame(True)
        # formLayout_2.addWidget(comboBox_end, 1, 3, 1, 1)
        #
        # label_size = QLabel(GroupBox_manual)
        # label_size.setObjectName(u"label_size")
        # label_size.setFont(self.font)
        # formLayout_2.addWidget(label_size, 0, 0, 1, 1)
        #
        # label_day = QLabel(GroupBox_manual)
        # label_day.setObjectName(u"label_day")
        # label_day.setFont(self.font)
        # formLayout_2.addWidget(label_day, 0, 1, 1, 1)
        #
        # label_start_day = QLabel(GroupBox_manual)
        # label_start_day.setObjectName(u"label_start_day")
        # label_start_day.setFont(self.font)
        # formLayout_2.addWidget(label_start_day, 0, 2, 1, 1)
        #
        # label_end_day = QLabel(GroupBox_manual)
        # label_end_day.setObjectName(u"label_end_day")
        # label_end_day.setFont(self.font)
        # formLayout_2.addWidget(label_end_day, 0, 3, 1, 1)
        #
        # spinBox.setEnabled(True)
        # doubleSpinBox.setEnabled(True)
        # gridLayout_112.addWidget(GroupBox_manual, 3, 0, 1, 1)
        #end manual

        GroupBox_manual = QGroupBox(model_optimized)
        GroupBox_manual.setObjectName(u"GroupBox_manual_2")
        GroupBox_manual.setMinimumSize(QSize(152, 71))
        GroupBox_manual.setMaximumSize(QSize(152, 71))
        GroupBox_manual.setFont(self.font5)
        formLayout_2 = QFormLayout(GroupBox_manual)
        formLayout_2.setObjectName(u"formLayout")
        formLayout_2.setContentsMargins(3, 2, 5, 2)
        doubleSpinBox = QDoubleSpinBox(GroupBox_manual)
        doubleSpinBox.setObjectName(u"doubleSpinBox")
        doubleSpinBox.setMaximum(250)
        doubleSpinBox.setFrame(True)
        doubleSpinBox.setAlignment(Qt.AlignCenter)
        formLayout_2.setWidget(0, QFormLayout.FieldRole, doubleSpinBox)
        spinBox = QSpinBox(GroupBox_manual)
        spinBox.setObjectName(u"spinBox")
        spinBox.setMinimum(-365)
        spinBox.setMaximum(365)
        formLayout_2.setWidget(1, QFormLayout.FieldRole, spinBox)
        label_size = QLabel(GroupBox_manual)
        label_size.setObjectName(u"label_size")
        label_size.setFont(self.font)
        formLayout_2.setWidget(0, QFormLayout.LabelRole, label_size)
        label_day = QLabel(GroupBox_manual)
        label_day.setObjectName(u"label_day")
        label_day.setFont(self.font)
        formLayout_2.setWidget(1, QFormLayout.LabelRole, label_day)

        spinBox.setEnabled(True)
        doubleSpinBox.setEnabled(True)
        gridLayout_112.addWidget(GroupBox_manual, 2, 1, 1, 1)

        # set text of labels' caption
        GroupBox_info.setTitle(QCoreApplication.translate("Growth_Tool_main", u"Block information", None))
        rootstock_label.setText(QCoreApplication.translate("Growth_Tool_main", u"Rootstock", None))
        fruitVariety_label.setText(QCoreApplication.translate("Growth_Tool_main", u"Fruit variety", None))
        soilType_label.setText(QCoreApplication.translate("Growth_Tool_main", u"Soil type", None))
        area_label.setText(QCoreApplication.translate("Growth_Tool_main", u"Area", None))
        fruitType_label.setText(QCoreApplication.translate("Growth_Tool_main", u"Fruit type", None))
        plantingYear_label.setText(QCoreApplication.translate("Growth_Tool_main", u"Planting year", None))
        crop_load_label.setText(QCoreApplication.translate("Growth_Tool_main", u"Crop load", None))
        # DAFB_label.setText(QCoreApplication.translate("Growth_Tool_main", u"DAFB", None))
        GroupBox_manual.setTitle(QCoreApplication.translate("Growth_Tool_main", u"Manual", None))
        label_day.setText(QCoreApplication.translate("Growth_Tool_main", u"1st scan day", None))
        label_size.setText(QCoreApplication.translate("Growth_Tool_main", u"Picking size", None))
        # label_start_day.setText(QCoreApplication.translate("Growth_Tool_main", u"start day", None))
        # label_end_day.setText(QCoreApplication.translate("Growth_Tool_main", u"end day", None))

        # set text of labels' value
        model_checkBox.setText(QCoreApplication.translate("Growth_Tool_main", model.get_model_id(), None))
        fruitVar_label_value.setText(model.get_fruit_variety().replace("_", " "))
        fruitType_label_value.setText(model.get_fruit_type().replace("_", " "))
        plantingYear_label_value.setText(model.get_planting_year().replace("_", " "))
        soiltype_label_value.setText(model.get_soil_type().replace("_", " "))
        area_label_value.setText(model.get_area().replace("_", " "))
        rootstock_label_value.setText(model.get_rootstock().replace("_", " "))
        crop_load_label_value.setText(model.get_crop_load().replace("_", " "))
        # DAFB_label_value.setText(model.get_DAFB().replace("_", " "))
        size, days = model.get_optimized_model(use_case='boxes')
        doubleSpinBox.setValue(size)
        spinBox.setValue(days)
        self.gridLayout_1.addWidget(model_optimized, row, col, 1, 1)

        return model_optimized, gridLayout_112

    def add_widget_model_dist(self, row, col, result):
        model_dist = QWidget(self.scrollAreaWidgetContents_2)
        model_dist.setObjectName(u"model_dist")
        model_dist.setMinimumSize(QSize(750, 501))
        model_dist.setMaximumSize(QSize(750, 501))
        model_dist.setBaseSize(QSize(750, 501))
        gridLayout = QGridLayout(model_dist)
        gridLayout.setObjectName(u"gridLayout")

        checkBox = QCheckBox(model_dist)
        checkBox.setObjectName(u"checkBox_down")
        checkBox.setFont(self.font5)
        checkBox.setIconSize(QSize(30, 20))
        checkBox.setTristate(False)

        gridLayout.addWidget(checkBox, 0, 0, 1, 1)

        # set text of labels' value
        checkBox.setText(QCoreApplication.translate("Growth_Tool_main", result.get_model_id(), None))

        self.gridLayout_3.addWidget(model_dist, row, col, 1, 1)

        return model_dist, gridLayout

    def label_note_set_text(self, note=None):
        if note != None:
            self.label_note.setText(QCoreApplication.translate("Growth_Tool_main",
                                                               u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; "
                                                               u"font-style:italic; color:#808000;\">"
                                                               + note +
                                                               "</span></p></body></html>",
                                                               None))
        else:
            self.label_note.setText(QCoreApplication.translate("Growth_Tool_main", '', None))
        self.label_note.show()

    def buttons_clicked(self, model, box, widget=None, layout=None):
        def picking_size():
            if not self.tmp_model_list_change.__contains__(model):
                self.tmp_model_list_change.append(model)
            model.set_dynamic_variables(manual_picking_size=box.value())
            # in case the user tune the picking size manually.
            self.set_graph_model(widget, layout, model, 'Single')

        def first_scan_day():
            # set values to model
            if not self.tmp_model_list_change.__contains__(model):
                self.tmp_model_list_change.append(model)
            model.set_dynamic_variables(days=box.value(), calc_delta_size=True)
            size_picking, days = model.get_optimized_model(use_case='boxes')

            # set value of size at picking_time accordingly
            diffDaysBox = layout.itemAt(2).widget().layout().itemAt(0).widget()
            diffDaysBox.setValue(size_picking)

            self.set_graph_model(widget, layout, model, 'Single')

        def check_box():
            global ids
            if not self.tmp_model_list_change.__contains__(model):
                self.tmp_model_list_change.append(model)
            if box.isChecked():
                self.API_manager.append(model)
                self.tmp_model_list_load.append(model.get_model_id())
            elif not box.isChecked():
                self.API_manager.remove(model)
                self.tmp_model_list_load.remove(model.get_model_id())

        # TODO
        def first_scan_choice():
            pass

        # TODO
        def second_scan_choice():
            pass

        if type(box) is QSpinBox:
            return first_scan_day
        elif type(box) is QDoubleSpinBox:
            return picking_size
        elif type(box) is QCheckBox:
            return check_box

        #TODO add 2 function for choosing 2 scans for analysis

    def exitProgram(self):
        _exit(0)

    def set_graph_model(self, widget, layout, info, type):
        if type == 'Single' or type == 'Dist':
            if type == 'Single':
                analysis_point, x_model, y_model, formula, labels,x_scans,y_scans  = self.API_manager.parser_model(model=info)
                ylim = self.API_manager.get_size_scale()
                # TODO
                canvas = MplCanvas.SingleModel(analysis_point, x_model, y_model, formula, labels, ylim,x_scans,y_scans)
            elif type == 'Dist':
                canvas = MplCanvas.sizeDistribution(result=info)

            Chart = QWidget(widget)
            Chart.setObjectName(u"fitChart")
            Chart.setMinimumSize(QSize(721, 351))
            Chart.setMaximumSize(QSize(721, 351))
            Chart.setStyleSheet(u"border-color: rgb(7, 7, 7);")
            layout.addWidget(Chart, 1, 0, 1, 2)
            grid = QGridLayout(Chart)
            grid.addWidget(canvas, 0, 0)

        elif type == 'bin1':
            canvas = MplCanvas.OneBin(samples=info)
            Chart = QWidget(widget)
            Chart.setObjectName(u"fitChart")
            Chart.setMaximumSize(QSize(1300, 550))
            Chart.setStyleSheet(u"border-color: rgb(7, 7, 7);")
            grid = QGridLayout(Chart)
            grid.addWidget(canvas, 0, 0)
            layout.addWidget(Chart, 0, 1, 1, 2)


class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.view().pressed.connect(self.handleItemPressed)
        self._changed = False

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        self._changed = True

    def hidePopup(self):
        if not self._changed:
            super(CheckableComboBox, self).hidePopup()
        self._changed = False

    def itemChecked(self, index):
        item = self.model().item(index, self.modelColumn())
        return item.checkState() == Qt.Checked

    def setItemChecked(self, index, checked=True):
        item = self.model().item(index, self.modelColumn())
        if checked:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)


class GuiApp:
    def __init__(self):
        import sys
        self.app = QApplication(sys.argv)
        self.app.setStyle('Windows')
        # use AA_EnableHighDpiScaling for both high and low res app versions:
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            self.app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            self.app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        self.window = QMainWindow()
        self.ui = Ui_Growth_Tool_main()
        self.ui.setupUi(self.window)
        self.window.showMaximized()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    GuiApp()
