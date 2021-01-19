from openpyxl import load_workbook, Workbook, styles, worksheet
import numpy as np
import sys, os 
from main_window import main
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) #get project root directory
# start the GUI
app = QApplication(sys.argv)
main(ROOT_DIR + '\\GUI\\main.ui')
sys.exit(app.exec_())