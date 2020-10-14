import sys
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QTableView
from PyQt5.QtCore import QDir, Qt


from openpyxl import load_workbook, Workbook, styles, worksheet
import numpy as np

from indexing import indexing as index
from dataTableViewModel import dataTableViewModel
from h2hTableViewModel import h2hTableViewModel


class main(QMainWindow):
    
    def __init__(self, ui_file):
        super(main, self).__init__()
        self.window = uic.loadUi(ui_file, self)
        self.window.show()

        self.window.openXL.triggered.connect(self.fileOpen) # when 'file -> open' is selected
        self.window.newXL.triggered.connect(self.fileNew) # when 'file -> new' is selected
        self.window.saveXL.triggered.connect(self.fileSave) # when 'file -> save' is selected
        self.window.saveAsXL.triggered.connect(self.fileSaveAs) # when 'file -> save as ...' is selected
        self.window.addNewResultButton.clicked.connect(self.addNewResult) # when 'Add new result' is pressed

    # logic for the 'Open' fileMenu option - initializes match data table  
    def fileOpen(self): 
        self.xlfile = QFileDialog.getOpenFileName(self, 'Select XL')

        if self.xlfile[0].endswith('.xlsx'):
            ### parse the results spreadsheet and prepare the dataTableViewModel
            self.xlpalmares = load_workbook(self.xlfile[0])
            self.xlpalmares.active = 0
            ws_singles = self.xlpalmares.active

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

            ### parse the h2h statistics spreadsheet
            self.xlpalmares.active = 1
            ws_h2h = self.xlpalmares.active

            self.h2h_data = np.empty(shape=(ws_h2h.max_row, 3), dtype='U64')
            self.h2h_header = np.array(['Score', '', 'Adversar'], dtype='U64')

        else:
            print('Cancel was pressed or a non .xlsx file format was selected, please re-open the desired file\n')

    def fileNew(self):
        self.header = np.array(['Data', 'Adversar', 'Rezultat', 'Set1', 'Set2', 'Set3', 'Set 4', 'Set 5', 'Set 6', 'Set 7', 'Set 8', 'Set 9', 'Tip', 'Round', 'Oras', 'Locatie', 'Suprafata', 'Rate', 'Observatii'], dtype='U64')
        self.match_data = np.empty(shape=(1, self.header.size), dtype='U64')
        self.h2h_header = np.array(['Score', '', 'Adversar'], dtype='U64')
        self.h2h_data = np.empty(shape=(1, self.h2h_header.size), dtype='U64')

        self.dtVM = dataTableViewModel(self.match_data, self.header, self.h2h_data, self.h2h_header, self.window)
        self.window.dataTableView.setModel(self.dtVM)        

    def fileSave(self):
        try:
            self.match_data = self.dtVM._data
            self.header = self.dtVM._header
        except:
            self.window.debugText.insertPlainText('You must have a table open before saving!\n')

    def fileSaveAs(self):
        try:
            self.match_data = self.dtVM._data
            self.header = self.dtVM._header
            XLmodified = Workbook()
            ws_out = XLmodified.active
            ws_out.title = 'Results'
            for col in range(0, self.header.size):
                ws_out.cell(row=1, column=col+1).value = self.header[col]

            for row in range(0, self.match_data.shape[0]):
                for col in range(0, self.match_data.shape[1]):
                    ws_out.cell(row=row+2, column=col+1).value = self.match_data[row][col]

            XLmodified.create_sheet('h2h')
            for ii in range(len(XLmodified.sheetnames)):
                if XLmodified.sheetnames[ii] == 'h2h':
                    break

            XLmodified.active = ii
            ws_out = XLmodified.active
            self.h2h_data = self.dtVM.h2hVM._data
            self.h2h_header = self.dtVM.h2hVM._header
            for col in range(0, self.h2h_header.size):
                ws_out.cell(row=1, column=col+1).value = self.h2h_header[col]

            for row in range(0, self.h2h_data.shape[0]):
                for col in range(0, self.h2h_data.shape[1]):
                    ws_out.cell(row=row+2, column=col+1).value = self.h2h_data[row][col]
        
            self_xlfile = QFileDialog.getSaveFileName(self)
            XLmodified.save(self_xlfile[0] + '.xlsx')
        except: 
            self.window.debugText.insertPlainText('You must have a table open before saving!\n')

    def addNewResult(self):
        try: 
            self.dtVM._data = np.vstack((self.dtVM._data, np.empty(shape=(1, index.col_end_xl-index.col_start_xl), dtype='U64')))
            self.dtVM.layoutChanged.emit()
        except: 
            self.window.debugText.insertPlainText('You must create a new table or open an already existing one first!\n')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            


