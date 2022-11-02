# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 08:38:51 2021

@author: Dell-User
"""

from includes import *
from PyQt5 import QtWidgets

# Debug
debug = False

# Instantiate test platform
if not debug:
    dut = test_platform.TestPlatform("moana3")
else:
    dut = None

# Run app
try:
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MoanaGui.Ui_PlotWindow(dut, paths.bitfile_path, debug=debug)
    ui.setupUi(MainWindow)
    ui.configure()
    MainWindow.show()
    sys.exit(app.exec_())
finally:
    if not debug:
        print("Ending stream")
        dut.FrameController.end_stream()
        
        print("Disabling power supplies")
        dut.disable_cath_sm_supply()
        dut.disable_hvdd_ldo_supply()
    
        print("Closing FPGA")
        dut.fpga_interface.xem.Close()