# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 14:47:19 2021

@author: Dell-User
"""

from PyQt5 import QtCore, QtWidgets

class PlainTextEdit(QtWidgets.QPlainTextEdit):
    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter, QtCore.Qt.Key_Tab):
            return
        super().keyPressEvent(event)
        
class BinaryTextEdit(QtWidgets.QPlainTextEdit):
    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_0, QtCore.Qt.Key_1):
            super().keyPressEvent(event)
        else:
            return
        