# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Dell-User\Dropbox\MOANA\Python\MOANA3_Python37_Codes\chips\moana3\experiments\gui_development\homeWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1269, 688)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.CaptureText = QtWidgets.QLabel(self.centralwidget)
        self.CaptureText.setGeometry(QtCore.QRect(460, 10, 341, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CaptureText.sizePolicy().hasHeightForWidth())
        self.CaptureText.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.CaptureText.setFont(font)
        self.CaptureText.setTextFormat(QtCore.Qt.PlainText)
        self.CaptureText.setScaledContents(True)
        self.CaptureText.setAlignment(QtCore.Qt.AlignCenter)
        self.CaptureText.setObjectName("CaptureText")
        self.graphicsLayoutWidget = GraphicsLayoutWidget(self.centralwidget)
        self.graphicsLayoutWidget.setGeometry(QtCore.QRect(30, 40, 1201, 591))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsLayoutWidget.sizePolicy().hasHeightForWidth())
        self.graphicsLayoutWidget.setSizePolicy(sizePolicy)
        self.graphicsLayoutWidget.setObjectName("graphicsLayoutWidget")
        self.layoutWidget = QtWidgets.QWidget(self.graphicsLayoutWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 1181, 571))
        self.layoutWidget.setObjectName("layoutWidget")
        self.allPlotsVerticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.allPlotsVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.allPlotsVerticalLayout.setObjectName("allPlotsVerticalLayout")
        self.plotRow0 = QtWidgets.QHBoxLayout()
        self.plotRow0.setObjectName("plotRow0")
        self.plotItemChip0 = PlotWidget(self.layoutWidget)
        self.plotItemChip0.setObjectName("plotItemChip0")
        self.plotRow0.addWidget(self.plotItemChip0)
        self.plotItemChip1 = PlotWidget(self.layoutWidget)
        self.plotItemChip1.setObjectName("plotItemChip1")
        self.plotRow0.addWidget(self.plotItemChip1)
        self.plotItemChip2 = PlotWidget(self.layoutWidget)
        self.plotItemChip2.setObjectName("plotItemChip2")
        self.plotRow0.addWidget(self.plotItemChip2)
        self.plotItemChip3 = PlotWidget(self.layoutWidget)
        self.plotItemChip3.setObjectName("plotItemChip3")
        self.plotRow0.addWidget(self.plotItemChip3)
        self.allPlotsVerticalLayout.addLayout(self.plotRow0)
        self.plotRow1 = QtWidgets.QHBoxLayout()
        self.plotRow1.setObjectName("plotRow1")
        self.plotItemChip4 = PlotWidget(self.layoutWidget)
        self.plotItemChip4.setObjectName("plotItemChip4")
        self.plotRow1.addWidget(self.plotItemChip4)
        self.plotItemChip5 = PlotWidget(self.layoutWidget)
        self.plotItemChip5.setObjectName("plotItemChip5")
        self.plotRow1.addWidget(self.plotItemChip5)
        self.plotItemChip6 = PlotWidget(self.layoutWidget)
        self.plotItemChip6.setObjectName("plotItemChip6")
        self.plotRow1.addWidget(self.plotItemChip6)
        self.plotItemChip7 = PlotWidget(self.layoutWidget)
        self.plotItemChip7.setObjectName("plotItemChip7")
        self.plotRow1.addWidget(self.plotItemChip7)
        self.allPlotsVerticalLayout.addLayout(self.plotRow1)
        self.plotRow2 = QtWidgets.QHBoxLayout()
        self.plotRow2.setObjectName("plotRow2")
        self.plotItemChip8 = PlotWidget(self.layoutWidget)
        self.plotItemChip8.setObjectName("plotItemChip8")
        self.plotRow2.addWidget(self.plotItemChip8)
        self.plotItemChip9 = PlotWidget(self.layoutWidget)
        self.plotItemChip9.setObjectName("plotItemChip9")
        self.plotRow2.addWidget(self.plotItemChip9)
        self.plotItemChip10 = PlotWidget(self.layoutWidget)
        self.plotItemChip10.setObjectName("plotItemChip10")
        self.plotRow2.addWidget(self.plotItemChip10)
        self.plotItemChip11 = PlotWidget(self.layoutWidget)
        self.plotItemChip11.setObjectName("plotItemChip11")
        self.plotRow2.addWidget(self.plotItemChip11)
        self.allPlotsVerticalLayout.addLayout(self.plotRow2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plotItemChip12 = PlotWidget(self.layoutWidget)
        self.plotItemChip12.setObjectName("plotItemChip12")
        self.horizontalLayout.addWidget(self.plotItemChip12)
        self.plotItemChip13 = PlotWidget(self.layoutWidget)
        self.plotItemChip13.setObjectName("plotItemChip13")
        self.horizontalLayout.addWidget(self.plotItemChip13)
        self.plotItemChip14 = PlotWidget(self.layoutWidget)
        self.plotItemChip14.setObjectName("plotItemChip14")
        self.horizontalLayout.addWidget(self.plotItemChip14)
        self.plotItemChip15 = PlotWidget(self.layoutWidget)
        self.plotItemChip15.setObjectName("plotItemChip15")
        self.horizontalLayout.addWidget(self.plotItemChip15)
        self.allPlotsVerticalLayout.addLayout(self.horizontalLayout)
        self.startStopButton = QtWidgets.QPushButton(self.centralwidget)
        self.startStopButton.setGeometry(QtCore.QRect(900, 630, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.startStopButton.setFont(font)
        self.startStopButton.setObjectName("startStopButton")
        self.patternPlottedTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.patternPlottedTextEdit.setGeometry(QtCore.QRect(180, 630, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.patternPlottedTextEdit.setFont(font)
        self.patternPlottedTextEdit.setBackgroundVisible(False)
        self.patternPlottedTextEdit.setObjectName("patternPlottedTextEdit")
        self.patternPlottedTextLabel = QtWidgets.QLabel(self.centralwidget)
        self.patternPlottedTextLabel.setGeometry(QtCore.QRect(30, 630, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.patternPlottedTextLabel.setFont(font)
        self.patternPlottedTextLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.patternPlottedTextLabel.setObjectName("patternPlottedTextLabel")
        self.newPatternSubmitButton = QtWidgets.QPushButton(self.centralwidget)
        self.newPatternSubmitButton.setGeometry(QtCore.QRect(240, 630, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.newPatternSubmitButton.setFont(font)
        self.newPatternSubmitButton.setObjectName("newPatternSubmitButton")
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(400, 630, 124, 31))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logPlottingCheckBox = QtWidgets.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.logPlottingCheckBox.setFont(font)
        self.logPlottingCheckBox.setObjectName("logPlottingCheckBox")
        self.horizontalLayout_2.addWidget(self.logPlottingCheckBox)
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(20, 10, 124, 31))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.timeTraceCheckBox = QtWidgets.QCheckBox(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.timeTraceCheckBox.setFont(font)
        self.timeTraceCheckBox.setObjectName("timeTraceCheckBox")
        self.horizontalLayout_3.addWidget(self.timeTraceCheckBox)
        self.testSetupButton = QtWidgets.QPushButton(self.centralwidget)
        self.testSetupButton.setGeometry(QtCore.QRect(730, 630, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.testSetupButton.setFont(font)
        self.testSetupButton.setObjectName("testSetupButton")
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setEnabled(True)
        self.statusLabel.setGeometry(QtCore.QRect(876, 12, 341, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.statusLabel.setFont(font)
        self.statusLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statusLabel.setObjectName("statusLabel")
        self.startDataCollectionButton = QtWidgets.QPushButton(self.centralwidget)
        self.startDataCollectionButton.setGeometry(QtCore.QRect(1070, 630, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.startDataCollectionButton.setFont(font)
        self.startDataCollectionButton.setObjectName("startDataCollectionButton")
        self.resetTimeTraceButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetTimeTraceButton.setGeometry(QtCore.QRect(150, 10, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.resetTimeTraceButton.setFont(font)
        self.resetTimeTraceButton.setObjectName("resetTimeTraceButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MOANA3 GUI"))
        self.CaptureText.setText(_translate("MainWindow", "Capture 0"))
        self.startStopButton.setText(_translate("MainWindow", "Start Imaging"))
        self.patternPlottedTextEdit.setPlainText(_translate("MainWindow", "0"))
        self.patternPlottedTextLabel.setText(_translate("MainWindow", "Pattern Plotted:"))
        self.newPatternSubmitButton.setText(_translate("MainWindow", "Update Pattern"))
        self.logPlottingCheckBox.setText(_translate("MainWindow", "Log Plotting"))
        self.timeTraceCheckBox.setText(_translate("MainWindow", "Time Trace"))
        self.testSetupButton.setText(_translate("MainWindow", "Test Setup"))
        self.statusLabel.setText(_translate("MainWindow", "Status"))
        self.startDataCollectionButton.setText(_translate("MainWindow", "Start Collection"))
        self.resetTimeTraceButton.setText(_translate("MainWindow", "Reset"))

from pyqtgraph import GraphicsLayoutWidget, PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
