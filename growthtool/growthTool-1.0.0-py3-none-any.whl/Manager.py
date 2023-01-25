from PyQt5.QtCore import (QCoreApplication, QRect, QSize)
from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog
import logging
import API
from datetime import datetime


class projectsUI():

    def __init__(self, tool_part):
        self.tableWidget = QTableWidget(tool_part)
        self.tableWidget.setColumnCount(4)
        font = QFont()
        font.setStrikeOut(False)
        font.setBold(True)
        font.setPointSize(8)

        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setDisabled(False)
        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView:section{Background-color:#db8d39;}")

        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(0, -2, 200, 618))
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(125)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(125)
        self.tableWidget.horizontalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(50)

        self.retranslateUi()
        self.parser()
        self.show_projects()

    # setupUi

    def retranslateUi(self):
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Customer", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Project", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Scan#", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Project type", None));

    def parser(self):
        self.df_projects = API.Manager.get_projects()

    def show_projects(self):
        self.tableWidget.setRowCount(len(self.df_projects))
        for index, row in self.df_projects.iterrows():
            # push all content into columns
            self.tableWidget.setItem(index, 0, QTableWidgetItem(row['customer_code']))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(row['project_code']))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(str(row['project_ordinal_number'])))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(row['type']))
            self.tableWidget.setItem(index, 4, QTableWidgetItem(row['project_id']))

    def get_Qtable(self):
        return self.tableWidget

    def get_table(self):
        return self.df_projects

    def connect_project(self, func):
        self.tableWidget.cellDoubleClicked.connect(func)


