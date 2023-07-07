# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from gui.textEditDialog import Ui_textEditDialog
from gui.CustomQtObjects import PlainTextEdit, BinaryTextEdit
from gui.VerifyDynamicPacketDialog import Ui_VerifyDynamicPacketDialog
from numpy import binary_repr


# Remember to replace QtWidgets.#QPlainTextEdit with PlainTextEdit
# padCapturedMaskTextEdit should be a binaryTextEdit
class Ui_TestSetupDialog(object):
    
    def __init__(self, test_setup_struct, dynamic_packet, yield_struct):
        
        # Keep track of the test setup
        self.__test_setup_struct = test_setup_struct
        
        # Keep track of the dynamic packet
        self.__dynamic_packet = dynamic_packet
        
        # # Register callback for reloading dynamic packet
        # self.__test_setup_struct.register_reload_dynamic_packet_callback(self.__reload_dynamic_packet)
        
        # Keep track of yield struct
        self.__yield_struct = yield_struct
        
        # For keeping track of whether dynamic packet dialog is open
        self.__dynamic_packet_dialog_is_open = False
    
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(751, 594)
        self.testSetupLabel = QtWidgets.QLabel(Dialog)
        self.testSetupLabel.setGeometry(QtCore.QRect(30, 0, 701, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.testSetupLabel.setFont(font)
        self.testSetupLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.testSetupLabel.setObjectName("testSetupLabel")
        self.conditionsLabel = QtWidgets.QLabel(Dialog)
        self.conditionsLabel.setGeometry(QtCore.QRect(400, 90, 151, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.conditionsLabel.setFont(font)
        self.conditionsLabel.setObjectName("conditionsLabel")
        self.conditionsTextEdit = PlainTextEdit(Dialog)
        self.conditionsTextEdit.setGeometry(QtCore.QRect(480, 90, 261, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.conditionsTextEdit.setFont(font)
        self.conditionsTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.conditionsTextEdit.setCenterOnScroll(True)
        self.conditionsTextEdit.setObjectName("conditionsTextEdit")
        self.controlSettingsLabel = QtWidgets.QLabel(Dialog)
        self.controlSettingsLabel.setGeometry(QtCore.QRect(50, 50, 301, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setUnderline(True)
        self.controlSettingsLabel.setFont(font)
        self.controlSettingsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.controlSettingsLabel.setObjectName("controlSettingsLabel")
        self.testSettingsLabel = QtWidgets.QLabel(Dialog)
        self.testSettingsLabel.setGeometry(QtCore.QRect(410, 50, 311, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setUnderline(True)
        self.testSettingsLabel.setFont(font)
        self.testSettingsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.testSettingsLabel.setObjectName("testSettingsLabel")
        self.layoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.layoutWidget_3.setGeometry(QtCore.QRect(400, 120, 191, 151))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.participantNameLabel = QtWidgets.QLabel(self.layoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.participantNameLabel.setFont(font)
        self.participantNameLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.participantNameLabel.setObjectName("participantNameLabel")
        self.verticalLayout_6.addWidget(self.participantNameLabel)
        self.testTypeLabel = QtWidgets.QLabel(self.layoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.testTypeLabel.setFont(font)
        self.testTypeLabel.setObjectName("testTypeLabel")
        self.verticalLayout_6.addWidget(self.testTypeLabel)
        self.deviceIDLabel = QtWidgets.QLabel(self.layoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.deviceIDLabel.setFont(font)
        self.deviceIDLabel.setObjectName("deviceIDLabel")
        self.verticalLayout_6.addWidget(self.deviceIDLabel)
        self.testNumberLabel = QtWidgets.QLabel(self.layoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.testNumberLabel.setFont(font)
        self.testNumberLabel.setObjectName("testNumberLabel")
        self.verticalLayout_6.addWidget(self.testNumberLabel)
        self.patchLocationLabel = QtWidgets.QLabel(self.layoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.patchLocationLabel.setFont(font)
        self.patchLocationLabel.setObjectName("patchLocationLabel")
        self.verticalLayout_6.addWidget(self.patchLocationLabel)
        self.layoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.layoutWidget_4.setGeometry(QtCore.QRect(600, 120, 139, 151))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget_4)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.participantNameTextEdit = PlainTextEdit(self.layoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.participantNameTextEdit.sizePolicy().hasHeightForWidth())
        self.participantNameTextEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.participantNameTextEdit.setFont(font)
        self.participantNameTextEdit.setAcceptDrops(True)
        self.participantNameTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.participantNameTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.participantNameTextEdit.setCenterOnScroll(True)
        self.participantNameTextEdit.setObjectName("participantNameTextEdit")
        self.verticalLayout_7.addWidget(self.participantNameTextEdit)
        self.testTypeTextEdit = PlainTextEdit(self.layoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.testTypeTextEdit.sizePolicy().hasHeightForWidth())
        self.testTypeTextEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.testTypeTextEdit.setFont(font)
        self.testTypeTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.testTypeTextEdit.setCenterOnScroll(True)
        self.testTypeTextEdit.setObjectName("testTypeTextEdit")
        self.verticalLayout_7.addWidget(self.testTypeTextEdit)
        self.deviceIDTextEdit = PlainTextEdit(self.layoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deviceIDTextEdit.sizePolicy().hasHeightForWidth())
        self.deviceIDTextEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.deviceIDTextEdit.setFont(font)
        self.deviceIDTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.deviceIDTextEdit.setCenterOnScroll(True)
        self.deviceIDTextEdit.setObjectName("deviceIDTextEdit")
        self.verticalLayout_7.addWidget(self.deviceIDTextEdit)
        self.testNumberTextEdit = PlainTextEdit(self.layoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.testNumberTextEdit.sizePolicy().hasHeightForWidth())
        self.testNumberTextEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.testNumberTextEdit.setFont(font)
        self.testNumberTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.testNumberTextEdit.setCenterOnScroll(True)
        self.testNumberTextEdit.setObjectName("testNumberTextEdit")
        self.verticalLayout_7.addWidget(self.testNumberTextEdit)
        self.patchLocationTextEdit = PlainTextEdit(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.patchLocationTextEdit.setFont(font)
        self.patchLocationTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.patchLocationTextEdit.setCenterOnScroll(True)
        self.patchLocationTextEdit.setObjectName("patchLocationTextEdit")
        self.verticalLayout_7.addWidget(self.patchLocationTextEdit)
        self.layoutWidget_5 = QtWidgets.QWidget(Dialog)
        self.layoutWidget_5.setGeometry(QtCore.QRect(600, 320, 131, 61))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.layoutWidget_5)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.SubtractorValueTextEdit = PlainTextEdit(self.layoutWidget_5)
        self.SubtractorValueTextEdit.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.SubtractorValueTextEdit.setFont(font)
        self.SubtractorValueTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.SubtractorValueTextEdit.setReadOnly(True)
        self.SubtractorValueTextEdit.setObjectName("SubtractorValueTextEdit")
        self.verticalLayout_8.addWidget(self.SubtractorValueTextEdit)
        self.delayTextEdit = PlainTextEdit(self.layoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.delayTextEdit.setFont(font)
        self.delayTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.delayTextEdit.setReadOnly(True)
        self.delayTextEdit.setObjectName("delayTextEdit")
        self.verticalLayout_8.addWidget(self.delayTextEdit)
        self.layoutWidget_6 = QtWidgets.QWidget(Dialog)
        self.layoutWidget_6.setGeometry(QtCore.QRect(400, 320, 191, 61))
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.layoutWidget_6)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.subtractorValueLabel = QtWidgets.QLabel(self.layoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.subtractorValueLabel.setFont(font)
        self.subtractorValueLabel.setObjectName("subtractorValueLabel")
        self.verticalLayout_9.addWidget(self.subtractorValueLabel)
        self.delayLabel = QtWidgets.QLabel(self.layoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.delayLabel.setFont(font)
        self.delayLabel.setObjectName("delayLabel")
        self.verticalLayout_9.addWidget(self.delayLabel)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 90, 191, 291))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.capturesLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.capturesLabel.setFont(font)
        self.capturesLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.capturesLabel.setObjectName("capturesLabel")
        self.verticalLayout.addWidget(self.capturesLabel)
        self.clkFreqLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.clkFreqLabel.setFont(font)
        self.clkFreqLabel.setObjectName("clkFreqLabel")
        self.verticalLayout.addWidget(self.clkFreqLabel)
        self.timeGateLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.timeGateLabel.setFont(font)
        self.timeGateLabel.setObjectName("timeGateLabel")
        self.verticalLayout.addWidget(self.timeGateLabel)
        self.measPerPattLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.measPerPattLabel.setFont(font)
        self.measPerPattLabel.setObjectName("measPerPattLabel")
        self.verticalLayout.addWidget(self.measPerPattLabel)
        self.pattPerFrameLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pattPerFrameLabel.setFont(font)
        self.pattPerFrameLabel.setObjectName("pattPerFrameLabel")
        self.verticalLayout.addWidget(self.pattPerFrameLabel)
        self.numberOfFramesLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.numberOfFramesLabel.setFont(font)
        self.numberOfFramesLabel.setObjectName("numberOfFramesLabel")
        self.verticalLayout.addWidget(self.numberOfFramesLabel)
        self.NIRVCSELBiasLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.NIRVCSELBiasLabel.setFont(font)
        self.NIRVCSELBiasLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.NIRVCSELBiasLabel.setObjectName("NIRVCSELBiasLabel")
        self.verticalLayout.addWidget(self.NIRVCSELBiasLabel)
        self.IRVCSELBiasLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.IRVCSELBiasLabel.setFont(font)
        self.IRVCSELBiasLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.IRVCSELBiasLabel.setObjectName("IRVCSELBiasLabel")
        self.verticalLayout.addWidget(self.IRVCSELBiasLabel)
        self.subtractorOffsetLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.subtractorOffsetLabel.setFont(font)
        self.subtractorOffsetLabel.setObjectName("subtractorOffsetLabel")
        self.verticalLayout.addWidget(self.subtractorOffsetLabel)
        self.padCapturedMaskLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.padCapturedMaskLabel.setFont(font)
        self.padCapturedMaskLabel.setObjectName("padCapturedMaskLabel")
        self.verticalLayout.addWidget(self.padCapturedMaskLabel)
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(230, 90, 131, 291))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.capturesTextEdit = PlainTextEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.capturesTextEdit.setFont(font)
        self.capturesTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.capturesTextEdit.setObjectName("capturesTextEdit")
        self.verticalLayout_2.addWidget(self.capturesTextEdit)
        self.clkFreqTextEdit = PlainTextEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.clkFreqTextEdit.setFont(font)
        self.clkFreqTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.clkFreqTextEdit.setObjectName("clkFreqTextEdit")
        self.verticalLayout_2.addWidget(self.clkFreqTextEdit)
        self.timeGateTextEdit = PlainTextEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.timeGateTextEdit.setFont(font)
        self.timeGateTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.timeGateTextEdit.setObjectName("timeGateTextEdit")
        self.verticalLayout_2.addWidget(self.timeGateTextEdit)
        self.measPerPattTextEdit = PlainTextEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.measPerPattTextEdit.setFont(font)
        self.measPerPattTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.measPerPattTextEdit.setObjectName("measPerPattTextEdit")
        self.verticalLayout_2.addWidget(self.measPerPattTextEdit)
        self.pattPerFrameTextEdit = PlainTextEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pattPerFrameTextEdit.setFont(font)
        self.pattPerFrameTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.pattPerFrameTextEdit.setObjectName("pattPerFrameTextEdit")
        self.verticalLayout_2.addWidget(self.pattPerFrameTextEdit)
        self.numberOfFramesTextEdit = PlainTextEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.numberOfFramesTextEdit.setFont(font)
        self.numberOfFramesTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.numberOfFramesTextEdit.setObjectName("numberOfFramesTextEdit")
        self.verticalLayout_2.addWidget(self.numberOfFramesTextEdit)
        self.NIRVCSELBiasTextEdit = PlainTextEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NIRVCSELBiasTextEdit.setFont(font)
        self.NIRVCSELBiasTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.NIRVCSELBiasTextEdit.setObjectName("NIRVCSELBiasTextEdit")
        self.verticalLayout_2.addWidget(self.NIRVCSELBiasTextEdit)
        self.IRVCSELBiasTextEdit = PlainTextEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.IRVCSELBiasTextEdit.setFont(font)
        self.IRVCSELBiasTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.IRVCSELBiasTextEdit.setCenterOnScroll(True)
        self.IRVCSELBiasTextEdit.setObjectName("IRVCSELBiasTextEdit")
        self.verticalLayout_2.addWidget(self.IRVCSELBiasTextEdit)
        self.subtractorOffsetTextEdit = PlainTextEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.subtractorOffsetTextEdit.setFont(font)
        self.subtractorOffsetTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.subtractorOffsetTextEdit.setReadOnly(False)
        self.subtractorOffsetTextEdit.setCenterOnScroll(True)
        self.subtractorOffsetTextEdit.setObjectName("subtractorOffsetTextEdit")
        self.verticalLayout_2.addWidget(self.subtractorOffsetTextEdit)
        self.padCapturedMaskTextEdit = BinaryTextEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.padCapturedMaskTextEdit.setFont(font)
        self.padCapturedMaskTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.padCapturedMaskTextEdit.setReadOnly(False)
        self.padCapturedMaskTextEdit.setCenterOnScroll(True)
        self.padCapturedMaskTextEdit.setObjectName("padCapturedMaskTextEdit")
        self.verticalLayout_2.addWidget(self.padCapturedMaskTextEdit)
        self.layoutWidget2 = QtWidgets.QWidget(Dialog)
        self.layoutWidget2.setGeometry(QtCore.QRect(30, 390, 331, 51))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.integrationTimeLabel = QtWidgets.QLabel(self.layoutWidget2)
        self.integrationTimeLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.integrationTimeLabel.setFont(font)
        self.integrationTimeLabel.setObjectName("integrationTimeLabel")
        self.verticalLayout_4.addWidget(self.integrationTimeLabel)
        self.framesPerSecondLabel = QtWidgets.QLabel(self.layoutWidget2)
        self.framesPerSecondLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.framesPerSecondLabel.setFont(font)
        self.framesPerSecondLabel.setObjectName("framesPerSecondLabel")
        self.verticalLayout_4.addWidget(self.framesPerSecondLabel)
        self.loggingEnabledCheckBox = QtWidgets.QCheckBox(Dialog)
        self.loggingEnabledCheckBox.setGeometry(QtCore.QRect(30, 10, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.loggingEnabledCheckBox.setFont(font)
        self.loggingEnabledCheckBox.setObjectName("loggingEnabledCheckBox")
        self.derivedSettingsLabel = QtWidgets.QLabel(Dialog)
        self.derivedSettingsLabel.setGeometry(QtCore.QRect(410, 280, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setUnderline(True)
        self.derivedSettingsLabel.setFont(font)
        self.derivedSettingsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.derivedSettingsLabel.setObjectName("derivedSettingsLabel")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 450, 701, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadTestSetupButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.loadTestSetupButton.setFont(font)
        self.loadTestSetupButton.setObjectName("loadTestSetupButton")
        self.horizontalLayout.addWidget(self.loadTestSetupButton)
        self.loadDynamicPatternButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.loadDynamicPatternButton.setFont(font)
        self.loadDynamicPatternButton.setObjectName("loadDynamicPatternButton")
        self.horizontalLayout.addWidget(self.loadDynamicPatternButton)
        self.loadYieldButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.loadYieldButton.setFont(font)
        self.loadYieldButton.setObjectName("loadYieldButton")
        self.horizontalLayout.addWidget(self.loadYieldButton)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
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
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(30, 490, 701, 41))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.editTestSetupButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.editTestSetupButton.setFont(font)
        self.editTestSetupButton.setObjectName("editTestSetupButton")
        self.horizontalLayout_4.addWidget(self.editTestSetupButton)
        self.verifyDynamicPacketButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.verifyDynamicPacketButton.setFont(font)
        self.verifyDynamicPacketButton.setObjectName("verifyDynamicPacketButton")
        self.horizontalLayout_4.addWidget(self.verifyDynamicPacketButton)
        self.editYieldButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.editYieldButton.setFont(font)
        self.editYieldButton.setObjectName("editYieldButton")
        self.horizontalLayout_4.addWidget(self.editYieldButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Test Setup Configuration"))
        self.testSetupLabel.setText(_translate("Dialog", "Test Setup"))
        self.conditionsLabel.setText(_translate("Dialog", "Conditions"))
        self.controlSettingsLabel.setText(_translate("Dialog", "Control Settings"))
        self.testSettingsLabel.setText(_translate("Dialog", "Test Settings"))
        self.participantNameLabel.setText(_translate("Dialog", "Participant Name"))
        self.testTypeLabel.setText(_translate("Dialog", "Test Type"))
        self.deviceIDLabel.setText(_translate("Dialog", "Device ID"))
        self.testNumberLabel.setText(_translate("Dialog", "Test Number"))
        self.patchLocationLabel.setText(_translate("Dialog", "Patch Location"))
        self.subtractorValueLabel.setText(_translate("Dialog", "Subtractor Value"))
        self.delayLabel.setText(_translate("Dialog", "Delay (ns)"))
        self.capturesLabel.setText(_translate("Dialog", "Number of Captures"))
        self.clkFreqLabel.setText(_translate("Dialog", "Clock Frequency (MHz)"))
        self.timeGateLabel.setText(_translate("Dialog", "Time Gating Setting"))
        self.measPerPattLabel.setText(_translate("Dialog", "Measurements per Pattern"))
        self.pattPerFrameLabel.setText(_translate("Dialog", "Patterns per Frame"))
        self.numberOfFramesLabel.setText(_translate("Dialog", "Number of Frames"))
        self.NIRVCSELBiasLabel.setText(_translate("Dialog", "NIR VCSEL Bias (V)"))
        self.IRVCSELBiasLabel.setText(_translate("Dialog", "IR VCSEL Bias (V)"))
        self.subtractorOffsetLabel.setText(_translate("Dialog", "Subtractor Offset"))
        self.padCapturedMaskLabel.setText(_translate("Dialog", "Pad Captured Mask"))
        self.integrationTimeLabel.setText(_translate("Dialog", "Integration time is X ms"))
        self.framesPerSecondLabel.setText(_translate("Dialog", "X frames collected per second"))
        self.loggingEnabledCheckBox.setText(_translate("Dialog", "Logging Enabled"))
        self.derivedSettingsLabel.setText(_translate("Dialog", "Derived Settings"))
        self.loadTestSetupButton.setText(_translate("Dialog", "Load Test Setup"))
        self.loadDynamicPatternButton.setText(_translate("Dialog", "Load Dynamic Packet"))
        self.loadYieldButton.setText(_translate("Dialog", "Load Yield"))
        self.updateTestSetupButton.setText(_translate("Dialog", "Update"))
        self.editTestSetupButton.setText(_translate("Dialog", "Direct Edit Test Setup"))
        self.verifyDynamicPacketButton.setText(_translate("Dialog", "Verify Dynamic Packet"))
        self.editYieldButton.setText(_translate("Dialog", "Direct Edit Yield"))
        
        # Leave this part alone
        
        # Set measurements per pattern read only
        self.pattPerFrameTextEdit.setReadOnly(True)
        
        # Update labels
        self.__update_labels()
        

    #################################################
    # Configuration done after initialization of ui
    #################################################
    def configure(self):
        
        # Show test values
        self.__show_test_setup_values()
        
        # Connect update button
        self.updateTestSetupButton.clicked.connect(self.__update_test_setup_button_pressed)
        
        # Connect the load button
        self.loadTestSetupButton.clicked.connect(self.__load_test_setup_file)
        
        # Connect the loadDynamicPatterButton
        self.loadDynamicPatternButton.clicked.connect(self.__load_dynamic_packet)
        
        # Connect the verifyDynamicPacketButton
        self.verifyDynamicPacketButton.clicked.connect(self.__show_verify_dynamic_packet_dialog)
        
        # Connect the loadYieldButton
        self.loadYieldButton.clicked.connect(self.__load_yield_file)
        
        # Connect the editTestSetupButton
        self.editTestSetupButton.clicked.connect(self.__show_test_setup_direct_edit_window)
        
        # Connect the editYieldButton
        self.editYieldButton.clicked.connect(self.__show_yield_direct_edit_window)
        
        
    #################################################
    # "Update Test Setup" button handler
    #################################################
    def __update_test_setup_button_pressed(self):
        
        # Update test setup values
        self.__update_test_setup_values()
        
        # Check logging status
        self.__update_logging()
        
        
    #################################################
    # Update the data structure with the values in the test setup form
    #################################################
    def __update_test_setup_values(self):
        self.__test_setup_struct.logging = self.loggingEnabledCheckBox.isChecked()
        self.__test_setup_struct.number_of_captures = self.capturesTextEdit.toPlainText()
        self.__test_setup_struct.clock_frequency = float(self.clkFreqTextEdit.toPlainText()) * 1e6
        self.__test_setup_struct.measurements_per_pattern = self.measPerPattTextEdit.toPlainText()
        # self.__test_setup_struct.patterns_per_frame = self.pattPerFrameTextEdit.toPlainText()
        self.__test_setup_struct.number_of_frames = self.numberOfFramesTextEdit.toPlainText()
        self.__test_setup_struct.nir_vcsel_bias = self.NIRVCSELBiasTextEdit.toPlainText()
        self.__test_setup_struct.ir_vcsel_bias = self.IRVCSELBiasTextEdit.toPlainText()
        self.__test_setup_struct.participant_name = self.participantNameTextEdit.toPlainText()
        self.__test_setup_struct.test_type = self.testTypeTextEdit.toPlainText()
        self.__test_setup_struct.device_id = self.deviceIDTextEdit.toPlainText()
        self.__test_setup_struct.test_number = self.testNumberTextEdit.toPlainText()
        self.__test_setup_struct.patch_location = self.patchLocationTextEdit.toPlainText()
        self.__test_setup_struct.subtractor_offset = self.subtractorOffsetTextEdit.toPlainText()
        self.__test_setup_struct.conditions = self.conditionsTextEdit.toPlainText()
        self.__test_setup_struct.pad_captured_mask = int(self.padCapturedMaskTextEdit.toPlainText(), base=2)
        
        # Push to test setup structure
        # self.__test_setup_struct.time_gating_setting = self.timeGateTextEdit.toPlainText()
        
        # Refresh display with accepted values
        self.__show_test_setup_values()
        
        

    #################################################
    # Show the values from the data structure in the test setup form 
    #################################################
    def __show_test_setup_values(self):
        # Update on-screen values to current data structure values
        self.loggingEnabledCheckBox.setChecked(self.__test_setup_struct.logging)
        self.conditionsTextEdit.setPlainText(self.__test_setup_struct.conditions)
        self.capturesTextEdit.setPlainText(str(self.__test_setup_struct.number_of_captures))
        self.clkFreqTextEdit.setPlainText(str(round(self.__test_setup_struct.clock_frequency / 1e6, 2)))
        self.timeGateTextEdit.setPlainText(str(self.__test_setup_struct.time_gating_setting))
        self.measPerPattTextEdit.setPlainText(str(self.__test_setup_struct.measurements_per_pattern))
        self.pattPerFrameTextEdit.setPlainText(str(self.__test_setup_struct.patterns_per_frame))
        self.numberOfFramesTextEdit.setPlainText(str(self.__test_setup_struct.number_of_frames))
        self.NIRVCSELBiasTextEdit.setPlainText(str(self.__test_setup_struct.nir_vcsel_bias))
        self.IRVCSELBiasTextEdit.setPlainText(str(self.__test_setup_struct.ir_vcsel_bias))
        self.participantNameTextEdit.setPlainText(str(self.__test_setup_struct.participant_name))
        self.testTypeTextEdit.setPlainText(str(self.__test_setup_struct.test_type))
        self.deviceIDTextEdit.setPlainText(str(self.__test_setup_struct.device_id))
        self.testNumberTextEdit.setPlainText(str(self.__test_setup_struct.test_number))
        self.patchLocationTextEdit.setPlainText(str(self.__test_setup_struct.patch_location))
        self.SubtractorValueTextEdit.setPlainText(str(self.__test_setup_struct.subtractor_value))
        self.subtractorOffsetTextEdit.setPlainText(str(self.__test_setup_struct.subtractor_offset))
        self.delayTextEdit.setPlainText(str(self.__test_setup_struct.delay))
        self.conditionsTextEdit.setPlainText(str(self.__test_setup_struct.conditions))
        self.padCapturedMaskTextEdit.setPlainText(binary_repr(self.__test_setup_struct.pad_captured_mask, self.__test_setup_struct.number_of_chips))
        self.__update_labels()
        
        
    #################################################
    # Update logging
    #################################################
    def __update_logging(self):
        
        # Check to see if logging is enabled
        if self.loggingEnabledCheckBox.isChecked():
            
            # Check to see if logging directory is already set
            if not self.__test_setup_struct.logging_directory_set:
                
                dlg = QtWidgets.QFileDialog()
                dlg.setWindowTitle("Choose Logging Directory")
                dlg.setFileMode(QtWidgets.QFileDialog.Directory)

                # Get filename
                if dlg.exec_():
                    self.__test_setup_struct.logging_directory = dlg.selectedFiles()[0]
                else:
                        print("Logging directory not selected")
                        self.loggingEnabledCheckBox.setChecked(False)
                    
        else:
            
            # Unset logging directory
            self.__test_setup_struct.logging_directory = ""
            

    #################################################
    # Load Dynamic Packet File
    #################################################
    def __load_dynamic_packet(self):
        
        # Spawn file selection dialog box
        dlg = QtWidgets.QFileDialog()
        dlg.setWindowTitle("Select Dynamic Packet File to Load")
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        # Get filename
        if dlg.exec_():
            
            # Pass to dynamic packet
            self.__dynamic_packet.read(dlg.selectedFiles()[0])
            
            # Update patterns per frame
            self.__test_setup_struct.patterns_per_frame = self.__dynamic_packet.patterns_per_frame
            
            # Update delay settings
            clk_flip, coarse, fine, finest = self.__dynamic_packet.get_delay_line_settings()
            
            # Convert from string to int
            clk_flip = int(clk_flip, base=2)
            coarse = int(coarse, base=2)
            fine = int(fine, base=2)
            finest = int(finest, base=2)
            
            # Update time gating setting
            self.__test_setup_struct.update_time_gating_setting_from_dynamic_packet(clk_flip, coarse, fine, finest)
            
            # Update test setup
            self.__show_test_setup_values()
            
        else:
                print("Dynamic packet file not selected")
                

    #################################################
    # Reload Dynamic Packet File
    #################################################
    def __reload_dynamic_packet(self):
        print("Reloading dynamic packet")
            

    #################################################
    # Load test setup File
    #################################################
    def __load_test_setup_file(self):
            
        # Spawn file selection dialog box
        dlg = QtWidgets.QFileDialog()
        dlg.setWindowTitle("Select Test Setup File to Load")
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        # Get filename
        if dlg.exec_():
            
            # Pass to test setup
            self.__test_setup_struct.interpret_test_setup_file(dlg.selectedFiles()[0])
            
            # Update test setup
            self.__show_test_setup_values()
            
        else:
            
            print("Test setup file not selected")
            
            
    #################################################
    # Show test setup direct edit window
    #################################################
    def __show_test_setup_direct_edit_window(self):
        
        # Parameters
        window_title = "Test Setup Direct Edit"
        heading = "Test Setup Text File"
        text = str(self.__test_setup_struct)
        slot = self.__direct_edit_update_test_setup
        
        # Spawn direct edit window
        self.__spawn_direct_edit_window(window_title, heading, text, slot)
            
            
    #################################################
    # Show test setup direct edit window
    #################################################
    def __spawn_direct_edit_window(self, window_title, heading, text, slot):
        
        # Create the test setup direct edit dialog
        self.direct_edit_window = Ui_textEditDialog(window_title, heading, text)
        self.direct_edit_dialog = QtWidgets.QDialog()
        self.direct_edit_dialog.setModal(True)
        if self.__test_setup_struct.logo_found:
            self.direct_edit_dialog.setWindowIcon(QtGui.QIcon(self.__test_setup_struct.logo_path))
        self.direct_edit_window.setupUi(self.direct_edit_dialog)
        self.direct_edit_dialog.show()
        
        # Connect finished signal
        self.direct_edit_dialog.finished.connect(slot)
        
        
    #################################################
    # Direct edit test setup update slot
    #################################################
    def __direct_edit_update_test_setup(self, r):
        
        # Interpret
        self.__test_setup_struct.interpret_test_setup_string(self.direct_edit_window.text)
        
        # Update
        self.__show_test_setup_values()
        
        # Disconnect slot
        self.direct_edit_dialog.finished.disconnect()
            
            
    #################################################
    # Load Yield File
    #################################################
    def __load_yield_file(self):
        
        # Spawn file selection dialog box
        dlg = QtWidgets.QFileDialog()
        dlg.setWindowTitle("Select Yield File to Load")
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        # Get filename
        if dlg.exec_():
            
            # Pass to dynamic packet
            self.__yield_struct.interpret_yield_file(dlg.selectedFiles()[0])
            
        else:
                print("Yield file not selected")
                
                
    #################################################
    # Show yield direct edit window
    #################################################
    def __show_yield_direct_edit_window(self):
        
        # Parameters
        window_title = "Yield Direct Edit"
        heading = "Yield Text File"
        text = str(self.__yield_struct)
        slot = self.__direct_edit_update_yield
        
        # Spawn direct edit window
        self.__spawn_direct_edit_window(window_title, heading, text, slot)
        
        
    #################################################
    # Direct edit yield update slot
    #################################################
    def __direct_edit_update_yield(self, r):
        
        # Interpret
        self.__yield_struct.interpret_yield_string(self.direct_edit_window.text)
        
        # Disconnect slot
        self.direct_edit_dialog.finished.disconnect()
                
        
    #################################################
    # Update information labels showing integration time and captures per second
    #################################################
    def __update_labels(self):
        
        # Calculate integration time
        integration_time = self.__test_setup_struct.measurements_per_pattern * 1.0/(self.__test_setup_struct.clock_frequency)
        
        # Calculate frames per second
        frames_per_second = 1.0 / (integration_time * self.__test_setup_struct.patterns_per_frame )
        
        # Round integration time and convert to ms
        integration_time = round(integration_time*1000, 2)
        
        # Round captures per second
        frames_per_second = round(frames_per_second, 2)
        
        # Update labels
        self.integrationTimeLabel.setText("Integration time is " + str(integration_time) + " ms per source")
        self.framesPerSecondLabel.setText("Frame rate is " + str(frames_per_second) + " Hz")
            
            
    #################################################
    # Show verify dynamic packet dialog
    #################################################
    def __show_verify_dynamic_packet_dialog(self):
        
        if not self.__dynamic_packet_dialog_is_open:
        
            # Create the test setup direct edit dialog
            self.dynamic_packet_window = Ui_VerifyDynamicPacketDialog(self.__dynamic_packet)
            self.dynamic_packet_dialog = QtWidgets.QDialog()
            self.dynamic_packet_dialog.setModal(True)
            if self.__test_setup_struct.logo_found:
                self.dynamic_packet_dialog.setWindowIcon(QtGui.QIcon(self.__test_setup_struct.logo_path))
            self.dynamic_packet_window.setupUi(self.dynamic_packet_dialog)
            self.dynamic_packet_dialog.show()
            
            # Keep track of whether or not the window is open
            self.__dynamic_packet_dialog_is_open = True
            
            # Connect done signal
            self.dynamic_packet_dialog.finished.connect(self.__dynamic_packet_dialog_finished)
            
            
    #################################################
    # Show verify dynamic packet dialog
    #################################################
    def __dynamic_packet_dialog_finished(self):
        
        # Keep track of when window is closed
        self.__dynamic_packet_dialog_is_open = False
        
        # Disconnect signal
        self.dynamic_packet_dialog.finished.disconnect()
        
    
    
    
    #################################################
    # Tab handler
    #################################################
    def __handle_tab_key(self):
        pass
    
        


if __name__ == "__main__":
    import sys
    import TestSetup
    import EmitterPattern
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    test_setup = TestSetup.TestSetup()
    emitter_pattern = EmitterPattern.EmitterPattern()
    ui = Ui_TestSetupDialog(test_setup, emitter_pattern)
    ui.setupUi(Dialog)
    ui.configure()
    Dialog.show()
    sys.exit(app.exec_())

