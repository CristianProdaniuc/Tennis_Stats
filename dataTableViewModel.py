from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
import numpy as np

from h2hTableViewModel import h2hTableViewModel

class dataTableViewModel(QAbstractTableModel):
    
    def __init__(self, data, header, h2h_data, h2h_header, window):
        super(dataTableViewModel, self).__init__()
        self._data = data
        self._header = header
        self._h2h_data = h2h_data
        self._h2h_header = h2h_header
        self._window = window

        self.h2hVM = h2hTableViewModel(self._h2h_data, self._h2h_header)     
        self._window.h2hTableView.setModel(self.h2hVM)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def setData(self, index, value, role=Qt.EditRole):

        if self._header[index.column()] == 'Data': # when editing 'Data' cell
            test=1
        elif self._header[index.column()] == 'Adversar': # when editing 'Adversar' cell
            if self._data[index.row(), index.column()] == str(value): # when cell value did not change
                self._window.debugText.insertPlainText('Cell value remained the same.\n')
            elif (self._data[index.row(), index.column()] == None or self._data[index.row(), index.column()] == np.array([''])) and \
                    (value != None and value != np.array([''])): # when empty cell is edited with non-empty value
                sets_won = 0
                sets_lost = 0
                for col in range(3, 6):
                    lindex = self._data[index.row(), col].find('-')
                    if lindex == -1 and col < 5:
                        self._window.debugText.insertPlainText('Invalid score or empty cell for sets 1 and/or 2. Please input the score in the following format: \'X-Y\'\n')
                        self._data[index.row(), 2] = 'NA'
                        break
                    elif lindex == -1 and col >= 5:
                        break
                    elif self._data[index.row(), col][-2:] == 'ab':
                        sets_won = 10
                    elif int(self._data[index.row(), col][0:lindex]) > int(self._data[index.row(), col][lindex+1:]) and \
                         int(self._data[index.row(), col][0:lindex]) > 5:
                        sets_won += 1
                    elif int(self._data[index.row(), col][0:lindex]) < int(self._data[index.row(), col][lindex+1:]) and \
                         int(self._data[index.row(), col][lindex+1:]) > 5:
                        sets_lost += 1

                if sets_won > sets_lost and sets_won > 1:
                    self.h2hVM._data[-1, 2] = str(value)
                    self.h2hVM._data[-1, 0] = '1-0'
                    self._data[index.row(), 2] = 'W'

                    self.h2h_index = self.h2hVM.createIndex(0, 0)
                    self.h2hVM.setData(self.h2h_index, self.h2hVM._data[-1, 0], role=Qt.EditRole)
                    self.h2h_index = self.h2hVM.createIndex(0, 2)
                    self.h2hVM.setData(self.h2h_index, self.h2hVM._data[-1, 2], role=Qt.EditRole)

                    self.h2hVM._data = np.vstack((self.h2hVM._data, np.empty(shape=(1, 3), dtype='U64')))
                    self.h2hVM.layoutChanged.emit()   
                    
                elif sets_won < sets_lost and sets_lost > 1:
                    self.h2hVM._data[-1, 2] = str(value)
                    self.h2hVM._data[-1, 0] = '0-1'
                    self._data[index.row(), 2] = 'L'

                    self.h2h_index = self.h2hVM.createIndex(0, 0)
                    self.h2hVM.setData(self.h2h_index, self.h2hVM._data[-1, 0], role=Qt.EditRole)
                    self.h2h_index = self.h2hVM.createIndex(0, 2)
                    self.h2hVM.setData(self.h2h_index, self.h2hVM._data[-1, 2], role=Qt.EditRole)

                    self.h2hVM._data = np.vstack((self.h2hVM._data, np.empty(shape=(1, 3), dtype='U64')))
                    self.h2hVM.layoutChanged.emit()  
                    
                else:
                    self._data[index.row(), 2] = 'NA'
               

        self._data[index.row(), index.column()] = str(value)

        #if self._data[index.row(), 1] != None and self._data[index.row(), 1] != np.array(['']):
        #    index_adversar = np.where(self.h2hVM._data[:, 2] == self._data[index.row(), 1])
            
        #    if index_adversar[0].size == 0:
        #        self.h2hVM._data = np.vstack((self.h2hVM._data, np.empty(shape=(1, 3), dtype='U64')))
        #        self.h2hVM.layoutChanged.emit()
        

        
        self.dataChanged.emit(index, index, (Qt.DisplayRole, ))
        #self.h2h_index = self.h2hVM.createIndex(0, 0)
        #self.h2hVM.setData(self.h2h_index, 'test', role=Qt.EditRole)


        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            header = self._header[section]
            return str(header)
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            header = section
            return str(header)


