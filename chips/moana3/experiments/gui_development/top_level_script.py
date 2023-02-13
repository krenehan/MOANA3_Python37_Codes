# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 08:38:51 2021

@author: Dell-User
"""

from includes import *
from PyQt5 import QtWidgets

# Debug
debug = False

# Run app
app = QtWidgets.QApplication(sys.argv)
MainWindow = MoanaGui.PlotWindow(debug=debug, bitfile_path=paths.bitfile_path)
MainWindow.configure()
MainWindow.show()
sys.exit(app.exec_())