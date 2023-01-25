# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 18:43:55 2022

@author: Maurilio
"""

from PySide6.QtWidgets import QScrollArea, QGroupBox, QSizePolicy
from PySide6.QtCore import Qt, QEvent

class verticalScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super(verticalScrollArea,self).__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.m_scrollAreaWidgetContents = QGroupBox(self)
        self.m_scrollAreaWidgetContents.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setWidget(self.m_scrollAreaWidgetContents)
        self.m_scrollAreaWidgetContents.installEventFilter(self)
        
    
    def eventFilter(self, object, event):
        if(object == self.m_scrollAreaWidgetContents and event.type() == QEvent.Resize):
            self.setMinimumWidth(self.m_scrollAreaWidgetContents.minimumSizeHint().width() + self.verticalScrollBar().width())

        return False