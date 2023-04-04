# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 11:00:24 2021

@author: Dell-User
"""
# Qt imports
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import GraphicsLayoutWidget, PlotWidget, ViewBox, setConfigOptions
import test_platform

# Custom Qt imports
from gui.Reader import Reader
from gui.ReaderStruct import ReaderStruct
from gui.TestSetupDialog import Ui_TestSetupDialog
from gui.TestSetupStruct import TestSetupStruct
from gui.CustomQtObjects import PlainTextEdit
from gui.YieldStruct import YieldStruct
from DataPacket import DataPacket
from DynamicPacket import DynamicPacket

# LSL inputs
from pylsl import StreamInlet, resolve_stream

# Generic  imports
import numpy as np
import os
import datetime
from time import sleep

import threading
def logthread(caller):
    print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
                              threading.current_thread().ident))


class Ui_PlotWindow(object):
    
    #################################################
    # This comes out of Qt Designer
    #################################################
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
        self.patternPlottedTextEdit = PlainTextEdit(self.centralwidget)
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
        self.resetTimeTraceButton.setEnabled(False)
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
    
    

# Remember to replace QtWidgets.QPlainTextEdit with PlainTextEdit
class PlotWindow(QtWidgets.QMainWindow):
    
        
    # Create signals for reader
    reader_start_signal = QtCore.pyqtSignal()
    reader_trigger_signal = QtCore.pyqtSignal()
    reader_stop_signal = QtCore.pyqtSignal()
    reader_reload_parameters_signal = QtCore.pyqtSignal()
    
    # Signals for triggering logging
    logging_start_signal = QtCore.pyqtSignal()
    logging_stop_signal = QtCore.pyqtSignal()
    
    # Plot variables
    capture_number                   = 0
    plot_interval                    = 0
    log_plotting                     = False
    time_trace_plotting              = False
    plot_counter                     = 0
    target_pattern                   = 0
    frame_to_plot_counter            = 0
    time_y_index                     = 0
    
    # Emitter information for plot colors
    emitters_in_pattern              = ()
    wavelength_of_pattern            = 0
    
    # Status bit for whether or not reader has new data
    reader_sent_new_data             = False
    reader_sent_zeroeth_capture      = False
    
    # Keep track of whether or not reader has been stopped
    reader_stopped                   = True
    
    # Keep track of whether imaging is running
    imaging_running                  = False
    logging_running                  = False
    
    # Test setup window
    test_setup_window_open           = False
    
    # Settings for delay line
    clk_flip                         = False
    coarse                           = 0
    fine                             = 0
    finest                           = 0
    actual_delay                     = 0
    
    # Reset time trace
    reset_time_trace_caught          = False
    
    # Experiment directory
    experiment_directory        = None
    
    
    #################################################
    # Constructor for main window
    #################################################
    def __init__(self, bitfile_path=None, debug=False, parent=None):
        
        # Init super
        super(PlotWindow, self).__init__(parent=parent)
        
        # Set default background and foreground colors
        setConfigOptions(background='w', foreground='k')
        
        # Create ui instance
        self.ui = Ui_PlotWindow()
        
        # Setup ui
        self.ui.setupUi(self)      
        
        # Debug variable removes hardware-specific functionality
        self.debug = bool(debug)
        
        # Store the dut handle so that read function can be called
        self.dut                              = None if self.debug else test_platform.TestPlatform("moana3")
        
        # Store the bitfile path
        self.bitfile_path                     = bitfile_path
        
        # Create the test setup handle
        self.test_setup_struct                = TestSetupStruct()
        
        # Create the dynamic packet
        self.dynamic_packet                   = DynamicPacket(self.test_setup_struct.number_of_chips, self.test_setup_struct.patterns_per_frame)
        
        # Create the yield struct
        self.yield_struct                     = YieldStruct(self.test_setup_struct.number_of_chips)
        
        # Path for icon
        self.logo_path = os.path.join(os.getcwd(), os.path.abspath('../../platform/gui/logo.png'))
        self.logo_found = os.path.exists(self.logo_path)
        
        # Pass the logo to the test setup window
        self.test_setup_struct.logo_path = self.logo_path
        
        # Print thread for main window
        logthread('mainwin.__init__')
        
        
    #################################################
    # Configuration done outside of Qt Designer function
    ################################################# 
    def configure(self):
        
        # Add logo
        if self.logo_found:
            self.setWindowIcon(QtGui.QIcon(self.logo_path))
        
        # Create font and set text
        font = QtGui.QFont("Times", weight=QtGui.QFont.Bold)
        font.setPointSize(15)
        self.ui.CaptureText.setFont(font)
        
        # Make status invisible
        self.ui.statusLabel.setVisible(False)

        # Connect start/stop button
        self.ui.startStopButton.clicked.connect(self.start_imaging)
        
        # Connect start collection button
        self.ui.startDataCollectionButton.clicked.connect(self.start_data_collection)
        
        # Connect the log plotting check box
        self.ui.logPlottingCheckBox.toggled.connect(self.toggle_log_plotting)
        
        # Connect the pattern text edit
        self.ui.newPatternSubmitButton.clicked.connect(self.change_pattern_plotted)
        
        # Connect the test setup button
        self.ui.testSetupButton.clicked.connect(self.show_test_setup_window)
        
        # Connect the time trace check box
        self.ui.timeTraceCheckBox.toggled.connect(self.toggle_time_trace)
        
        # Connect the resetTimeTraceButton
        self.ui.resetTimeTraceButton.clicked.connect(self.reset_time_trace)
        
        # Create the plot timer
        self.create_plot_timer()
        
        # Create list for targeting plots
        self.plot_list = (    self.ui.plotItemChip0,  \
                              self.ui.plotItemChip1,  \
                              self.ui.plotItemChip2,  \
                              self.ui.plotItemChip3,  \
                              self.ui.plotItemChip4,  \
                              self.ui.plotItemChip5,  \
                              self.ui.plotItemChip6,  \
                              self.ui.plotItemChip7,  \
                              self.ui.plotItemChip8,  \
                              self.ui.plotItemChip9,  \
                              self.ui.plotItemChip10, \
                              self.ui.plotItemChip11, \
                              self.ui.plotItemChip12, \
                              self.ui.plotItemChip13, \
                              self.ui.plotItemChip14, \
                              self.ui.plotItemChip15, )
        
        # Update plot format
        self.set_plot_format_to_hist()
            
        # Create default plot pen
        self.plotPen = QtGui.QPen()
        self.plotPen.setColor(QtGui.QColor("blue"))
        self.plotPen.setWidth(0)
        
        # Create special plot pen for emitter
        self.nir_emitter_plot_pen = QtGui.QPen()
        self.nir_emitter_plot_pen.setColor(QtGui.QColor("darkRed"))
        self.nir_emitter_plot_pen.setWidth(0)
        
        # Create special plot pen for emitter
        self.ir_emitter_plot_pen = QtGui.QPen()
        self.ir_emitter_plot_pen.setColor(QtGui.QColor("darkMagenta"))
        self.ir_emitter_plot_pen.setWidth(0)
        
        # Initialize the hardware
        if not self.debug:
            self.configure_dut()
            self.power_up()
        
        
    #################################################
    # Update the status message
    #################################################
    def update_status_message(self, message):
        
        # Update status label
        self.ui.statusLabel.setText(message)
        
        # Make status visible
        self.ui.statusLabel.setVisible(True)
        
        
    #################################################
    # Update the button state
    #################################################
    def update_start_stop_button(self):
        
        # Change the start button to a stop button and vice versa
        if self.imaging_running:
            self.ui.startStopButton.setEnabled(False)
            self.ui.startStopButton.setText("Stop Imaging")
            self.ui.startStopButton.clicked.disconnect()
            self.ui.startStopButton.clicked.connect(self.stop_imaging)
            self.ui.startStopButton.setEnabled(True)
        else:
            self.ui.startStopButton.setEnabled(False)
            self.ui.startStopButton.setText("Start Imaging")
            self.ui.startStopButton.clicked.disconnect()
            self.ui.startStopButton.clicked.connect(self.start_imaging)
            self.ui.startStopButton.setEnabled(True)
            
            
    #################################################
    # Update the start/stop collection button state
    #################################################
    def update_start_stop_collection_button(self):
        
        # Change the start button to a stop button and vice versa
        if self.logging_running:
            self.ui.startDataCollectionButton.setEnabled(False)
            self.ui.startDataCollectionButton.setText("Stop Collection")
            self.ui.startDataCollectionButton.clicked.disconnect()
            self.ui.startDataCollectionButton.clicked.connect(self.stop_data_collection)
            self.ui.startDataCollectionButton.setEnabled(True)
        else:
            self.ui.startDataCollectionButton.setEnabled(False)
            self.ui.startDataCollectionButton.setText("Start Collection")
            self.ui.startDataCollectionButton.clicked.disconnect()
            self.ui.startDataCollectionButton.clicked.connect(self.start_data_collection)
            self.ui.startDataCollectionButton.setEnabled(True)
        
        
    #################################################
    # Update the capture label
    #################################################
    def update_capture_label(self):
        self.ui.CaptureText.setText("Capture " + str(self.capture_number))
            

    #################################################
    # Toggle time trace
    #################################################
    def toggle_time_trace(self):
        
        if self.time_trace_plotting:
            print("Changing to histogram plotting")
            self.time_trace_plotting = False
            self.set_plot_format_to_hist()
              
        else:
            print("Changing to time trace plotting")
            self.time_trace_plotting = True
            self.set_plot_format_to_time_trace()
            
            
    #################################################
    # Change the plotted pattern
    #################################################
    def change_pattern_plotted(self):
        
        # Get the new pattern
        new_pattern = int(self.ui.patternPlottedTextEdit.toPlainText())
        
        # Verify it is in the range of acceptable patterns
        if (new_pattern >= 0) and (new_pattern < self.test_setup_struct.patterns_per_frame):
            print("New pattern accepted")
            self.target_pattern = new_pattern
        else:
            print("New pattern invalid")
        
        # Update the text
        self.ui.patternPlottedTextEdit.setPlainText(str(self.target_pattern))
        
        # Refresh pattern info
        self.refresh_pattern_emitter_info()
        
    
    #################################################
    # Start data collection within reader thread
    #################################################
    def start_data_collection(self):
        
        # Update status message
        self.update_status_message("Data collection started")
        
        # Check that imaging is running
        if self.imaging_running:
            
            # Initialize logging
            if self.test_setup_struct.logging:
                self.initialize_logging()
            
            # Send signal to reader
            self.logging_start_signal.emit()
            
            # Update status bit
            self.logging_running = True
            
            # Update button
            self.update_start_stop_collection_button()
            
            # Update capture number
            self.capture_number = 0
        
    
    #################################################
    # Start data collection within reader thread
    #################################################
    def stop_data_collection(self):
        
        # Update status message
        self.update_status_message("Data collection stopped")
        
        # Send signal to reader
        self.logging_stop_signal.emit()
        
        # Update status bit
        self.logging_running = False
            
        # Update button
        self.update_start_stop_collection_button()
            
        # Update capture number
        self.capture_number = 0
            
            
    #################################################
    # Start the imaging process
    #################################################
    def start_imaging(self):
        
        # Make sure test setup window has been closed
        if self.test_setup_window_open:
            
            self.update_status_message("Finish test setup before starting")
            
        else:
            
            # Update status message
            self.update_status_message("Starting imaging")
            
            # Set capture count to 0
            self.capture_number = 0
            
            # Update the capture counter
            self.update_capture_label()
            
            # Indicate that reader has not sent data yet
            self.reader_sent_zeroeth_capture = False
            self.reader_sent_new_data = False
            
            # Refresh pattern info
            self.refresh_pattern_emitter_info()
            
            # Change the start button to a stop button
            self.imaging_running = True
            self.update_start_stop_button()
            
            # Set test setup button to be unclickable
            self.ui.testSetupButton.setEnabled(False)
            
            # Reload test settings
            self.reload_test_setup()
            
            # Configure hardware
            if not self.debug:
                
                self.reconfigure_dut()
                
                self.power_up()
                
                # Rescan
                self.scan()
                
                # Reconfigure the frame controller
                self.configure_frame_controller()
                
                # Activate dynamic mode
                self.activate_dynamic_mode()
            
            # Initialize reader
            self.initialize_reader()
            
            # Start the reader thread
            self.start_reader()
            
            # Reset the plot counter
            self.plot_counter = 0
            
            # Start plot timer
            self.start_plot_timer()
            
            # Update status message
            self.update_status_message("Waiting for first capture to complete...")
            
            
    #################################################
    # Stop the imaging process
    #################################################
    def stop_imaging(self):
        
        # Update status message
        self.update_status_message("Stopping imaging")
        
        # Update status bit
        self.imaging_running = False
        self.logging_running = False
        
        # Destroy the reader if needed
        print("reader status is " + str(self.reader_stopped))
        if not self.reader_stopped:
            print("Stop reader called from within stop imaging")
            self.stop_reader()
        
        # Stop the plot timer
        self.stop_plot_timer()
        
        # Disable stop button, enable start button
        self.update_start_stop_button()
        self.update_start_stop_collection_button()
        
        # Set test setup and scan settings buttons to be clickable
        self.ui.testSetupButton.setEnabled(True)
        
        # Update status message
        self.update_status_message("Imaging stopped")
        
        
    #################################################
    # Reload from test setup
    #################################################
    def reload_test_setup(self):

        # Create packet based on test setup information
        self.data_packet =  DataPacket( \
                                    self.test_setup_struct.number_of_chips, \
                                    self.test_setup_struct.number_of_frames, \
                                    self.test_setup_struct.patterns_per_frame, \
                                    self.test_setup_struct.measurements_per_pattern, \
                                    self.test_setup_struct.period, \
                                    compute_mean=False
                                    )
        
        # X axis for histogram plotting
        self.hist_x = range(self.data_packet.bins_per_histogram)
            
        # Data structure for plotting pattern-dependent data
        self.hist_y = np.empty(( \
                                             self.data_packet.number_of_chips, \
                                             self.data_packet.number_of_frames, \
                                             self.data_packet.patterns_per_frame, \
                                             self.data_packet.bins_per_histogram), \
                                             dtype=int)
            
        # Time axis for time trace plotting
        self.time_x = np.arange(0, self.test_setup_struct.number_of_captures * \
                                      self.test_setup_struct.number_of_frames * \
                                      self.test_setup_struct.frame_time, self.test_setup_struct.frame_time, dtype=float)
        
        # Data structure for time trace plotting
        self.time_y = np.empty(( \
                                             self.test_setup_struct.number_of_captures * self.data_packet.number_of_frames, \
                                             self.data_packet.number_of_chips, \
                                             self.data_packet.patterns_per_frame), \
                                             dtype=float)
        self.time_y.fill(np.nan)
        self.time_y_index = 0
        
        # Update pattern plotted
        if self.target_pattern >= self.test_setup_struct.patterns_per_frame:
            self.ui.patternPlottedTextEdit.setPlainText(str(self.test_setup_struct.patterns_per_frame-1))
            self.changePatternPlotted()
        
        
    #################################################
    # Reset the time trace
    #################################################
    def reset_time_trace(self):
        
        self.reset_time_trace_caught = True
        self.update_status_message("Time trace will reset at end of current capture")
            
            
    def get_time_indices(self):
        return np.where(np.isnan(np.transpose(self.time_y, axes=(1,2,0))[0][0]) == False)
            
    def time_x_plot_func(self, chip, frame, pattern):
        return self.time_x[0:self.time_y_index - self.test_setup_struct.number_of_frames + frame]
    
    def time_y_plot_func(self, chip, frame, pattern):
        return np.transpose(self.time_y[0:self.time_y_index - self.test_setup_struct.number_of_frames + frame], axes=(1,2,0))[chip][pattern]
            
    def hist_x_plot_func(self, chip, frame, pattern):
        return self.hist_x
    
    def hist_y_plot_func(self, chip, frame, pattern):
        return self.hist_y[chip][frame][pattern]
        
        
    #################################################
    # Increment the capture counter
    #################################################
    def increment_capture_number(self):
        
        # Change the capture number
        self.capture_number = self.capture_number + 1
        
        
    #################################################
    # Plot the data
    # Plotting works at the data packet level, so number_of_frames is taken from the packet, not the test setup
    #################################################  
    def plot_data(self):
            
        # Check for new data
        if self.reader_sent_new_data:
            
            # Reset
            self.reader_sent_new_data = False
            
            if self.reader_sent_zeroeth_capture is False:
                
                # Update status message
                self.update_status_message("Plotting captures...")
                
            # Unset
            self.reader_sent_zeroeth_capture = True
            
            # Reset frame to plot
            self.frame_to_plot_counter = 0
            
            # Update capture label
            self.update_capture_label()
            
            # Increment the capture counter
            self.increment_capture_number()
            
            # Update the capture_data
            self.hist_y = self.reader_data.copy()
            
        # Check if data has been sent yet before beginning plots
        if self.reader_sent_zeroeth_capture:
            
            # Print thread information on first plot
            if self.plot_counter == 0:
                
                logthread('mainwin.plot_data')
            
            # Increment plot counter
            self.plot_counter += 1
            
            # Frame to plot
            if self.frame_to_plot_counter < self.test_setup_struct.number_of_frames - 1:
                self.frame_to_plot_counter = self.frame_to_plot_counter + 1
            else:
                self.frame_to_plot_counter = 0
                print("rollover for capture " + str(self.capture_number))
            
            # Spawn subplots
            for chip in range(self.test_setup_struct.number_of_chips):
                
                # Change plotting to log scale if requested
                if self.log_plotting:
                    
                    # Set log plotting
                    self.plot_list[chip].setLogMode(y=self.log_plotting)
                
                # Downsample
                self.plot_list[chip].setDownsampling(ds=1, auto=False, mode='subsample')
                
                # # Plot the target pattern data
                if chip in self.emitters_in_pattern:
                    
                    # If NIR, plot with red color
                    if self.wavelength_of_pattern == self.dynamic_packet.nir_index:
                        self.plot_list[chip].plot(self.plot_x(chip, self.frame_to_plot_counter, self.target_pattern), \
                                                  self.plot_y(chip, self.frame_to_plot_counter, self.target_pattern), \
                                                  pen=self.nir_emitter_plot_pen, clear=True)
                    
                    # If IR, plot with purple color
                    elif self.wavelength_of_pattern == self.dynamic_packet.ir_index:
                        self.plot_list[chip].plot(self.plot_x(chip, self.frame_to_plot_counter, self.target_pattern), \
                                                  self.plot_y(chip, self.frame_to_plot_counter, self.target_pattern), \
                                                  pen=self.ir_emitter_plot_pen, clear=True)
                        
                else:
                    
                    # If detector, plot with blue color
                    self.plot_list[chip].plot(self.plot_x(chip, self.frame_to_plot_counter, self.target_pattern), \
                                              self.plot_y(chip, self.frame_to_plot_counter, self.target_pattern), \
                                              pen=self.plotPen, clear=True)
        
        # This is the case where the reader hasn't given us a capture yet
        else:
            
            # Spawn subplots
            for chip in range(self.test_setup_struct.number_of_chips):
                
                # Clear existing plot items
                self.plot_list[chip].clear()
    
    #################################################
    # Set log plotting
    #################################################
    def toggle_log_plotting(self):
        
        if self.log_plotting:
            print("Changing to linear plotting")
            self.log_plotting = False
            
        else:
            print("Changing to log plotting")
            self.log_plotting = True
        
        # Change plotting to log scale if requested
        for chip in range(self.test_setup_struct.number_of_chips):
            self.plot_list[chip].setLogMode(y=self.log_plotting)
            
    
    #################################################
    # Set plot format to histogram
    #################################################
    def set_plot_format_to_time_trace(self):
    
        # Update plot ranges
        for i in range(self.test_setup_struct.number_of_chips):
            self.plot_list[i].getViewBox().enableAutoRange(axis=ViewBox.YAxis, enable=True)
            self.plot_list[i].getViewBox().enableAutoRange(axis=ViewBox.XAxis, enable=True)
        
        # Add y-label to left side
        for i in [0, 4, 8, 12]:
            self.plot_list[i].setLabels(left="CW Counts")
            
        # Add x-label to bottom side
        for i in [12, 13, 14, 15]:
            self.plot_list[i].setLabels(bottom="Time (s)")
            
        # Pointers for x and y data for plotting
        self.plot_x = self.time_x_plot_func
        self.plot_y = self.time_y_plot_func
        
        # Enable reset button
        self.ui.resetTimeTraceButton.setEnabled(True)
            
    
    #################################################
    # Set plot format to time trace
    #################################################
    def set_plot_format_to_hist(self):
        
        # Update plot ranges
        for i in range(self.test_setup_struct.number_of_chips):
            self.plot_list[i].getViewBox().enableAutoRange(axis=ViewBox.YAxis, enable=True)
            self.plot_list[i].getViewBox().enableAutoRange(axis=ViewBox.XAxis, enable=False)
            self.plot_list[i].getViewBox().setXRange(0,150)
            self.plot_list[i].setLabels(title="Chip " + str(i+1))
        
        # Add y-label to left side
        for i in [0, 4, 8, 12]:
            self.plot_list[i].setLabels(left="Counts")
            
        # Add x-label to bottom side
        for i in [12, 13, 14, 15]:
            self.plot_list[i].setLabels(bottom="Bin Number")  
            
        # Pointers for x and y data for plotting
        self.plot_x = self.hist_x_plot_func
        self.plot_y = self.hist_y_plot_func
        
        # Disable reset button
        self.ui.resetTimeTraceButton.setEnabled(False)
            
            
    #################################################
    # Refresh information about the emitter in the pattern
    #################################################
    def refresh_pattern_emitter_info(self):
        
        # Update the emitters in the pattern
        self.emitters_in_pattern = self.dynamic_packet.emitters_for_pattern(self.target_pattern)
        
        # Update the wavelength of the pattern
        self.wavelength_of_pattern = self.dynamic_packet.wavelength_for_pattern(self.target_pattern)
        
        
    #################################################
    # Create test setup window
    #################################################
    def show_test_setup_window(self):
        
        # Update status message
        self.update_status_message("Configuring test setup")
        
        # Create the emitter pattern window
        self.test_setup_window = Ui_TestSetupDialog(self.test_setup_struct, self.dynamic_packet, self.yield_struct)
        self.test_setup_dialog = QtWidgets.QDialog()
        self.test_setup_dialog.setModal(True)
        if self.logo_found:
            self.test_setup_dialog.setWindowIcon(QtGui.QIcon(self.logo_path))
        self.test_setup_window.setupUi(self.test_setup_dialog)
        self.test_setup_window.configure()
        self.test_setup_dialog.show()
        
        # Update
        self.test_setup_window_open = True
        
        # Connect window close signal
        self.test_setup_dialog.finished.connect(self.test_setup_window_closed)
        
    
    #################################################
    # Called when test setup window is closed
    #################################################
    def test_setup_window_closed(self):
        
        # Keep track of state
        self.test_setup_window_open = False
        
        # Update status message
        self.update_status_message("Test setup configuration complete")
        
    
    #################################################
    # Create the reader structure and reader
    ################################################# 
    def initialize_reader(self):
        
        # Create the reader struct
        self.reader_struct                    = ReaderStruct()
        print("Created reader struct")
        
        # Update reader struct
        self.update_reader_struct()
        
        # Create the reader thread
        self.reader = Reader(self.dut, self.data_packet, self.reader_struct)
        print("Created reader")
        
        # Create thread
        self.reader_thread = QtCore.QThread()
        print("Created reader thread")
        
        # Move reader to thread
        self.reader.moveToThread(self.reader_thread)
        print("Moved reader to reader thread")
        
        # # Connect started signal from thread to reader, which will start reader when thread starts
        self.reader_thread.started.connect(self.reader.start) 
        
        # Connect new_data_available signal from reader to new_data_from_reader slot
        self.reader.new_data_available.connect(self.new_data_from_reader)
        
        # Connect reader_stop signal to stop slot in reader
        self.reader_stop_signal.connect(self.reader.stop)
        
        # Connect logging_start and logging_stop signal to slots in reader
        self.logging_start_signal.connect(self.reader.start_logging)
        self.logging_stop_signal.connect(self.reader.stop_logging)
        
        # Connect reload_parameters signal
        self.reader_reload_parameters_signal.connect(self.reader.reload_parameters)
        
        # Connect logging_finished signal to reader_stopped_data_collection slot
        self.reader.logging_finished.connect(self.reader_stopped_data_collection)
        
        # Connect internal_finished signal to reader_called_stop slot
        self.reader.finished.connect(self.reader_called_stop)
        
        # Connect the destroyed signal from the reader to the reader_destroyed slot
        self.reader.destroyed.connect(self.reader_destroyed)
        
        # Connect finished signal from reader thread to internal method
        self.reader_thread.finished.connect(self.reader_thread_finished) 
        
        
        
    #################################################
    # Start the reader by emitting start signal
    ################################################# 
    def start_reader(self):

        # # Start thread
        self.reader_thread.start()
        
        # Status bit
        self.reader_stopped = False
    
    
    #################################################
    # Stop the reader by emitting reader stop signal
    ################################################# 
    def stop_reader(self):
        
        print("Emitting stop signal to reader")
        
        # Stop reader
        self.reader_stop_signal.emit()
        
        
    #################################################
    # Keep track of when the reader has new data
    #################################################
    @QtCore.pyqtSlot(object)
    def new_data_from_reader(self, np_arr):
        
        print("Reader sent new data")
        
        # Store
        self.reader_data = np_arr
        
        # Sum and transpose numpy array to [frames:chips:patterns]
        np_arr = np.transpose(np.sum(np_arr, axis=3), axes=(1,0,2))
        
        # Time trace reset triggers the time vector to reset
        if self.reset_time_trace_caught:
            self.time_y_index = 0
            self.time_y.fill(np.nan)
            self.reset_time_trace_caught = False
            
        # Accumulate data in the time structure
        if self.time_y_index + self.test_setup_struct.number_of_frames < len(self.time_y):
            self.time_y[self.time_y_index: self.time_y_index + self.test_setup_struct.number_of_frames] = np_arr
            self.time_y_index = self.time_y_index + self.test_setup_struct.number_of_frames
        
        # Update
        self.reader_sent_new_data = True
        
    
    #################################################
    # Handler for when data collection is stopped by the reader
    #################################################
    @QtCore.pyqtSlot(int)
    def reader_stopped_data_collection(self, status_int):
        
        # Update status message
        self.update_status_message("Data collection stopped by reader")
        
        # Update status bit
        self.logging_running = False
            
        # Update button
        self.update_start_stop_collection_button()
            
        # Update capture number
        self.capture_number = 0
        
        
    #################################################
    # Reader calls stop internally, which triggers this function
    #################################################
    @QtCore.pyqtSlot()
    def reader_called_stop(self):
        
        print("Reader called stop")
        
        # Update status bit
        self.reader_stopped = True
        
        # Delete reader later
        self.reader.deleteLater()
        
        # Call the stop_imaging function if needed
        if self.imaging_running:
            print("stop_imaging called from within stop reader_call_stop")
            self.stop_imaging()
        
        
    #################################################
    # Function for situation where reader is destroyed
    #################################################
    @QtCore.pyqtSlot(QtCore.QObject)
    def reader_destroyed(self, obj):
        
        # Stop imaging if the reader sends finished signal to this slot
        print("Reader sent destroyed signal")
        
        # Remove pointer to reader
        self.reader = None
        
        # Quit reader thread
        self.reader_thread.quit()
        
        
    #################################################
    # If the reader thread sends the finished signal and it was not initiated by the main thread, it will stop the imaging process
    #################################################
    @QtCore.pyqtSlot()
    def reader_thread_finished(self):
        
        # Print
        print("Reader thread sent finished signal")
        
        # Schedule reader thread for deletion
        self.reader_thread.deleteLater()
        
        # Release pointer to reader thread
        self.reader_thread = None
        
        
    #################################################
    # Create the plotting timer
    #################################################
    def create_plot_timer(self):
        
        # Create a coarse timer for controlling overall plotting speed
        self.plot_timer=QtCore.QTimer()
        self.plot_timer.setTimerType(QtCore.Qt.CoarseTimer)
        
        # Create the precise timer for scheduling plot operations when overal plot timer expires
        self.do_plot_timer = QtCore.QTimer()
        self.do_plot_timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.do_plot_timer.setSingleShot(True)
        
        # Connect the timer's timeout function to the plot function
        self.plot_timer.timeout.connect(self.do_plot)
        self.do_plot_timer.timeout.connect(self.plot_data)
        
        
    #################################################
    # Start the timer that calls plot_data
    #################################################
    def do_plot(self):
        self.do_plot_timer.start(self.plot_timer.remainingTime())
    
    
    #################################################
    # Start the plotting timer
    #################################################
    def start_plot_timer(self):
        
        print("Plot timer started")
        
        # Recalculate plot interval based on number of frames and capture time
        self.plot_interval = int(self.test_setup_struct.capture_time / self.test_setup_struct.number_of_frames * 1000)
        
        # Start plot timer
        self.plot_timer.start(self.plot_interval // 2)
        
        
    #################################################
    # Stop the plotting timer
    #################################################
    def stop_plot_timer(self):
        
        print("Plot timer stopped")
        self.plot_timer.stop()
            
            
    #################################################
    # Create the logging directory
    #################################################  
    def initialize_logging(self):
                        
        # Get the date and time for logging directory creation
        date_time=str(datetime.datetime.now())
        
        # Build the log_file_name (conditions_year-month-day_hour-minute-second.csv)
        c_str = self.test_setup_struct.conditions + "_" if len(self.test_setup_struct.conditions) > 0 else ''
        print("c_str: " + c_str)
        experiment_directory_name = \
                        c_str + \
                        date_time[0:10] + "_" + \
                        date_time[11:13]+ "-" + \
                        date_time[14:16]+ "-" + \
                        date_time[17:19]
        print("exp dir name: " + experiment_directory_name)
        
        # Create directory
        self.experiment_directory = os.path.join(self.test_setup_struct.logging_directory, experiment_directory_name)
        os.mkdir(self.experiment_directory)
        
        # Check that logging directory was created
        if not os.path.exists(self.experiment_directory):
            raise Exception("Experiment directory " + self.experiment_directory + " was not created successfully")
            
        # Save test setup
        ts_file = open(os.path.join(self.experiment_directory, "test_setup.txt"), 'w')
        ts_file.write(str(self.test_setup_struct))
        ts_file.close()
        
        # Save dynamic packet
        dp_file = open(os.path.join(self.experiment_directory, "dynamic_packet.txt"), "w")
        dp_file.write(str(self.dynamic_packet))
        dp_file.close()
        
        # Save yield file
        y_file = open(os.path.join(self.experiment_directory, "yield.txt"), "w")
        y_file.write(str(self.yield_struct))
        
        # Update reader structure
        self.update_reader_struct()
            
        # Emit reload parameters to reader
        self.reader_reload_parameters_signal.emit()
            
            
    #################################################
    # Update reader structure
    #################################################  
    def update_reader_struct(self):
    
        # Set parameters in reader structure
        self.reader_struct.number_of_captures = self.test_setup_struct.number_of_captures
        self.reader_struct.debug = self.debug
        self.reader_struct.capture_time = self.test_setup_struct.capture_time
        
        # If we're logging, we need to specify a directory
        if self.test_setup_struct.logging and self.test_setup_struct.logging_directory_set:
            self.reader_struct.experiment_directory = self.experiment_directory
            self.reader_struct.logging_enabled = self.test_setup_struct.logging
        else:
            self.reader_struct.logging_enabled = False
        
        
        
        
    #################################################
    # Override closeEvent to prevent closing of MainWindow while reader thread is still alive
    ################################################# 
    def closeEvent(self, event):
        
        # If imaging process is still running, we ignore the close event
        if self.imaging_running:
            
            # Update status message
            self.update_status_message("Stop imaging before closing!")
            
            # Ignore close event
            event.ignore()
            
        else:
            
            # Shut down hardware
            if not self.debug:
                print("Disabling power supplies")
                self.dut.disable_cath_sm_supply()
                self.dut.disable_hvdd_ldo_supply()
            
                print("Closing FPGA")
                self.dut.fpga_interface.xem.Close()
            
            # Accept close event
            event.accept()
            
            
#################################################
#################################################
# HARDWARE FUNCTIONS
################################################# 
#################################################
            
            
    #################################################
    # Power up the hardware
    ################################################# 
    def power_up(self):
        
        # Power-up chip and reset
        self.update_status_message("Powering on...")
        
        # Configure level shifter
        use_clock_level_shifter = True
        clock_input_through_level_shifter = True
        clock_output_through_level_shifter = False
        
        # Configure level shifter
        if use_clock_level_shifter:
            self.dut.enable_clock_level_shifter()
            if clock_input_through_level_shifter:
                self.dut.set_clock_level_shifter_for_clock_input()
            elif clock_output_through_level_shifter:
                self.dut.set_clock_level_shifter_for_clock_output()
            else:
                self.dut.disable_clock_level_shifter()
        else:
            self.dut.disable_clock_level_shifter()
        
        # Enable supplies
        self.dut.enable_hvdd_ldo_supply()
        self.dut.enable_cath_sm_supply()
        sleep(0.1)
        self.update_status_message("Power on done!")
        
        # Issue scan reset
        self.update_status_message("Resetting hardware...")
        self.dut.pulse_signal('scan_reset')
        self.dut.pulse_signal('cell_reset')
        self.update_status_message("Reset done!")
        
        
    #################################################
    # Configure the DUT - called whenever clock frequency needs to be adjusted
    ################################################# 
    def configure_dut(self):
        
        # Print
        self.update_status_message("Configuring FPGA...")
        
        # Reconfigure the clocks on the FPGA
        self.dut.init_fpga(self.bitfile_path)
        self.dut.fpga_interface.xem.ResetFPGA()
        
        # Print
        self.update_status_message("FPGA configuration done!")
        

    #################################################
    # Reconfigure the DUT - called whenever clock frequency needs to be adjusted
    ################################################# 
    def reconfigure_dut(self):
        
        # Print
        self.update_status_message("Configuring FPGA...")
        
        # Close FPGA interface
        self.dut.fpga_interface.xem.Close()
        
        # Recreate dut
        self.dut = test_platform.TestPlatform("moana3")
        self.dut.init_fpga(self.bitfile_path, refclk_freq=self.test_setup_struct.clock_frequency)
        self.dut.fpga_interface.xem.ResetFPGA()
        
        # Print
        self.update_status_message("FPGA configuration done!")
        
    #################################################
    # Configure scan chain based on test setup
    ################################################# 
    def scan(self):
        
        # =============================================================================
        # Scan chain configuration
        # =============================================================================
        self.update_status_message("Configuring scan chains...")
        
        # Issue scan reset
        self.update_status_message("Resetting hardware...")
        self.dut.pulse_signal('scan_reset')
        self.dut.pulse_signal('cell_reset')
        self.update_status_message("Reset done!")
        
        # Create scan bits
        row         = ['chip_row_'+ str(i) for i in range(self.test_setup_struct.number_of_chips)]
        cell        = 'multicell_0'
        scan_bits = [ self.dut.chip_infrastructure.get_scan_chain(row[i]).get_scan_chain_segment(cell) for i in range(self.test_setup_struct.number_of_chips)]
        
        for chip in range(self.test_setup_struct.number_of_chips):
            
            # Configure TDC
            scan_bits[chip].TDCStartSelect        = '1'*8
            scan_bits[chip].TDCStopSelect         = '1'*8
            scan_bits[chip].TDCDisable            = '0'*8
            scan_bits[chip].TDCDCBoost            = '0'*8
            
            # Configure Pattern Counter
            scan_bits[chip].MeasPerPatt           = np.binary_repr(self.test_setup_struct.measurements_per_pattern, 24)
            scan_bits[chip].MeasCountEnable       = '1'

            scan_bits[chip].AQCDLLCoarseWord      = np.binary_repr(self.coarse, 4)
            scan_bits[chip].AQCDLLFineWord        = np.binary_repr(self.fine, 3)
            scan_bits[chip].AQCDLLFinestWord      = np.binary_repr(self.finest, 1)
            scan_bits[chip].DriverDLLWord         = np.binary_repr(0, 5)
            scan_bits[chip].ClkFlip               = np.binary_repr(self.clk_flip,1)
            scan_bits[chip].ClkBypass             = '0'
            
            # Configure pattern reset signal
            scan_bits[chip].PattResetControlledByTriggerExt       = '0' 
            scan_bits[chip].PattResetExtEnable    = '0'
                
            # Configure VCSELs
            scan_bits[chip].VCSELWave1Enable         = '0'    
            scan_bits[chip].VCSELEnableWithScan        = '0'     
            scan_bits[chip].VCSELEnableControlledByScan        = '0' 
            scan_bits[chip].VCSELWave2Enable         = '0'
            
            # Configure TxData
            scan_bits[chip].TestPattEnable        = '0'
            scan_bits[chip].TestDataIn            = np.binary_repr(4, 10)
            scan_bits[chip].TxDataExtRequestEnable = '0'
            
            # Configure subtractor
            scan_bits[chip].TimeOffsetWord        = np.binary_repr(self.test_setup_struct.subtractor_value, 10)
            scan_bits[chip].SubtractorBypass      = '0'
            
            # Dynamic operation
            scan_bits[chip].DynamicConfigEnable = '1'
            
            # Configure SPADs
            scan_bits[chip].SPADEnable            = '1'*64
        
        # Make scan bits for the fpga
        for chip in range(self.test_setup_struct.number_of_chips):
            self.dut.commit_scan_chain(row[chip])
            sleep(0.1)
            
        # Read out results
        for chip in range(self.test_setup_struct.number_of_chips):
            self.dut.update_scan_chain(row[chip], 0.1)
        # scan_bits_received = [self.dut.chip_infrastructure.get_scan_chain(row[chip]).get_scan_chain_segment(cell) for chip in range(self.test_setup_struct.number_of_chips)]
        
        # Print the scan chain configuration
        self.update_status_message("Scan chain configuration done!")
        
    
    #################################################
    # Configure frame controller based on test settings
    ################################################# 
    def configure_frame_controller(self):
        
        # Print
        self.update_status_message("Configuring frame controller...")
        
        # Specify clock for delay line
        self.dut.DelayLine.specify_clock(self.test_setup_struct.period, 0.5)
        
        # Find requested delay
        self.clk_flip, self.coarse, self.fine, self.finest, self.actual_delay = self.dut.DelayLine.get_setting(self.test_setup_struct.delay)
        self.dut.FrameController.send_frame_data( self.test_setup_struct.number_of_chips, \
                                            self.test_setup_struct.number_of_frames,   \
                                            self.test_setup_struct.patterns_per_frame,     \
                                            self.test_setup_struct.measurements_per_pattern,
                                            self.test_setup_struct.pad_captured_mask )
            
        # Print
        self.update_status_message("Frame controller configuration done!")
        
        
    #################################################
    # Configure frame controller based on test settings
    ################################################# 
    def activate_dynamic_mode(self):
        
        # Print
        self.update_status_message("Activating dynamic mode...")
        
        # Activate dynamic mode
        self.dut.activate_dynamic_mode(self.dynamic_packet)

        # Print
        self.update_status_message("Dynamic mode activated!")
        
        


if __name__ == "__main__":
    import sys
    
    # DUT and packet for initializing mainwindow
    dut = None
    debug = True

    # Run app
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = PlotWindow(dut, debug=debug)
    MainWindow.configure()
    MainWindow.show()
    # Set logo
    # self.test_setup_dialog.setWindowIcon(QtGui.QIcon("logo.png"))
    # ui = Ui_PlotWindow(dut, debug=debug)
    # ui.setupUi(MainWindow)
    # ui.configure()
    # MainWindow.show()
    sys.exit(app.exec_())

