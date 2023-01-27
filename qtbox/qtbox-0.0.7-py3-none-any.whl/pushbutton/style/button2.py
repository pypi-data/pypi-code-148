from PyQt5.QtWidgets import QPushButton
from qtbox.pushbutton.base import Base as QPushButton
from pathlib import Path


class StyleButton2(QPushButton):
    def __init__(self):
        super(StyleButton2, self).__init__(str(Path(__file__)))
        self.setFixedSize(150, 50)
        self.setText("按钮02")
        self.setStyleSheet("""
        QPushButton {
            background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #47a7ed, stop: 1 #a967b2);
            color: white;
            font-size: 20px;
            font-weight:bold;
            border-radius: 25px;
        }
        
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #459ee0, stop: 1 #995da1);
        }
        
        QPushButton:pressed {
               background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #4093d1, stop: 1 #87538e);
        }
        """)