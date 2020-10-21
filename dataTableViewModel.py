from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
import numpy as np

from h2hTableViewModel import h2hTableViewModel
from statistics import statistics as st
from refresh import refresh

class dataTableViewModel(QAbstractTableModel):
    
    def __init__(self, data, header, h2h_data, h2h_header, window, indexes):
        super(dataTableViewModel, self).__init__()
        self._data = data
        self._header = header
        self._h2h_data = h2h_data
        self._h2h_header = h2h_header
        self._window = window
        self._index = indexes

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

        if index.column() == self._index.date: # when editing 'Data' cell
            test=1

        elif index.column() == self._index.op: # when editing 'Adversar' cell
            if self._data[index.row(), index.column()] == value: # when cell value did not change
                self._window.debugText.insertPlainText('Cell value remained the same.\n')
            elif (self._data[index.row(), index.column()] == None or self._data[index.row(), index.column()] == np.array([''])) and \
                    (value != None and value != np.array([''])): # when empty cell is edited with non-empty value

                st.h2h_sets(self._data, self._index, index, self._window)

                index_h2h_op = np.where(self.h2hVM._data[:, self._index.h2h_op] == value) 

                if index_h2h_op[0].size == 0:
                    st.h2h_result_first(self._data, self.h2hVM._data, index_h2h_op[0], self._index, index, value)
                    refresh.h2h_score(self.h2hVM, self._h2h_data.shape[0]-1, self._index)
                    refresh.h2h_opponent(self.h2hVM, self._h2h_data.shape[0]-1, self._index)

                    self.h2hVM._data = np.vstack((self.h2hVM._data, np.empty(shape=(1, self._h2h_data.shape[1]), dtype='U64')))
                    self.h2hVM.layoutChanged.emit()   

                else:
                    st.h2h_result_update(self._data, self.h2hVM._data, index_h2h_op[0], self._index, index)
                    refresh.h2h_score(self.h2hVM, index_h2h_op[0], self._index)
               
            elif (self._data[index.row(), index.column()] != None or self._data[index.row(), index.column()] != np.array([''])) and \
                 (value != None and value != np.array([''])): # when non-empty cell contents are changed/edited

                st.h2h_sets(self._data, self._index, index, self._window)

                index_h2h_op_old = np.where(self.h2hVM._data[:, self._index.h2h_op] == self._data[index.row(), index.column()]) 
                index_h2h_op_new = np.where(self.h2hVM._data[:, self._index.h2h_op] == value)
                
                if index_h2h_op_new[0].size == 0:
                    st.h2h_result_remove(self._data,  self.h2hVM._data, index_h2h_op_old[0], self._index, index)
                    refresh.h2h_score(self.h2hVM, self._h2h_data.shape[0]-1, self._index)

                    st.h2h_result_first(self._data, self.h2hVM._data, index_h2h_op_new[0], self._index, index, value)
                    refresh.h2h_score(self.h2hVM, self._h2h_data.shape[0]-1, self._index)
                    refresh.h2h_opponent(self.h2hVM, self._h2h_data.shape[0]-1, self._index)

                    self.h2hVM._data = np.vstack((self.h2hVM._data, np.empty(shape=(1, self._h2h_data.shape[1]), dtype='U64')))
                    self.h2hVM.layoutChanged.emit() 

                else:
                    st.h2h_result_remove(self._data,  self.h2hVM._data, index_h2h_op_old[0], self._index, index)
                    refresh.h2h_score(self.h2hVM, index_h2h_op_old[0], self._index)

                    st.h2h_result_update(self._data, self.h2hVM._data, index_h2h_op_new[0], self._index, index)
                    refresh.h2h_score(self.h2hVM, index_h2h_op_new[0], self._index)
                    test=1

            elif (self._data[index.row(), index.column()] != None or self._data[index.row(), index.column()] != np.array([''])) and \
                 (value == None and value == np.array([''])): # when name in cell is deleted

                st.h2h_sets(self._data, self._index, index, self._window)
                index_h2h_op = np.where(self.h2hVM._data[:, self._index.h2h_op] == self._data[index.row(), index.column()])

                st.h2h_result_remove(self._data,  self.h2hVM._data, index_h2h_op[0], self._index, index)
                refresh.h2h_score(self.h2hVM, index_h2h_op[0], self._index)

        elif index.column() == self._index.set1 or index.column() == self._index.set2 or index.column() == self._index.set3: # when editing 'SetN' cell
            st.h2h_sets(self._data, self._index, index, self._window)
            self._data[index.row(), index.column()] = str(value)
            st.h2h_sets_update(self._data, self._index, index, self._window)

            index_h2h_op = np.where(self.h2hVM._data[:, self._index.h2h_op] == self._data[index.row(), self._index.op])
            if st.sets_won != st.sets_won_new or st.sets_lost != st.sets_lost_new: # if sets won or lost changed
                if self._data[index.row(), self._index.op] == None or self._data[index.row(), self._index.op] == np.array(['']): # check if name empty
                    self._window.debugText.insertPlainText('Please input opponent name! \n')
                else:
                    st.h2h_compare_results(self._data, self.h2hVM._data, index_h2h_op[0], self._index, index, self._window)

            refresh.h2h_score(self.h2hVM, index_h2h_op[0], self._index)


        self._data[index.row(), index.column()] = str(value)       
        self.dataChanged.emit(index, index, (Qt.DisplayRole, ))

        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            header = self._header[section]
            return str(header)
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            header = section
            return str(header)


