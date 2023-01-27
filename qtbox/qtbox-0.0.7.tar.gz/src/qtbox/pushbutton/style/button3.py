from PyQt5.QtWidgets import QPushButton
from qtbox.pushbutton.base import Base as QPushButton
from pathlib import Path


class StyleButton3(QPushButton):
    def __init__(self):
        super(StyleButton3, self).__init__(str(Path(__file__)))
        self.setFixedSize(100, 100)
        self.setText("按钮03")
        self.setStyleSheet("""
        QPushButton {
            background-color: qlineargradient(x1:1, y1:0, x2:1, y2:1, stop:0 #454b4f, stop: 1 #1d2225);
            color: white;
            border-radius: 50px;
            font-size: 20px;
            font-weight: bold;
            border: 10px solid #f9f9f9;
        }
        
        QPushButton:hover {
            border: 10px solid white;
            background-color: qlineargradient(x1:1, y1:0, x2:1, y2:1, stop:0 #35393c, stop: 1 #101214);
        }
        
        QPushButton:pressed {
            color: black;
            border: 10px solid black;
            background-color: white;
        }
        """)