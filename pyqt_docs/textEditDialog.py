# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Dell-User\Dropbox\MOANA\Python\MOANA3_Python37_Codes\chips\moana3\experiments\gui_development\textEditDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_textEditDialog(object):
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    textEditDialog = QtWidgets.QDialog()
    ui = Ui_textEditDialog()
    ui.setupUi(textEditDialog)
    textEditDialog.show()
    sys.exit(app.exec_())

