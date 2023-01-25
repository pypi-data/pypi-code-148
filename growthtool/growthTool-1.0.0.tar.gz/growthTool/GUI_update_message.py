from PyQt5.QtWidgets import *
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PyQt5.QtGui import (QFont)
import API

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if Dialog.objectName():
            Dialog.setObjectName(u"confirmation message")
        Dialog.setStyleSheet(u"background-color:#e3ddcf\n""")
        Dialog.resize(281, 107)

        self.font = QFont()
        self.font.setFamily(u"Gisha")
        self.font.setPointSize(10)
        self.font.setBold(True)
        self.font.setWeight(75)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(110, 60, 161, 41))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.No|QDialogButtonBox.Yes)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 271, 41))
        self.label.setFont(self.font)

        self.retranslateUi(Dialog)
        # self.buttonBox.accepted.connect(self.update_models)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Confirmation request", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"The current model set will be updated.\nAre you sure? ", None))

    def update_models(self):
        API.Manager.update_models()