class plotsUI():

    def __init__(self, tool_part, id=None):
        self.tableWidget = QTableWidget(tool_part)
        self.tableWidget.setColumnCount(17)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        font = QFont()
        font.setStrikeOut(False)
        font.setBold(True)
        font.setPointSize(8)
        __qtablewidgetitem0 = QTableWidgetItem()
        __qtablewidgetitem0.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem0)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(9, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(10, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(11, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(12, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(13, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(14, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(15, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(16, __qtablewidgetitem17)

        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(0, -2, 1525, 700))
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(125)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(135)
        self.tableWidget.horizontalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(50)
        self.tableWidget.setSortingEnabled(False)

        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView:section{Background-color:#db8d39;}")

        self.retranslateUi()
        if id is not None:
            self.set_plots(project=id)
            self.show_plots()

    def retranslateUi(self):
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Plot code", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Results", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Upload", None))
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Fruit variety", None))
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"1st scan date", None))
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"1st avg. size", None))
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog", u"1st mode size", None))
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog", u"1st pred. weight", None))
        ___qtablewidgetitem9 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Dialog", u"2nd scan date", None))
        ___qtablewidgetitem10 = self.tableWidget.horizontalHeaderItem(9)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Dialog", u"2nd avg. size", None))
        ___qtablewidgetitem11 = self.tableWidget.horizontalHeaderItem(10)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Dialog", u"2nd mode size", None))
        ___qtablewidgetitem12 = self.tableWidget.horizontalHeaderItem(11)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Dialog", u"2nd Pred. weight", None))
        ___qtablewidgetitem13 = self.tableWidget.horizontalHeaderItem(12)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Dialog", u"F", None))
        ___qtablewidgetitem14 = self.tableWidget.horizontalHeaderItem(13)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Dialog", u"Acc. weight 1st-2nd", None))
        ___qtablewidgetitem15 = self.tableWidget.horizontalHeaderItem(14)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Dialog", u"Growth rate 1st-2nd", None))
        ___qtablewidgetitem16 = self.tableWidget.horizontalHeaderItem(15)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("Dialog", u"Growth rate 1st-picking", None))
        ___qtablewidgetitem17 = self.tableWidget.horizontalHeaderItem(16)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("Dialog", u"Growth rate 2nd-picking", None))

    def get_Qtable(self):
        return self.tableWidget

    def get_blocks_id(self):
        return self.df_open_blocks['project_plot_id']

    def set_plots(self, project):
        self.project = project
        self.df_open_blocks = API.Manager.get_open_plots(project)

    def show_plots(self):
        # reset
        self.tableWidget.setRowCount(0)
        # setup
        self.tableWidget.setRowCount(len(self.df_open_blocks))
        for index, row in self.df_open_blocks.iterrows():
            # push all content into columns
            self.tableWidget.setItem(index, 0, QTableWidgetItem(row['plot_code']))
            push = QPushButton()
            self.tableWidget.setCellWidget(index, 1, push)
            push = QPushButton()
            push.setEnabled(False)
            self.tableWidget.setCellWidget(index, 2, push)
            self.tableWidget.setItem(index, 3, QTableWidgetItem(row['variety_name']))
            self.tableWidget.setItem(index, 4, QTableWidgetItem(datetime.strptime(row['scan1_date'],"%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d") if row['scan1_date'] is not None else ''))
            self.tableWidget.setItem(index, 5, QTableWidgetItem(str(row['scan1_avg_vis']) if row['scan1_avg_vis'] is not None else ''))
            self.tableWidget.setItem(index, 6, QTableWidgetItem(str(row['scan1_mod_vis']) if row['scan1_mod_vis'] is not None else ''))
            self.tableWidget.setItem(index, 7, QTableWidgetItem(str(row['scan1_W_pred']) if row['scan1_W_pred'] is not None else ''))
            self.tableWidget.setItem(index, 8, QTableWidgetItem(datetime.strptime(row['scan2_date'],"%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d") if row['scan2_date'] is not None else ''))
            self.tableWidget.setItem(index, 9, QTableWidgetItem(str(row['scan2_avg_vis']) if row['scan2_avg_vis'] is not None else ''))
            self.tableWidget.setItem(index, 10, QTableWidgetItem(str(row['scan2_mod_vis']) if row['scan2_mod_vis'] is not None else ''))
            self.tableWidget.setItem(index, 11, QTableWidgetItem(str(row['scan2_W_pred']) if row['scan2_W_pred'] is not None else ''))
            self.tableWidget.setItem(index, 12, QTableWidgetItem(str(int(row['ground_truth'])) if row['ground_truth'] is not None else ''))
            self.tableWidget.setItem(index, 13, QTableWidgetItem(str(round(row['AccuWeight1ST2ND'], 3)) if row['AccuWeight1ST2ND'] is not None else ''))
            self.tableWidget.setItem(index, 14, QTableWidgetItem(str(round(row['GrowthRate1ST2ND'], 3)) if row['GrowthRate1ST2ND'] is not None else ''))

    def get_dialog_logger(self, index, id):

        def open_dialog():
            if dialog.exec_() == QDialog.Accepted:
                pass

        dialog = LoggerDialog(id)
        dialog.ui = Ui_Dialog()
        dialog.ui.setupUi(dialog)

        # connect logger with push button
        push = self.tableWidget.cellWidget(index, 1)
        push.clicked.connect(open_dialog)

        return dialog

    def set_results(self, index, size, redFlag, result, done):

        def accept():
            status, color = API.Manager.upload_samples(result)
            push_accept.setText(status)
            push_accept.setStyleSheet(u"background-color:" + color)

        push_logger = self.tableWidget.cellWidget(index, 1)
        if redFlag:
            push_logger.setText('Failed')
            push_logger.setStyleSheet(u"background-color:#aa5555")

        else:
            push_logger.setText(str(round(size, 2)))
            push_logger.setStyleSheet(u"background-color:#55aa55")
            # add growth information once there is a size

            picking_date = API.Manager.datime_picking_date(self.df_open_blocks.loc[index, 'picking_time'], datetime.strptime(self.df_open_blocks.loc[index, 'scan1_date'],"%Y-%m-%dT%H:%M:%S.%fZ"))
            if picking_date != None:
                if self.df_open_blocks.loc[index, 'scan1_avg_vis'] != None and self.df_open_blocks.loc[index, 'scan1_date'] != None:
                    diffdays = (picking_date - datetime.strptime(self.df_open_blocks.loc[index, 'scan1_date'],"%Y-%m-%dT%H:%M:%S.%fZ").date()).days
                    rate = round((size - float(self.df_open_blocks.loc[index, 'scan1_avg_vis'])) / diffdays, 2)
                    self.tableWidget.setItem(index, 15, QTableWidgetItem(str(rate)))

                if self.df_open_blocks.loc[index, 'scan2_avg_vis'] != None and self.df_open_blocks.loc[index, 'scan2_date'] != None:
                    diffdays = (picking_date - datetime.strptime(self.df_open_blocks.loc[index, 'scan2_date'],"%Y-%m-%dT%H:%M:%S.%fZ").date()).days
                    rate = round((size - float(self.df_open_blocks.loc[index, 'scan2_avg_vis'])) / diffdays, 2)
                    self.tableWidget.setItem(index, 16, QTableWidgetItem(str(rate)))

            if done:
                push_accept = self.tableWidget.cellWidget(index, 2)
                push_accept.setEnabled(True)
                push_accept.setText('Accept')
                push_accept.setStyleSheet(u"background-color:#adcdb4")
                push_accept.clicked.connect(accept)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(600, 300)
        Dialog.setStyleSheet(u"background-color:#e3ddcf")
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Analysis", None))


class LoggerDialog(QDialog):
    def __init__(self, id, parent=None):
        super(LoggerDialog, self).__init__(parent)

        # setup the ui
        _console = QTextBrowser(self)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_handler = QPlainTextEditLogger(_console)
        log_handler.setFormatter(formatter)

        # initiate logger
        self.logger = logging.getLogger(str(id))
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(log_handler)

        # create the layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(_console)
        self.setLayout(layout)

    def getLogger(self):
        return self.logger


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super(QPlainTextEditLogger, self).__init__()

        self.widget = QPlainTextEdit(parent)
        self.widget.setMaximumSize(QSize(600, 300))
        self.widget.setMinimumSize(QSize(600, 300))
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
