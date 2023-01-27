from PyQt5.QtWidgets import QPushButton
from qtbox.pushbutton.base import Base as QPushButton
from pathlib import Path


class StyleButton1(QPushButton):
    def __init__(self):
        super(StyleButton1, self).__init__(str(Path(__file__)))
        self.setFixedSize(150, 50)
        self.setText("按钮01")
        self.setStyleSheet("""
        QPushButton {
            background-color: qlineargradient(x1:1, y1:0, x2:1, y2:0.3, stop:0 #8a9195, stop:1 black);
            color: white;
            font-size: 20px;
            font-weight:bold;
            border-radius: 25px;
        }

        QPushButton:hover {
            background-color: qlineargradient(x1:1, y1:0, x2:1, y2:0.3, stop:0 #7d8488, stop:1 black);
        }

        QPushButton:pressed {
            background-color: qlineargradient(x1:1, y1:0, x2:1, y2:0.3, stop:0 #6a7073, stop:1 black);
        }
        """)