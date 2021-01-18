from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtWidgets import QTableView
import numpy as np
from datetime import datetime as dt

from h2hTableViewModel import h2hTableViewModel
from statsTableViewModel import statsTableViewModel

from statistics import statistics as st
from refresh import refresh

class dataTableViewModel(QAbstractTableModel):
    
    def __init__(self, data, header, h2h_data, h2h_header, stats_data, stats_header, stats_years, window, indexes):
        super(dataTableViewModel, self).__init__()
        self._data = data
        self._header = header
        self._h2h_data = h2h_data
        self._h2h_header = h2h_header
        self._stats_data = stats_data
        self._stats_header = stats_header
        self._stats_years = stats_years
        self._window = window
        self._index = indexes

        self.h2hVM = h2hTableViewModel(self._h2h_data, self._h2h_header)     
        self._window.h2hTableView.setModel(self.h2hVM)

        self.statsVM = {}
        self.tabCounter = 0
        for ii in self._stats_years:
            self.statsVM[ii] = statsTableViewModel(self._stats_data[ii], self._stats_header)
            self._window.tabWidget.widget(self.tabCounter).setModel(self.statsVM[ii])
            self.tabCounter = self.tabCounter +1

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

    # ------------------------------------------------------ editing 'Date' cell -----------------------------------------------------------------
        if index.column() == self._index.date: # when editing 'Date' cell
            try:
                dt_value = dt.strptime(value, '%d.%m.%Y').date()
            except:
                value = ''
                self._window.debugText.insertPlainText('Invalid datetime format. Please input date using the dd.mm.yyyy format \n')


            if self._data[index.row(), index.column()] == value: # when cell value doesn't change
                self._window.debugText.insertPlainText('Date cell value did not change. \n')
            elif (self._data[index.row(), index.column()] == None or self._data[index.row(), index.column()] == np.array([''])) and \
                    (value != None and value != np.array([''])): # when empty cell is edited with non-empty value

                if value[-4:] in self._stats_years: # if year in stats_years, update fields of corresponding tab
                    test=1
                else: # if year not in stats_years, add a new tab and initialize VM and update fields
                    self._stats_years = np.append(self._stats_years, value[-4:])
                    self._stats_data[self._stats_years[-1]] = np.empty(shape=(self._stats_header.size, 1), dtype='U64')

                    newTab = QTableView()
                    self._window.tabWidget.addTab(newTab, self._stats_years[-1])
                    self.statsVM[self._stats_years[-1]] = statsTableViewModel(self._stats_data[self._stats_years[-1]], self._stats_header)
                    print(self._stats_years.size)
                    self._window.tabWidget.widget(self._stats_years.size-1).setModel(self.statsVM[self._stats_years[-1]]) #end VM initialization



            print(value[-4:])     
            test=1

    # ------------------------------------------------------ editing 'Opponent' cell -------------------------------------------------------------
        elif index.column() == self._index.op: # when editing 'Opponent' cell
            if self._data[index.row(), index.column()] == value: # when cell value did not change
                self._window.debugText.insertPlainText('Cell value remained the same.\n')
            elif (self._data[index.row(), index.column()] == None or self._data[index.row(), index.column()] == np.array([''])) and \
                    (value != None and value != np.array([''])): # when empty cell is edited with non-empty value
                # h2h -----------------------------------------------------
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

                index_h2h_op = np.where(self.h2hVM._data[:, self._index.h2h_op] == self._data[index.row(), index.column()]) 
                index_h2h_op_new = np.where(self.h2hVM._data[:, self._index.h2h_op] == value)
                
                if index_h2h_op_new[0].size == 0:
                    st.h2h_result_remove(self._data,  self.h2hVM._data, index_h2h_op[0], self._index, index)
                    refresh.h2h_score(self.h2hVM, self._h2h_data.shape[0]-1, self._index)

                    st.h2h_result_first(self._data, self.h2hVM._data, index_h2h_op_new[0], self._index, index, value)
                    refresh.h2h_score(self.h2hVM, self._h2h_data.shape[0]-1, self._index)
                    refresh.h2h_opponent(self.h2hVM, self._h2h_data.shape[0]-1, self._index)

                    self.h2hVM._data = np.vstack((self.h2hVM._data, np.empty(shape=(1, self._h2h_data.shape[1]), dtype='U64')))
                    self.h2hVM.layoutChanged.emit() 

                else:
                    st.h2h_result_remove(self._data,  self.h2hVM._data, index_h2h_op[0], self._index, index)
                    refresh.h2h_score(self.h2hVM, index_h2h_op[0], self._index)

                    st.h2h_result_update(self._data, self.h2hVM._data, index_h2h_op_new[0], self._index, index)
                    refresh.h2h_score(self.h2hVM, index_h2h_op_new[0], self._index)
                    test=1

            elif (self._data[index.row(), index.column()] != None or self._data[index.row(), index.column()] != np.array([''])) and \
                 (value == None and value == np.array([''])): # when name in cell is deleted

                st.h2h_sets(self._data, self._index, index, self._window)
                index_h2h_op = np.where(self.h2hVM._data[:, self._index.h2h_op] == self._data[index.row(), index.column()])

                st.h2h_result_remove(self._data,  self.h2hVM._data, index_h2h_op[0], self._index, index)
                refresh.h2h_score(self.h2hVM, index_h2h_op[0], self._index)

    #--------------------------------------------------- editing 'SetN' cell ---------------------------------------------------------------------
        elif index.column() == self._index.set1 or index.column() == self._index.set2 or index.column() == self._index.set3:
            st.h2h_sets(self._data, self._index, index, self._window)
            self._data[index.row(), index.column()] = str(value)
            st.h2h_sets_update(self._data, self._index, index, self._window)

            ### h2h table
            index_h2h_op = np.where(self.h2hVM._data[:, self._index.h2h_op] == self._data[index.row(), self._index.op])
            if index_h2h_op[0].size == 0:
                st.h2h_result_first(self._data, self.h2hVM._data, index_h2h_op[0], self._index, index, self._data[index.row(), self._index.op])
                refresh.h2h_score(self.h2hVM, self._h2h_data.shape[0]-1, self._index)
                refresh.h2h_opponent(self.h2hVM, self._h2h_data.shape[0]-1, self._index)

                self.h2hVM._data = np.vstack((self.h2hVM._data, np.empty(shape=(1, self._h2h_data.shape[1]), dtype='U64')))
                self.h2hVM.layoutChanged.emit()   

            else:
                if st.sets_won != st.sets_won_new or st.sets_lost != st.sets_lost_new: # if sets won or lost changed
                    if self._data[index.row(), self._index.op] == None or self._data[index.row(), self._index.op] == np.array(['']): # check if name empty
                        self._window.debugText.insertPlainText('Please input opponent name! \n')
                    else:
                        st.h2h_compare_results(self._data, self.h2hVM._data, index_h2h_op[0], self._index, index, self._window)

                refresh.h2h_score(self.h2hVM, index_h2h_op[0], self._index)

            ### stats table
            if st.sets_won != st.sets_won_new or st.sets_lost != st.sets_lost_new: # if sets won or lost changed
                if self._stats_data['All Time'][0] == '':
                    refresh.stats_tab_init(self.statsVM['All Time'], self._stats_header)
                else:
                    st.stats_compare_results(self._data, self._stats_data, self._stats_header, self._stats_years, self._index, index, self._window)
                    for tab_name in self._stats_years:
                        refresh.stats_tab(self.statsVM[tab_name], self._stats_header)

    #------------------------------------------------ refresh tables after editing ----------------------------------------------------------------
        try: # in case h2h is 0-0 remove the opponent from h2h_table 
            if self.h2hVM._data[index_h2h_op, self._index.h2h_won][0] == '0' and self.h2hVM._data[index_h2h_op, self._index.h2h_lost][0] == '0':
                self.h2hVM._data = np.delete(self.h2hVM._data, index_h2h_op, 0)
                self.h2hVM.layoutChanged.emit() 
        except:
            test=2
            #self._window.debugText.insertPlainText('No opponent was removed from h2h table \n')

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


