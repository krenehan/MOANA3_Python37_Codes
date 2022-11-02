# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 11:00:24 2021

@author: Dell-User
"""
# Qt imports
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import GraphicsLayoutWidget, PlotWidget, ViewBox, setConfigOptions

# Custom Qt imports
from gui.ScanWindowDialog import Ui_ScanWindowDialog
from gui.Reader import Reader
from gui.ReaderStruct import ReaderStruct
from gui.TestSetupDialog import Ui_TestSetupDialog
from gui.TestSetup import TestSetup
from gui.EmitterPatternStruct import EmitterPatternStruct
from gui.CustomQtObjects import PlainTextEdit
from DataPacket import DataPacket

# Generic  imports
import numpy as np
from copy import copy
import os
import datetime
from time import sleep




class Ui_PlotWindow(object):
    
    
    #################################################
    # Constructor for main window
    #################################################
    def __init__(self, dut, bitfile_path, debug=False):
        
        # Store the dut handle so that read function can be called
        self.__dut                              = dut
        
        # Store the bitfile path
        self.__bitfile_path                     = bitfile_path
        
        # Create the emitter pattern handle
        self.__emitter_pattern                  = EmitterPatternStruct()
        
        # Create the test setup handle
        self.__test_setup                       = TestSetup()
        
        # Create the threadpool
        self.__threadpool                       = QtCore.QThreadPool()
        
        # Debug variable removes hardware-specific functionality
        self.__debug = bool(debug)
        
        # Set default background and foreground colors
        setConfigOptions(background='w', foreground='k')
        
        # Capture parameters
        self.capture_counter                    = 0
        
        # Path for icon
        self.__logo_path = os.path.join(os.getcwd(), os.path.abspath('../../platform/gui/logo.png'))
        self.__logo_found = os.path.exists(self.__logo_path)
        
        # Pass the logo to the test setup window
        self.__test_setup.logo_path = self.__logo_path
        
        # Plotting params
        self.fps                                = 15
        self.plotInterval                       = 0#int(1/self.fps * 1000)
        self.log_plotting                       = False
        self.auto_scaling                       = True
        self.plot_counter                       = 0
        self.__target_pattern                    = 0
        

            
    
    #################################################
    # This comes out of Qt Designer
    #################################################
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1269, 690)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.CaptureText = QtWidgets.QLabel(self.centralwidget)
        self.CaptureText.setGeometry(QtCore.QRect(30, 10, 1201, 31))
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
        self.startStopButton.setGeometry(QtCore.QRect(1070, 630, 161, 31))
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
        self.layoutWidget1.setGeometry(QtCore.QRect(700, 630, 341, 29))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.testSetupButton = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.testSetupButton.setFont(font)
        self.testSetupButton.setObjectName("testSetupButton")
        self.horizontalLayout_3.addWidget(self.testSetupButton)
        self.scanSettingsButton = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.scanSettingsButton.setFont(font)
        self.scanSettingsButton.setObjectName("scanSettingsButton")
        self.horizontalLayout_3.addWidget(self.scanSettingsButton)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(400, 630, 271, 31))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logPlottingCheckBox = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.logPlottingCheckBox.setFont(font)
        self.logPlottingCheckBox.setObjectName("logPlottingCheckBox")
        self.horizontalLayout_2.addWidget(self.logPlottingCheckBox)
        self.autoScaleCheckBox = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.autoScaleCheckBox.setFont(font)
        self.autoScaleCheckBox.setObjectName("autoScaleCheckBox")
        self.horizontalLayout_2.addWidget(self.autoScaleCheckBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MOANA GUI"))
        self.CaptureText.setText(_translate("MainWindow", "Capture 0"))
        self.startStopButton.setText(_translate("MainWindow", "Start Imaging"))
        self.patternPlottedTextEdit.setPlainText(_translate("MainWindow", "0"))
        self.patternPlottedTextLabel.setText(_translate("MainWindow", "Pattern Plotted:"))
        self.newPatternSubmitButton.setText(_translate("MainWindow", "Update Pattern"))
        self.testSetupButton.setText(_translate("MainWindow", "Test Setup"))
        self.scanSettingsButton.setText(_translate("MainWindow", "Scan Settings"))
        self.logPlottingCheckBox.setText(_translate("MainWindow", "Log Plotting"))
        self.autoScaleCheckBox.setText(_translate("MainWindow", "Auto-scale"))
        
        
        # Leave this line
        self.MainWindow = MainWindow
        
        
    #################################################
    # Configure the DUT - This is only called once when the FPGA is turned on
    ################################################# 
    def __configure_dut(self):
        
        # Program the FPGA
        self.__dut.init_fpga(self.__bitfile_path)
        dut.fpga_interface.xem.ResetFPGA()
        
        
    #################################################
    # Reconfigure the DUT - called whenever clock frequency needs to be adjusted
    ################################################# 
    def __reconfigure_dut(self):
        
        # Reconfigure the clocks on the FPGA
        self.__dut.init_fpga(self.__bitfile_path)
        dut.fpga_interface.xem.ResetFPGA()
  
        
    #################################################
    # Power up the hardware
    ################################################# 
    def __power_up(self):
        
        # Power-up chip and reset
        print("Powering on...")
        
        # Configure level shifter
        use_clock_level_shifter = True
        clock_input_through_level_shifter = True
        clock_output_through_level_shifter = False
        
        # Configure level shifter
        if use_clock_level_shifter:
            self.__dut.enable_clock_level_shifter()
            if clock_input_through_level_shifter:
                self.__dut.set_clock_level_shifter_for_clock_input()
            elif clock_output_through_level_shifter:
                self.__dut.set_clock_level_shifter_for_clock_output()
            else:
                self.__dut.disable_clock_level_shifter()
        else:
            self.__dut.disable_clock_level_shifter()
    
        # Enable power level shifter
        self.__dut.enable_power_level_shifter()
        
        # Enable supplies
        self.__dut.enable_hvdd_ldo_supply()
        self.__dut.enable_cath_sm_supply()
        sleep(0.1)
        print("Power on done!")
        
        # Issue scan reset
        print("Resetting hardware...")
        self.__dut.pulse_signal('scan_reset')
        self.__dut.pulse_signal('cell_reset')
        print("Reset done!")
        
        
    #################################################
    # Configure scan chain based on test setup
    ################################################# 
    def __scan(self):
        
        # =============================================================================
        # Scan chain configuration
        # =============================================================================
        print("Configuring scan chains...")
        
        # Issue scan reset
        print("Resetting hardware...")
        self.__dut.pulse_signal('scan_reset')
        self.__dut.pulse_signal('cell_reset')
        print("Reset done!")
        
        # Create scan bits
        row         = ['chip_row_'+ str(i) for i in range(self.__test_setup.number_of_chips)]
        cell        = 'multicell_0'
        scan_bits = [ self.__dut.chip_infrastructure.get_scan_chain(row[i]).get_scan_chain_segment(cell) for i in range(self.__test_setup.number_of_chips)]
        
        for chip in range(self.__test_setup.number_of_chips):
            
            # Configure TDC
            scan_bits[chip].TDCStartSelect            = '1'*8
            scan_bits[chip].TDCStopSelect             = '1'*8
            scan_bits[chip].TDCDisable                = '0'*8
            scan_bits[chip].TDCDCBoost                = '0'
            
            # Configure Pattern Counter
            scan_bits[chip].MeasPerPatt               = np.binary_repr(self.__test_setup.measurements_per_pattern, 15)
            scan_bits[chip].MeasCountEnable           = '1'
            
            # Configure Delay Lines
            scan_bits[chip].AQCDLLCoarseWord          = np.binary_repr(self.__coarse, 4)
            scan_bits[chip].AQCDLLFineWord            = np.binary_repr(self.__fine, 3)
            scan_bits[chip].DriverDLLWord             = np.binary_repr(1 << self.__test_setup.vcsel_setting, 4)
            scan_bits[chip].ClkFlip                   = '1'
            scan_bits[chip].ClkBypass                 = np.binary_repr(self.__bypass, 1)
            
            # Configure pattern reset signal
            scan_bits[chip].PattResetExtSel           = '0'
            scan_bits[chip].PattResetExtEnable        = '0'
            
            # Configure VCSEL drivers
            scan_bits[chip].VCSELEnableExt            = '0'
            scan_bits[chip].VCSELEnableSel            = '0'
            scan_bits[chip].VCSELWave1Sel             = '1' if not self.__emitter_pattern.ir_emitters[chip] else '0' #NIR
            scan_bits[chip].VCSELWave2Sel             = '1' if self.__emitter_pattern.ir_emitters[chip] else '0' #IR
            
            # Configure TxData
            scan_bits[chip].TestPattEnable            = '0'
            scan_bits[chip].TestDataIn                = np.binary_repr(20, 10)
            scan_bits[chip].TxDataExtRequestEnable    = '0'
            
            # Configure subtractor
            scan_bits[chip].TimeOffsetWord            = np.binary_repr((self.__test_setup.subtractor_value & 0x3F8) >> 3, 7)
            scan_bits[chip].TimeOffsetWordLSBs        = np.binary_repr(self.__test_setup.subtractor_value & 0x7, 3)*8
            scan_bits[chip].SubtractorBypass          = '0'
            
            # Configure SPADs
            scan_bits[chip].SPADEnable                = '1'*64
        
        # Make scan bits for the fpga
        for chip in range(self.__test_setup.number_of_chips):
            self.__dut.commit_scan_chain(row[chip])
            sleep(0.1)
            
        # Read out results
        for chip in range(self.__test_setup.number_of_chips):
            self.__dut.update_scan_chain(row[chip], 0.1)
        scan_bits_received = [self.__dut.chip_infrastructure.get_scan_chain(row[chip]).get_scan_chain_segment(cell) for chip in range(self.__test_setup.number_of_chips)]
        
        # Print the scan chain configuration
        print("Scan chain configuration done!")
        
    
    #################################################
    # Configure frame controller based on test settings
    ################################################# 
    def __configure_frame_controller(self):
        
        dut.DelayLine.specify_clock(self.__test_setup.period,0.5) 
        self.__clk_flip, self.__bypass, self.__coarse, self.__fine = self.__dut.DelayLine.get_setting(self.__test_setup.delay)
        
        print("Configuring frame controller...")
        self.__dut.FrameController.send_frame_data( self.__test_setup.number_of_chips, \
                                            self.__test_setup.number_of_frames, \
                                            self.__test_setup.patterns_per_frame, \
                                            self.__test_setup.measurements_per_pattern )
        self.__dut.check_emitter_pattern()
        print("Frame controller configuration done!")
        
    
    #################################################
    # Begin streaming
    ################################################# 
    def __begin_stream(self):
        
        # Final reset
        print("Initializing operation")
        self.__dut.pulse_signal('cell_reset')
        self.__dut.reset_fifos()
        sleep(0.1)
        
        # Clear any existing trigger, begin the stream
        print("Capturing histograms")
        self.__dut.check_read_trigger()
        self.__dut.FrameController.begin_stream()
        

    #################################################
    # Configuration done outside of Qt Designer function
    ################################################# 
    def configure(self):
        
        # Add logo
        if self.__logo_found:
            self.MainWindow.setWindowIcon(QtGui.QIcon(self.__logo_path))
        
        # Create font and set text
        font = QtGui.QFont("Times", weight=QtGui.QFont.Bold)
        font.setPointSize(15)
        self.CaptureText.setFont(font)

        # Connect start/stop button
        self.startStopButton.clicked.connect(self.__startImaging)
        
        # Connect the log plotting check box
        self.logPlottingCheckBox.toggled.connect(self.__toggleLogPlotting)
        
        # Connect the auto scaling check box
        self.autoScaleCheckBox.setChecked(True)
        self.autoScaleCheckBox.toggled.connect(self.__toggleAutoScaling)
        
        # Connect the pattern text edit
        self.newPatternSubmitButton.clicked.connect(self.__changePatternPlotted)
        
        # Connect the test setup button
        self.testSetupButton.clicked.connect(self.__show_test_setup_window)
        
        # Connect the scan test button
        self.scanSettingsButton.clicked.connect(self.__showScanWindow)
        
        # Create the plot timer
        self.__createPlotTimer()
        
        # Create list for targeting plots
        self.plot_list = [    self.plotItemChip0,  \
                              self.plotItemChip1,  \
                              self.plotItemChip2,  \
                              self.plotItemChip3,  \
                              self.plotItemChip4,  \
                              self.plotItemChip5,  \
                              self.plotItemChip6,  \
                              self.plotItemChip7,  \
                              self.plotItemChip8,  \
                              self.plotItemChip9,  \
                              self.plotItemChip10, \
                              self.plotItemChip11, \
                              self.plotItemChip12, \
                              self.plotItemChip13, \
                              self.plotItemChip14, \
                              self.plotItemChip15  ]
        
        # Update plot ranges
        for i in range(self.__test_setup.number_of_chips):
            self.plot_list[i].getViewBox().enableAutoRange(axis=ViewBox.YAxis, enable=True)
            # self.plot_list[i].getViewBox().setYRange(0,4095)
            self.plot_list[i].getViewBox().setXRange(0,150)
            # self.plot_list[i].setLabels(title="Chip " + str(i), left="Counts", bottom="Bin")
            self.plot_list[i].setLabels(title="Chip " + str(i+1))
            # self.plot_list[i].setDownsampling(ds=15,mode='subsample')
        
        # Add y-label to left side
        for i in [0, 4, 8, 12]:
            self.plot_list[i].setLabels(left="Counts")
            
        # Add x-label to bottom side
        for i in [12, 13, 14, 15]:
            self.plot_list[i].setLabels(bottom="Bin Number")
            
        # Create default plot pen
        self.plotPen = QtGui.QPen()
        self.plotPen.setColor(QtGui.QColor("blue"))
        self.plotPen.setWidthF(1.25)
        
        # Create special plot pen for emitter
        self.emitterPlotPen = QtGui.QPen()
        self.emitterPlotPen.setColor(QtGui.QColor("red"))
        self.emitterPlotPen.setWidthF(1.25)
        
        # Reload the test setup
        self.__reload_test_setup()
        
        # Initialize the hardware
        if not self.__debug:
            self.__configure_dut()
            self.__power_up()
            self.__configure_frame_controller()
            self.__scan()
        
        
    #################################################
    # Start the imaging process
    #################################################
    def __startImaging(self):
        
        # Change the start button to a stop button
        self.imaging_started = True
        self.__updateStartStopButton()
        
        # Set test setup and scan settings buttons to be unclickable
        self.testSetupButton.setEnabled(False) 
        self.scanSettingsButton.setEnabled(False)
        
        # Reload test settings
        self.__reload_test_setup()
        
        if not self.__debug:
        
            # Reconfigure dut
            self.__reconfigure_dut()
            
            # Reconfigure the frame controller
            self.__configure_frame_controller()
            
            # Rescan
            self.__scan()
        
        # Initialize logging
        if self.__test_setup.logging:
            self.__initialize_logging()
        
        # Initialize reader
        self.__initialize_reader()
        
        # Start the reader thread
        self.__reader.start()
        
        # Reset the plot counter
        self.plot_counter = 0
        
        # Start plot timer
        self.__startPlotTimer()
        
        
    #################################################
    # Stop the imaging process
    #################################################
    def __stopImaging(self):
        
        # Disable stop button, enable start button
        self.imaging_started = False
        self.__updateStartStopButton()
        
        # If this function was triggered by startStopButton, stop the reader thread manually
        if not self.__reader_struct.reader_done:
            self.__reader_struct.reader_should_stop = True
            self.__reader.wait()
        
        # Set test setup and scan settings buttons to be clickable
        self.testSetupButton.setEnabled(True)
        self.scanSettingsButton.setEnabled(True)
        
        # Stop the plot timer
        self.__stopPlotTimer()
        
        
    #################################################
    # Update the button state
    #################################################
    def __updateStartStopButton(self):
        
        # Change the start button to a stop button and vice versa
        if self.imaging_started:
            self.startStopButton.setEnabled(False)
            self.startStopButton.setText("Stop Imaging")
            self.startStopButton.clicked.connect(self.__stopImaging)
            self.startStopButton.clicked.disconnect(self.__startImaging)
            self.startStopButton.setEnabled(True)
        else:
            self.startStopButton.setEnabled(False)
            self.startStopButton.setText("Start Imaging")
            self.startStopButton.clicked.connect(self.__startImaging)
            self.startStopButton.clicked.disconnect(self.__stopImaging)
            self.startStopButton.setEnabled(True)
        
        
    #################################################
    # Update the capture counter
    #################################################
    def __updateCaptureCounter(self):
        
        # Change the capture number
        capture_number = copy(self.__reader_struct.capture_counter)
        self.CaptureText.setText("Capture " + str(capture_number))
        
        
    #################################################
    # Plot the data
    # Plotting works at the data packet level, so number_of_frames is taken from the packet, not the test setup
    #################################################  
    def __plotData(self):
        
        # Increment plot counter
        self.plot_counter += 1
        
        # Update the capture counter
        self.__updateCaptureCounter()
        
        # Update the capture_data
        self.__full_capture_data = self.__packet.data.copy()
        
        # Zero out the zeroeth bin
        for chip in range(self.__packet.number_of_chips):
            for frame in range(self.__packet.number_of_frames):
                for pattern in range(self.__packet.patterns_per_frame):
                    self.__full_capture_data[chip][frame][pattern][0] = 0
                    
        # Calculate the y-max if needed
        if not self.auto_scaling:
            y_max = min(np.amax(self.__full_capture_data), 4095)
        
        # Spawn subplots
        for chip in range(self.__test_setup.number_of_chips):
            
            # Clear existing plot items
            self.plot_list[chip].clear()
            
            # Update axis
            if not self.auto_scaling:
                self.plot_list[chip].getViewBox().setYRange(0,y_max)
            
            # Change plotting to log scale if requested
            self.plot_list[chip].setLogMode(y=self.log_plotting)
            
            # Plot the target pattern data
            if self.__emitter_pattern.emitter_pattern[self.__target_pattern][chip]:
                self.plot_list[chip].plot(range(self.__packet.bins_per_histogram), self.__full_capture_data[chip][0][self.__target_pattern], pen=self.emitterPlotPen)
            else:
                self.plot_list[chip].plot(range(self.__packet.bins_per_histogram), self.__full_capture_data[chip][0][self.__target_pattern], pen=self.plotPen)
            
            
    #################################################
    # Create the logging directory
    #################################################  
    def __initialize_logging(self):
                        
        # Get the date and time for logging directory creation
        date_time=str(datetime.datetime.now())
        
        # Build the log_file_name (conditions_year-month-day_hour-minute-second.csv)
        experiment_directory_name = \
                        self.__test_setup.conditions_str + "_" + \
                        date_time[0:10] + "_" + \
                        date_time[11:13]+ "-" + \
                        date_time[14:16]+ "-" + \
                        date_time[17:19]
        
        # Create directory
        self.__experiment_directory = os.path.join(self.__test_setup.logging_directory, experiment_directory_name)
        os.mkdir(self.__experiment_directory)
        
        # Check that logging directory was created
        if not os.path.exists(self.__experiment_directory):
            raise Exception("Experiment directory " + self.__experiment_directory + " was not created successfully")
            
        # Save test setup
        ts_file = open(os.path.join(self.__experiment_directory, "test_setup.txt"), 'w')
        ts_file.write(str(self.__test_setup))
        ts_file.close()
        
        # Save emitter pattern
        np.save(os.path.join(self.__experiment_directory, "emitter_pattern.npy"), self.__emitter_pattern.emitter_pattern, fix_imports=False)
        
        # Save ir emitters
        np.save(os.path.join(self.__experiment_directory, "ir_emitters.npy"), self.__emitter_pattern.ir_emitters, fix_imports=False)
        
    #################################################
    # Create the reader structure and reader
    ################################################# 
    def __initialize_reader(self):
        
        # Create the reader struct
        self.__reader_struct                    = ReaderStruct()
        
        # Set parameters
        self.__reader_struct.number_of_captures = self.__test_setup.number_of_captures
        self.__reader_struct.debug = self.__debug
        self.__reader_struct.threadpool = self.__threadpool
        self.__reader_struct.stream_mode = self.__test_setup.stream_mode
        
        # If we're logging, we need to specify a directory
        if self.__test_setup.logging and self.__test_setup.logging_directory_set:
            self.__reader_struct.experiment_directory = self.__experiment_directory
            self.__reader_struct.logging = self.__test_setup.logging
        else:
            self.__reader_struct.logging = False
        
        # Create the reader thread
        self.__reader = Reader(self.__dut, self.__packet, self.__reader_struct)
        
        # Connect the finished signal
        self.__reader.finished.connect(self.__reader_finished)
        
        
    #################################################
    # If the reader sends the finished signal and it was not initiated by the main thread, it will stop the imaging process
    ################################################# 
    def __reader_finished(self):
        print("Reader thread called finish")
        if not self.__reader_struct.reader_should_stop:
            self.__stopImaging()
        
                
    #################################################
    # Create the plotting timer
    #################################################
    def __createPlotTimer(self):
        
        # Create a precise timer
        self.plotTimer=QtCore.QTimer()
        self.plotTimer.setTimerType(QtCore.Qt.PreciseTimer)
        # self.plotTimer.setSingleShot(True)
        
        # Connect the timer's timeout function to the plot function
        self.plotTimer.timeout.connect(self.__plotData)
        
    
    #################################################
    # Start the plotting timer
    #################################################
    def __startPlotTimer(self):
        
        # print("Starting plot timer")
        self.plotTimer.start(self.plotInterval)
        
        
    #################################################
    # Stop the plotting timer
    #################################################
    def __stopPlotTimer(self):
        
        # print("Stopping plot timer")
        self.plotTimer.stop()
        

    #################################################
    # Change the plotted pattern
    #################################################
    def __changePatternPlotted(self):
        
        # Get the new pattern
        new_pattern = int(self.patternPlottedTextEdit.toPlainText())
        
        # Verify it is in the range of acceptable patterns
        if (new_pattern >= 0) and (new_pattern < self.__test_setup.patterns_per_frame):
            print("New pattern accepted")
            self.__target_pattern = new_pattern
        else:
            print("New pattern invalid")
        
        # Update the text
        self.patternPlottedTextEdit.setPlainText(str(self.__target_pattern))
        
        
    #################################################
    # Set log plotting
    #################################################
    def __toggleLogPlotting(self):
        
        if self.log_plotting:
            print("Changing to linear plotting")
            self.log_plotting = False
            
        else:
            print("Changing to log plotting")
            self.log_plotting = True
        
        # Change plotting to log scale if requested
        for chip in range(self.__test_setup.number_of_chips):
            self.plot_list[chip].setLogMode(y=self.log_plotting)
     
            
    #################################################
    # Set auto scaling
    #################################################  
    def __toggleAutoScaling(self):
        
        if self.auto_scaling:
            print("Changing to fixed scale")
            self.auto_scaling = False
            for i in range(self.__test_setup.number_of_chips):
                self.plot_list[i].getViewBox().enableAutoRange(axis=ViewBox.YAxis, enable=False)
        else:
            print("Changing to auto scaling")
            self.auto_scaling = True
            for i in range(self.__test_setup.number_of_chips):
                self.plot_list[i].getViewBox().enableAutoRange(axis=ViewBox.YAxis, enable=True)
            
            
    #################################################
    # Create scan window
    #################################################
    def __showScanWindow(self):
        
        # Create the scan window
        self.scanWindow = Ui_ScanWindowDialog(0)
        self.scanDialog = QtWidgets.QDialog()
        self.scanDialog.setModal(True)
        if self.__logo_found:
            self.scanDialog.setWindowIcon(QtGui.QIcon(self.__logo_path))
        self.scanWindow.setupUi(self.scanDialog)
        self.scanDialog.show()
        
        
    #################################################
    # Create test setup window
    #################################################
    def __show_test_setup_window(self):
        
        # Create the emitter pattern window
        self.test_setup_window = Ui_TestSetupDialog(self.__test_setup, self.__emitter_pattern)
        self.test_setup_dialog = QtWidgets.QDialog()
        self.test_setup_dialog.setModal(True)
        if self.__logo_found:
            self.test_setup_dialog.setWindowIcon(QtGui.QIcon(self.__logo_path))
        self.test_setup_window.setupUi(self.test_setup_dialog)
        self.test_setup_window.configure()
        self.test_setup_dialog.show()
        

    #################################################
    # Reload from test setup
    #################################################
    def __reload_test_setup(self):

        # Create packet based on test setup information
        # TODO determine if this needs to be preset to 0
        self.__packet =  DataPacket(self.__test_setup.number_of_chips, self.__test_setup.number_of_frames, self.__test_setup.patterns_per_frame, self.__test_setup.measurements_per_pattern, self.__test_setup.period)
        
        # Data structure for plotting pattern-dependent data
        # TODO determine if this needs to be preset to 0
        self.__full_capture_data = np.empty((self.__packet.number_of_chips, self.__packet.number_of_frames, self.__packet.patterns_per_frame, self.__packet.bins_per_histogram), dtype=int)
        
        # Update pattern plotted
        if self.__target_pattern >= self.__test_setup.patterns_per_frame:
            self.patternPlottedTextEdit.setPlainText(str(0))
            self.__changePatternPlotted()
        
        # Total counts
        # TODO Implement average counts display on pyqtgraphs
        # TODO determine if this needs to be preset to 0
        self.__average_counts = np.empty((self.__packet.number_of_chips), dtype=float)
        


if __name__ == "__main__":
    import sys
    
    # DUT and packet for initializing mainwindow
    dut = None

    # Run app
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # Set logo
    # self.test_setup_dialog.setWindowIcon(QtGui.QIcon("logo.png"))
    ui = Ui_PlotWindow(dut)
    ui.setupUi(MainWindow)
    ui.configure()
    MainWindow.show()
    sys.exit(app.exec_())

