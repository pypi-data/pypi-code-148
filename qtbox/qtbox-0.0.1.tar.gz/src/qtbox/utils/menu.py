from pathlib import Path
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ContextMenu(QMenu):
    view_code_signal = pyqtSignal()
    download_code_signal = pyqtSignal()
    res_path = Path(__file__).parent.parent / "res"

    def __init__(self):
        super(ContextMenu, self).__init__()
        self.view_code_action = QAction(QIcon(str(self.res_path / "images/view.png")), "查看代码", self)
        self.download_code_action = QAction(QIcon(str(self.res_path / "images/download.png")), "下载代码", self)

        self.set_up()

    def set_up(self):
        self.set_action()
        self.set_signal()
        self.set_style_sheet()

    def set_action(self):
        self.addAction(self.view_code_action)
        self.addAction(self.download_code_action)

    def set_signal(self):
        self.view_code_action.triggered.connect(self.view_code_signal.emit)
        self.download_code_action.triggered.connect(self.download_code_signal.emit)

    def set_style_sheet(self):
        with open(self.res_path / "qss/menu.qss") as f:
            self.setStyleSheet(f.read())

