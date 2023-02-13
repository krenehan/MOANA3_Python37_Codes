# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:23:34 2023

@author: Dell-User
"""

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VerifyDynamicPacketDialog(object):
    
    #################################################
    # Constructor for dialog
    #################################################
    def __init__(self, dynamic_packet):
        
        # Store the dynamic packet
        self.__dynamic_packet = dynamic_packet
        
        # Target chip and pattern
        self.__target_chip = 0
        self.__target_pattern = 0
    
    
    def setupUi(self, VerifyDynamicPacketDialog):
        VerifyDynamicPacketDialog.setObjectName("VerifyDynamicPacketDialog")
        VerifyDynamicPacketDialog.setWindowModality(QtCore.Qt.WindowModal)
        VerifyDynamicPacketDialog.resize(535, 499)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VerifyDynamicPacketDialog.sizePolicy().hasHeightForWidth())
        VerifyDynamicPacketDialog.setSizePolicy(sizePolicy)
        self.headingLabel = QtWidgets.QLabel(VerifyDynamicPacketDialog)
        self.headingLabel.setGeometry(QtCore.QRect(20, 0, 491, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.headingLabel.setFont(font)
        self.headingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headingLabel.setObjectName("headingLabel")
        self.dynamicPacketTextEdit = QtWidgets.QPlainTextEdit(VerifyDynamicPacketDialog)
        self.dynamicPacketTextEdit.setGeometry(QtCore.QRect(20, 130, 491, 341))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dynamicPacketTextEdit.setFont(font)
        self.dynamicPacketTextEdit.setReadOnly(True)
        self.dynamicPacketTextEdit.setObjectName("dynamicPacketTextEdit")
        self.verticalLayoutWidget = QtWidgets.QWidget(VerifyDynamicPacketDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 50, 491, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.patternHorizontalLayout = QtWidgets.QHBoxLayout()
        self.patternHorizontalLayout.setObjectName("patternHorizontalLayout")
        self.patternLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.patternLabel.sizePolicy().hasHeightForWidth())
        self.patternLabel.setSizePolicy(sizePolicy)
        self.patternLabel.setMaximumSize(QtCore.QSize(125, 125))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.patternLabel.setFont(font)
        self.patternLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.patternLabel.setObjectName("patternLabel")
        self.patternHorizontalLayout.addWidget(self.patternLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.patternHorizontalLayout.addItem(spacerItem)
        self.patternSlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.patternSlider.sizePolicy().hasHeightForWidth())
        self.patternSlider.setSizePolicy(sizePolicy)
        self.patternSlider.setMaximum(1)
        self.patternSlider.setOrientation(QtCore.Qt.Horizontal)
        self.patternSlider.setObjectName("patternSlider")
        self.patternHorizontalLayout.addWidget(self.patternSlider)
        self.verticalLayout.addLayout(self.patternHorizontalLayout)
        self.chipHorizontalLayout = QtWidgets.QHBoxLayout()
        self.chipHorizontalLayout.setObjectName("chipHorizontalLayout")
        self.chipLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chipLabel.sizePolicy().hasHeightForWidth())
        self.chipLabel.setSizePolicy(sizePolicy)
        self.chipLabel.setMaximumSize(QtCore.QSize(125, 125))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.chipLabel.setFont(font)
        self.chipLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.chipLabel.setObjectName("chipLabel")
        self.chipHorizontalLayout.addWidget(self.chipLabel)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.chipHorizontalLayout.addItem(spacerItem1)
        self.chipSlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chipSlider.sizePolicy().hasHeightForWidth())
        self.chipSlider.setSizePolicy(sizePolicy)
        self.chipSlider.setMinimumSize(QtCore.QSize(110, 0))
        self.chipSlider.setMaximumSize(QtCore.QSize(16777215, 125))
        self.chipSlider.setMaximum(1)
        self.chipSlider.setOrientation(QtCore.Qt.Horizontal)
        self.chipSlider.setObjectName("chipSlider")
        self.chipHorizontalLayout.addWidget(self.chipSlider)
        self.verticalLayout.addLayout(self.chipHorizontalLayout)

        self.retranslateUi(VerifyDynamicPacketDialog)
        QtCore.QMetaObject.connectSlotsByName(VerifyDynamicPacketDialog)

    def retranslateUi(self, VerifyDynamicPacketDialog):
        _translate = QtCore.QCoreApplication.translate
        VerifyDynamicPacketDialog.setWindowTitle(_translate("VerifyDynamicPacketDialog", "Dynamic Packet Verification"))
        self.headingLabel.setText(_translate("VerifyDynamicPacketDialog", "Dynamic Packet"))
        self.patternLabel.setText(_translate("VerifyDynamicPacketDialog", "Pattern #"))
        self.chipLabel.setText(_translate("VerifyDynamicPacketDialog", "Chip #"))
        
        
        # Leave this part alone
        
        # Reset maximum values for sliders
        self.patternSlider.setMaximum(self.__dynamic_packet.patterns_per_frame - 1)
        self.chipSlider.setMaximum(self.__dynamic_packet.number_of_chips - 1)
        
        # Connect slide events to update functions
        self.patternSlider.valueChanged.connect(self.__update_target_pattern)
        self.chipSlider.valueChanged.connect(self.__update_target_chip)
        
        # Update text
        self.__update_text()
            
        
    #################################################
    # Update target pattern
    #################################################
    def __update_target_pattern(self, p):
        
        # Store new chip value
        self.__target_pattern = p
        
        # Update text
        self.__update_text()
            
        
    #################################################
    # Update target chip
    #################################################
    def __update_target_chip(self, c):
        
        # Store new chip value
        self.__target_chip = c
        
        # Update text
        self.__update_text()
        
    
    #################################################
    # Update the text that is displayed
    #################################################
    def __update_text(self):
        
        self.patternLabel.setText("Pattern " + str(self.__target_pattern))
        self.chipLabel.setText("Chip " + str(self.__target_chip))
        
        # Update text with results of show
        self.dynamicPacketTextEdit.setPlainText(    self.__dynamic_packet.write( \
                                                        chip_list=(self.__target_chip,), \
                                                        pattern_list=(self.__target_pattern,) \
                                                    ) \
                                                )
