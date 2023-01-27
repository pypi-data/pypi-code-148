from qtbox.utils.menu import ContextMenu
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Base(QPushButton):
    view_code_signal = pyqtSignal(str)
    download_code_signal = pyqtSignal(str)

    def __init__(self, code_file_path):
        super(Base, self).__init__()
        self.code_file_path = code_file_path
        self.context_menu = ContextMenu()

    def contextMenuEvent(self, event):
        self.context_menu.view_code_signal.connect(lambda: self.view_code_signal.emit(self.code_file_path))
        self.context_menu.download_code_signal.connect(lambda: self.download_code_signal.emit(self.code_file_path))
        self.context_menu.exec(event.globalPos())

