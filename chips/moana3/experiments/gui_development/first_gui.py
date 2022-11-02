# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Dell-User\Dropbox\MOANA\2020 January Tapeout\MOANA2 Python Codes\MOANA2_Python37_Codes\chips\moana2\experiments\gui_development\demo.ui'
#
# Created by: PyQt5 UI code generator 5.9.2

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from time import sleep, perf_counter
from copy import copy
import os
import datetime
from ScanWindowDialog import Ui_ScanWindowDialog

class Reader(QtCore.QThread):
    """ Reader polls the read trigger, updates the packet with new data, and writes chip data to a file. """
    
    # data_available = QtCore.pyqtSignal(bool)  # Signal indicating new UI data is available

    #################################################
    # Constructor
    ################################################# 
    def __init__(self, dut, packet, enable_logs):
        
        # Init QThread
        super().__init__()
        
        # Handles passed to worker thread
        self.__dut = dut
        self.__packet = packet
        self.__enable_logs = enable_logs
        
        # Public variables
        self.capture_counter = 0
        self.reader_should_stop = False
        
        # Create the log file
        if self.__enable_logs:
            self.createLogFile()
      
        
    #################################################
    # Create the log file
    #################################################
    def createLogFile(self):
        
        # Print statement
        print("Creating log file")
        
        # Create the results directory if it does not exist
        results_dir = 'C:/Users/Dell-User/Downloads/'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
            
        # Get the date and time
        date_time=str(datetime.datetime.now())
        
        # Create the log_file_name (year-month-day, hour, minute, second)
        log_file_name = "%s_%s-%s-%s.csv" % (date_time[0:10], date_time[11:13], date_time[14:16], date_time[17:19])
        
        # File header
        header = 'Time\n'
        self.log_file = open(results_dir + log_file_name, 'w')
        self.log_file.write(header)
        

    #################################################
    # Write to a log file
    ################################################# 
    def writeToLog(self):
        
        # Write to the log file
        self.log_file.write(str(self.time) + '\n')
        
        
    #################################################
    # Read function for updating data packet
    #################################################      
    def readData(self):
        
        # Call the read function
        self.__packet.data = np.random.randint(0, np.random.randint(1, high = 4096, size=1)[0], (self.__packet.number_of_chips* self.__packet.number_of_frames * self.__packet.patterns_per_frame * self.__packet.bins_per_histogram))
        self.time = perf_counter()
        
        # Call 
        self.capture_counter += 1
        # print("Capture counter incremented in reader class")


    #################################################
    # Run function (called implicitly by thread.start)
    #################################################
    def run(self):
        
        # Event loop
        while True:
            
            # Read data and log until stopped
            if not self.reader_should_stop:
                # sleep(0.01)
                self.readData()
                if self.__enable_logs:
                    self.writeToLog()
            else:
                self.stop()
                break
            
            # if self.__dut.check_read_trigger():
                # self.data_available.emit(True)
                # break
            
            
    #################################################
    # Stop function
    #################################################   
    def stop(self):
        
        # Close the log file
        if self.__enable_logs:
            print("Closing log file")
            self.log_file.close()


