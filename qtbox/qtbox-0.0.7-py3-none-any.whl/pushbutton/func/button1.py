from PyQt5.QtWidgets import QPushButton, QMessageBox
from qtbox.pushbutton.base import Base as QPushButton
from pathlib import Path


class FuncButton1(QPushButton):
    def __init__(self):
        super(FuncButton1, self).__init__(str(Path(__file__)))
        self.setText("点击后出现消息框")
        self.clicked.connect(self.show_message_box)

    def show_message_box(self):
        QMessageBox.information(self, "信息框", "Hi, Qt Box!")