import sys
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QTableView
from PyQt5.QtCore import QDir, Qt


from openpyxl import load_workbook, Workbook, styles, worksheet
import numpy as np

from indexing import indexing as index
from dataTableViewModel import dataTableViewModel


class main(QMainWindow):
    
    def __init__(self, ui_file):
        super(main, self).__init__()
        self.window = uic.loadUi(ui_file, self)
        self.window.show()

        self.window.openXL.triggered.connect(self.fileOpen) # when file -> open is selected
        self.window.newXL.triggered.connect(self.fileNew) # when file -> new is selected
        self.window.saveAsXL.triggered.connect(self.fileSaveAs)

    # logic for the 'Open' fileMenu option - initializes match data table  
    def fileOpen(self): 
        self_xlfile = QFileDialog.getOpenFileName(self, 'Select XL')
        self_xlpalmares = load_workbook(self_xlfile[0])
        self_xlpalmares.active = 0
        ws_singles = self_xlpalmares.active

        index.origin(ws_singles)
        index.rows(ws_singles)
        index.columns(ws_singles)        

        self.match_data = np.empty(shape=(index.row_end_xl-index.row_start_xl, index.col_end_xl-index.col_start_xl), dtype='U64')
        self.header = np.empty(shape=index.col_end_xl-index.col_start_xl, dtype='U64')

        for row in range(0, index.row_end_py - index.row_start_py):
            for col in range(0, index.col_end_py - index.col_start_py):
                self.match_data[row][col] = ws_singles.cell(row = index.row_start_xl +row, column = index.col_start_xl +col).value

        for col in range(0, index.col_end_py - index.col_start_py):
            self.header[col] = ws_singles.cell(row=index.header_xl, column=index.col_start_xl +col).value

        self.dtVM = dataTableViewModel(self.match_data, self.header)
        self.window.dataTableView.setModel(self.dtVM)

    def fileNew(self):
        self.header_data = np.array(['Data', 'Adversar', 'Rezultat', 'Set1', 'Set2', 'Set3', 'Set 4', 'Set 5', 'Set 6', 'Set 7', 'Set 8', 'Set 9', 'Tip', 'Round', 'Oras', 'Locatie', 'Suprafata', 'Rate', 'Observatii'], dtype='U64')
        self.match_data = np.empty(shape=(1, self.header_data.size), dtype='U64')
        self.dtVM = dataTableViewModel(self.match_data, self.header_data)
        self.window.dataTableView.setModel(self.dtVM)

    def fileSaveAs(self):
        XLmodified = Workbook()
        ws_out = XLmodified.active
        for col in range(0, self.header_data.size):
            ws_out.cell(row=1, column=col+1).value = self.header_data[col]

        for row in range(0, self.match_data.shape[0]):
            for col in range(0, self.match_data.shape[1]):
                ws_out.cell(row=row+2, column=col+1).value = self.match_data[row][col]

        self_xlfile = QFileDialog.getSaveFileName(self)
        XLmodified.save(self_xlfile[0] + '_xlsx')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            