class Ui_PlotWindow(object):
    
    
    #################################################
    # Constructor for main window
    #################################################
    def __init__(self, dut, packet, number_of_captures, fps):
        
        # Store the dut handle so that read function can be called
        self.__dut                              = dut
        
        # Store packet handle
        self.__packet                           = packet
        
        # Packet parameters
        self.__number_of_chips                  = self.__packet.number_of_chips
        self.__measurements_per_pattern         = self.__packet.measurements_per_pattern
        self.__patterns_per_frame               = self.__packet.patterns_per_frame
        self.__number_of_frames                 = self.__packet.number_of_frames
        self.__period                           = self.__packet.period
        self.__bins_per_histogram               = self.__packet.bins_per_histogram
        
        # Capture parameters
        self.number_of_captures                 = number_of_captures
        self.capture_counter                    = 0
        
        # Plotting params
        self.fps                                = fps
        self.plotInterval                       = 1/fps
        self.log_plotting                       = False
        self.plot_counter                       = 0
        self.__target_pattern                    = 0
        
        # Logging
        self.__enable_logs                      = False
        
        # Calculate read interval
        # self.read_interval = self.__number_of_frames * self.__patterns_per_frame * self.__measurements_per_pattern * (self.__period*1e-9) * 1000
        self.read_interval = 2
        print("Period is " + str(self.__period))
        print("Read interval is " + str(self.read_interval) + " ms")
            
        # Data structure for plotting pattern-dependent data
        self.__full_capture_data = np.empty((self.__number_of_chips, self.__number_of_frames, self.__patterns_per_frame, self.__bins_per_histogram), dtype=int)
        
        # Total counts
        self.__total_counts_data = np.empty((self.__number_of_chips, self.__number_of_frames, self.__patterns_per_frame), dtype=int)
        self.__average_total_counts = np.empty((self.__number_of_chips), dtype=float)
    
    
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
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(420, 630, 221, 31))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.loggingCheckBox = QtWidgets.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.loggingCheckBox.setFont(font)
        self.loggingCheckBox.setObjectName("loggingCheckBox")
        self.horizontalLayout_2.addWidget(self.loggingCheckBox)
        self.logPlottingCheckBox = QtWidgets.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.logPlottingCheckBox.setFont(font)
        self.logPlottingCheckBox.setObjectName("logPlottingCheckBox")
        self.horizontalLayout_2.addWidget(self.logPlottingCheckBox)
        self.newPatternSubmitButton = QtWidgets.QPushButton(self.centralwidget)
        self.newPatternSubmitButton.setGeometry(QtCore.QRect(240, 630, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.newPatternSubmitButton.setFont(font)
        self.newPatternSubmitButton.setObjectName("newPatternSubmitButton")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(688, 630, 331, 29))
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.scanTestButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.scanTestButton.setFont(font)
        self.scanTestButton.setObjectName("scanTestButton")
        self.horizontalLayout_3.addWidget(self.scanTestButton)
        self.DataTxTestButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.DataTxTestButton.setFont(font)
        self.DataTxTestButton.setObjectName("DataTxTestButton")
        self.horizontalLayout_3.addWidget(self.DataTxTestButton)
        self.streamTestButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.streamTestButton.setFont(font)
        self.streamTestButton.setObjectName("streamTestButton")
        self.horizontalLayout_3.addWidget(self.streamTestButton)
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
        self.loggingCheckBox.setText(_translate("MainWindow", "Logging"))
        self.logPlottingCheckBox.setText(_translate("MainWindow", "Log Plotting"))
        self.newPatternSubmitButton.setText(_translate("MainWindow", "Update Pattern"))
        self.scanTestButton.setText(_translate("MainWindow", "Scan Test"))
        self.DataTxTestButton.setText(_translate("MainWindow", "DataTx Test"))
        self.streamTestButton.setText(_translate("MainWindow", "Stream Test"))

        
    #################################################
    # Configuration done outside of Qt Designer function
    ################################################# 
    def myConfig(self):
        
        # Create font and set text
        font = QtGui.QFont("Times", weight=QtGui.QFont.Bold)
        font.setPointSize(15)
        self.CaptureText.setFont(font)

        # Connect start/stop button
        self.startStopButton.clicked.connect(self.__startImaging)
        
        # Connect the log plotting check box
        self.logPlottingCheckBox.toggled.connect(self.__toggleLogPlotting)
        
        # Connect the logging check box
        self.loggingCheckBox.toggled.connect(self.__toggleLogging)
        
        # Connect the pattern text edit
        self.newPatternSubmitButton.clicked.connect(self.__changePatternPlotted)
        
        # Connect the scan test button
        self.scanTestButton.clicked.connect(self.__showScanWindow)
        
        # Create the plot timer
        # self.createReadTriggerTimer()
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
        for i in range(self.__number_of_chips):
            self.plot_list[i].getViewBox().enableAutoRange(axis=ViewBox.YAxis, enable=True)
            # self.plot_list[i].getViewBox().setYRange(0,4095)
            self.plot_list[i].getViewBox().setXRange(0,150)
            # self.plot_list[i].setLabels(title="Chip " + str(i), left="Counts", bottom="Bin")
            self.plot_list[i].setLabels(title="Chip " + str(i))
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


    #################################################
    # Reset after imaging process expires
    #################################################    
    def __reset(self):
        
        # Initialize class variables
        self.imaging_started = False
        
        
    #################################################
    # Start the imaging process
    #################################################
    def __startImaging(self):
        
        # Change the start button to a stop button
        self.imaging_started = True
        self.__updateStartStopButton()
        
        # Set logging radio button to be uncheckable
        self.loggingCheckBox.setCheckable(False)        
                
        # Start the read timer
        # self.startReadTriggerTimer(self.read_interval)
        
        # Create the reader thread
        self.reader = Reader(self.__dut, self.__packet, self.__enable_logs)
        
        # Start the reader thread
        self.reader.start()
        
        # Start plot timer
        self.__startPlotTimer()
        
        
    #################################################
    # Stop the imaging process
    #################################################
    def __stopImaging(self):
        
        # Disable stop button, enable start button
        self.imaging_started = False
        self.__updateStartStopButton()
        
        # Exit the read thread
        self.reader.reader_should_stop = True
        self.reader.quit()
        self.reader.wait()
        
        # Set logging radio button to be checkable
        self.loggingCheckBox.setCheckable(True)
        
        # Stop the read timer
        # self.stopReadTriggerTimer()
        
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
    # Update the button state
    #################################################
    # def __updateStartStopButton(self):
        
        
    #################################################
    # Update the capture counter
    #################################################
    def __updateCaptureCounter(self):
        
        # Increment the counter
        # print("Counter incremented")
        # self.capture_counter += 1
        
        # Change the capture number
        capture_number = copy(self.reader.capture_counter)
        self.CaptureText.setText("Capture " + str(capture_number))
        # print("Capture counter is " + str(capture_number))
        
        # Check to see if imaging is done
        if (capture_number >= self.number_of_captures):
            self.__stopImaging()
            self.__reset()
            
            
    # #################################################
    # # Read function for updating data packet
    # #################################################      
    # def readData(self):
        
    #     # Call the read function
    #     # print("Reading data")
    #     # self.__dut.read_master_fifo_data(self.__packet)
    #     self.__packet.data = np.random.randint(0, 4096, (self.__number_of_chips* self.__number_of_frames * self.__patterns_per_frame * self.__bins_per_histogram))

    #     # Increment the capture counter
    #     self.incrementCaptureCounter()
        
    #     # Plot
    #     if ~self.plotTimer.isActive():
    #         self.__startPlotTimer()
        
        
    #################################################
    # Plot the data
    #################################################  
    def __plotData(self):
        
        # Increment plot counter
        self.plot_counter += 1
        
        # Update the capture counter
        self.__updateCaptureCounter()
        
        # Update the capture_data
        self.__full_capture_data = self.__packet.data.copy()
        
        # Zero out the zeroeth bin
        for chip in range(self.__number_of_chips):
            for frame in range(self.__number_of_frames):
                for pattern in range(self.__patterns_per_frame):
                    self.__full_capture_data[chip][frame][pattern][0] = 0
        
        # Spawn subplots
        for chip in range(self.__number_of_chips):
            
            # Clear existing plot items
            self.plot_list[chip].clear()
            
            # Plot the target pattern data
            self.plot_list[chip].plot(range(self.__bins_per_histogram), self.__full_capture_data[chip][0][self.__target_pattern], pen=self.plotPen)
            
            # Change plotting to log scale if requested
            self.plot_list[chip].setLogMode(y=self.log_plotting)
                  
                
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
        if (new_pattern >= 0) and (new_pattern < self.__patterns_per_frame):
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
         
            
    #################################################
    # Set logging
    #################################################
    def __toggleLogging(self):
        
        if self.__enable_logs:
            print("Disable logging")
            self.__enable_logs = False
        else:
            print("Enable logging")
            self.__enable_logs = True
            
            
    #################################################
    # Create scan window
    #################################################
    def __showScanWindow(self):
        
        # Create the scan window
        self.scanWindow = Ui_ScanWindowDialog()
        self.scanDialog = QtWidgets.QDialog()
        self.scanDialog.setModal(True)
        self.scanDialog.setWindowIcon(QtGui.QIcon("logo.png"))
        self.scanWindow.setupUi(self.scanDialog)
        self.scanDialog.show()
        

from pyqtgraph import GraphicsLayoutWidget, PlotWidget, ViewBox, setConfigOptions

if __name__ == "__main__":
    import sys
    from includes import *
    
    # Params
    number_of_chips = 16
    number_of_frames = 1
    patterns_per_frame = 16
    measurements_per_pattern = 32000
    period = 20.0
    number_of_captures = 1000
    fps = 20
    
    # DUT and packet for initializing mainwindow
    dut = None
    packet = DataPacket.DataPacket(number_of_chips, number_of_frames, patterns_per_frame, measurements_per_pattern, period)

    # Set default background and foreground colors
    setConfigOptions(background='w', foreground='k')

    # Run app
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # Set logo
    icon = QtGui.QIcon("logo.png")
    MainWindow.setWindowIcon(icon)
    ui = Ui_PlotWindow(dut, packet, number_of_captures, fps)
    ui.setupUi(MainWindow)
    ui.myConfig()
    MainWindow.show()
    sys.exit(app.exec_())

