from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtWidgets import QTableView
import numpy as np
from datetime import datetime as dt

from h2hTableViewModel import h2hTableViewModel
from statsTableViewModel import statsTableViewModel

from statistics import statistics as st
from tools import tools
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

    ##############################################################################################################################################
    # ------------------------------------------------------ editing 'Date' cell -----------------------------------------------------------------
    ##############################################################################################################################################
        self._window.debugText.clear()
        if index.column() == self._index.date: # when editing 'Date' cell
            try:
                dt_value = dt.strptime(value, '%d.%m.%Y').date()
                if self._data[index.row(), index.column()] == value: # when cell value doesn't change
                    self._window.debugText.insertPlainText('Date cell value did not change. \n')
                else:
                    if self._data[index.row(), self._index.date] != '': # if last iteration of that year, remove the corresponding tab from stats table
                        cnt_date = -1
                        for date_row in range(0, self._data[:, self._index.date].size):
                            if self._data[index.row(), self._index.date][-4:] == self._data[date_row, self._index.date][-4:]:
                                cnt_date = cnt_date +1

                        if cnt_date == 0:
                            temp_years = self._stats_years[1:]
                            temp_years = np.sort(temp_years)
                            pos = int(np.where(temp_years == self._data[index.row(), self._index.date][-4:])[0][0]) 

                            self._stats_years = np.setdiff1d(self._stats_years, temp_years[pos], True)
                            self._window.tabWidget.removeTab(pos+1)
                            self.statsVM.pop(self._data[index.row(), self._index.date][-4:])

                    if (value[-4:] not in self._stats_years) and value != '': # if year not in stats_years, add a new tab and initialize VM and update fields
                        self._stats_years = np.append(self._stats_years, value[-4:])
                        self._stats_data[self._stats_years[-1]] = np.array([['0-0'], ['0-0'], ['0-0'], ['0-0']], dtype='U64')

                        temp_years = self._stats_years[1:]
                        temp_years = np.sort(temp_years)
                        pos = int(np.where(temp_years == value[-4:])[0][0]) 

                        newTab = QTableView()
                        self._window.tabWidget.insertTab(pos+1, newTab, temp_years[pos])
                        self.statsVM[self._stats_years[-1]] = statsTableViewModel(self._stats_data[self._stats_years[-1]], self._stats_header)
                        self._window.tabWidget.widget(pos+1).setModel(self.statsVM[self._stats_years[-1]]) #end VM initialization

                    st.stats_date_update(self._data, self._stats_data, self._stats_header, self._data[index.row(), self._index.date][-4:], value[-4:], self._index, index)
                    refresh.stats_tab(self.statsVM[value[-4:]], self._stats_header)

                         
            except:
                if value != '' or (self._data[index.row(), index.column()] == '' and value == ''):
                    value = self._data[index.row(), index.column()]
                    self._window.debugText.insertPlainText('Invalid datetime format. Please input date using the dd.mm.yyyy format \n')
                else:
                    st.stats_date_update(self._data, self._stats_data, self._stats_header, self._data[index.row(), self._index.date][-4:], value[-4:], self._index, index)
                    refresh.stats_tab(self.statsVM[value[-4:]], self._stats_header)

                self._window.debugText.insertPlainText('Invalid datetime format. Please input date using the dd.mm.yyyy format \n')

    ##############################################################################################################################################
    # ------------------------------------------------------ editing 'Opponent' cell -------------------------------------------------------------
    ##############################################################################################################################################
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
                    self.h2hVM._data = tools.sort_h2h(self.h2hVM._data, self._index) # sort h2h table by name
                    index_h2h_op = np.where(self.h2hVM._data[:, self._index.h2h_op] == value) # recalculate because index changed in previous line
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
                    self.h2hVM._data = tools.sort_h2h(self.h2hVM._data, self._index) # sort h2h table by name
                    index_h2h_op = np.where(self.h2hVM._data[:, self._index.h2h_op] == self._data[index.row(), index.column()]) # recalculate because index changed in previous line
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

    ##############################################################################################################################################
    #--------------------------------------------------- editing 'Result' cell ---------------------------------------------------------------------
    ##############################################################################################################################################
        elif index.column() == self._index.res: # when editing 'Result' cell
            value = self._data[index.row(), index.column()] # makes it impossible to edit the 'Result' field (this field is generated automatically)
            self._window.debugText.insertPlainText('Do not edit the \'Result\' field! \n')

    ##############################################################################################################################################
    #--------------------------------------------------- editing 'SetN' cell ---------------------------------------------------------------------
    ##############################################################################################################################################
        elif index.column() == self._index.set1 or index.column() == self._index.set2 or index.column() == self._index.set3:
            st.h2h_sets(self._data, self._index, index, self._window)
            self._data[index.row(), index.column()] = str(value)
            st.h2h_sets_update(self._data, self._index, index, self._window)
            if st.valid_input == False:
                value = ''

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
                for year in self._stats_years:
                    if year == 'All Time' or year == self._data[index.row(), self._index.date][-4:]:
                        st.stats_compare_results(self._data, self._stats_data[year], self._stats_header, self._stats_years, self._index, index, self._window)
                        refresh.stats_tab(self.statsVM[year], self._stats_header)

    #############################################################################################################################################################
    #------------------------------------------------ editing 'Surface' cell ------------------------------------------------------------------------------------
    #############################################################################################################################################################
        elif index.column() == self._index.surf:
            st.stats_surface_update(self._data, value, self._stats_data['All Time'], self._stats_header, self._stats_years, index, self._index, self._window)
            refresh.stats_tab(self.statsVM['All Time'], self._stats_header)
            try:
                dt_value = dt.strptime(self._data[index.row(), self._index.date], '%d.%m.%Y').date()
                st.stats_surface_update(self._data, value, self._stats_data[self._data[index.row(), self._index.date][-4:]], self._stats_header, self._stats_years, index, self._index, self._window)
                refresh.stats_tab(self.statsVM[self._data[index.row(), self._index.date][-4:]], self._stats_header)
            except:
                test=1

    #------------------------------------------------ refresh h2h tables after editing ----------------------------------------------------------------
        self._data[index.row(), index.column()] = str(value)   

        try: # in case h2h is 0-0 and opponent not in data anymore, remove the opponent from h2h_table 
            print(self.h2hVM._data[index_h2h_op, self._index.h2h_op], self._data[:, self._index.op])
            if self.h2hVM._data[index_h2h_op, self._index.h2h_op][0] not in self._data[:, self._index.op]:
                if (self.h2hVM._data[index_h2h_op, self._index.h2h_won][0] == '0' and self.h2hVM._data[index_h2h_op, self._index.h2h_lost][0] == '0') or \
                    (self.h2hVM._data[index_h2h_op, self._index.h2h_won][0] == '1' and self.h2hVM._data[index_h2h_op, self._index.h2h_lost][0] == '0') or \
                    (self.h2hVM._data[index_h2h_op, self._index.h2h_won][0] == '0' and self.h2hVM._data[index_h2h_op, self._index.h2h_lost][0] == '1'):
                    self.h2hVM._data = np.delete(self.h2hVM._data, index_h2h_op, 0)
                    self.h2hVM.layoutChanged.emit() 
        except:
            test=2


        ### sorting data table by date
        if '' not in self._data[:, self._index.date]:
            self._data = tools.sort_date(self._data, self._index)

        self.dataChanged.emit(index, index, (Qt.DisplayRole, ))

        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            header = self._header[section]
            return str(header)
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            header = section
            return str(header)


