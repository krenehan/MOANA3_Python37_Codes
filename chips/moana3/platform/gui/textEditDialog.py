# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 16:38:50 2023

@author: Dell-User
"""

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_textEditDialog(object):
    
    def __init__(self, window_title, heading, text):
        
        # Store
        self.__window_title = window_title
        self.__heading = heading
        self.text = text
        self.text_changed = False
    
    def setupUi(self, textEditDialog):
        textEditDialog.setObjectName("textEditDialog")
        textEditDialog.setWindowModality(QtCore.Qt.WindowModal)
        textEditDialog.resize(751, 594)
        self.headingLabel = QtWidgets.QLabel(textEditDialog)
        self.headingLabel.setGeometry(QtCore.QRect(30, 0, 701, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.headingLabel.setFont(font)
        self.headingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headingLabel.setObjectName("headingLabel")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(textEditDialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(500, 550, 231, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.updateTestSetupButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.updateTestSetupButton.setFont(font)
        self.updateTestSetupButton.setObjectName("updateTestSetupButton")
        self.horizontalLayout_2.addWidget(self.updateTestSetupButton)
        self.fileTextEdit = QtWidgets.QPlainTextEdit(textEditDialog)
        self.fileTextEdit.setGeometry(QtCore.QRect(30, 50, 701, 481))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fileTextEdit.setFont(font)
        self.fileTextEdit.setObjectName("fileTextEdit")

        self.retranslateUi(textEditDialog)
        QtCore.QMetaObject.connectSlotsByName(textEditDialog)
        
        

    def retranslateUi(self, textEditDialog):
        _translate = QtCore.QCoreApplication.translate
        textEditDialog.setWindowTitle(_translate("textEditDialog", "Dialog"))
        self.headingLabel.setText(_translate("textEditDialog", "Heading"))
        self.updateTestSetupButton.setText(_translate("textEditDialog", "Update"))
        
        # Leave this alone
        self.dialog = textEditDialog
        textEditDialog.setWindowTitle(_translate("textEditDialog", self.__window_title))
        self.headingLabel.setText(_translate("textEditDialog", self.__heading))
        self.fileTextEdit.setPlainText(self.text)
        self.updateTestSetupButton.clicked.connect(self.update_button_pressed)
        
        
    #################################################
    # Update button function
    #################################################
    def update_button_pressed(self):
        
        # Store text
        self.text = self.fileTextEdit.toPlainText()
        
        # Call done
        self.dialog.done(0)
        
        
if __name__ == "__main__":
    import sys
    
    window_title = "Title"
    heading = "Heading"
    text = "The human torch was denied a bank loan."
    
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_textEditDialog(window_title, heading, text)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())