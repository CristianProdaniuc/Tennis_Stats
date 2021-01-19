import numpy as np

class statistics(object):
    
    #---------------------------------- h2h Table Stats Functions -----------------------------------------------------------------------------------------------
    def h2h_sets(data, index, index_table, window):

        statistics.sets_won = 0
        statistics.sets_lost = 0

        for col in range(index.set1, index.set1 +3):
            lindex = data[index_table.row(), col].find('-')
            if lindex == -1 and col < index.set3:
                window.debugText.insertPlainText('Invalid score or empty cell for sets 1 and/or 2. Please input the score in the following format: \'X-Y\'\n')
                data[index_table.row(), index.res] = 'NA'
                break
            elif lindex == -1 and col >= index.set3:
                break
            elif data[index_table.row(), col][-2:] == 'ab':
                statistics.sets_won = 10
            elif int(data[index_table.row(), col][0:lindex]) > int(data[index_table.row(), col][lindex+1:]) and \
                    int(data[index_table.row(), col][0:lindex]) > 5:
                statistics.sets_won += 1
            elif int(data[index_table.row(), col][0:lindex]) < int(data[index_table.row(), col][lindex+1:]) and \
                    int(data[index_table.row(), col][lindex+1:]) > 5:
                statistics.sets_lost += 1

    def h2h_sets_update(data, index, index_table, window):
        statistics.sets_won_new = 0
        statistics.sets_lost_new = 0

        for col in range(index.set1, index.set1 +3):
            lindex = data[index_table.row(), col].find('-')
            if lindex == -1 and col < index.set3:
                window.debugText.insertPlainText('Invalid score or empty cell for sets 1 and/or 2. Please input the score in the following format: \'X-Y\'\n')
                data[index_table.row(), index.res] = 'NA'
                break
            elif lindex == -1 and col >= index.set3:
                break
            elif data[index_table.row(), col][-2:] == 'ab':
                statistics.sets_won_new = 10
            elif int(data[index_table.row(), col][0:lindex]) > int(data[index_table.row(), col][lindex+1:]) and \
                  int(data[index_table.row(), col][0:lindex]) > 5:
                statistics.sets_won_new += 1
            elif int(data[index_table.row(), col][0:lindex]) < int(data[index_table.row(), col][lindex+1:]) and \
                  int(data[index_table.row(), col][lindex+1:]) > 5:
                statistics.sets_lost_new += 1

    def h2h_compare_results(data, h2h_data, index_op, index, index_table, window):  

        if statistics.sets_lost > statistics.sets_won and statistics.sets_lost > 1: # old lost
            if statistics.sets_lost_new > statistics.sets_won_new and statistics.sets_lost_new > 1: # still a loss
                window.debugText.insertPlainText('Match outcome remains the same \n')
            elif statistics.sets_lost_new < statistics.sets_won_new and statistics.sets_won_new > 1: # win
                h2h_data[index_op, index.h2h_won] = \
                    np.array( [int(h2h_data[index_op, index.h2h_won]) +1], dtype='U64')[0]
                h2h_data[index_op, index.h2h_lost] = \
                    np.array( [int(h2h_data[index_op, index.h2h_lost]) -1], dtype='U64')[0]
                data[index_table.row(), index.res] = 'W'
            else: # NA
                h2h_data[index_op, index.h2h_lost] = \
                    np.array( [int(h2h_data[index_op, index.h2h_lost]) -1], dtype='U64')[0]
                data[index_table.row(), index.res] = 'NA'

        elif statistics.sets_lost < statistics.sets_won and statistics.sets_won > 1: # old win
            if statistics.sets_lost_new > statistics.sets_won_new and statistics.sets_lost_new > 1: # loss
                h2h_data[index_op, index.h2h_won] = \
                    np.array( [int(h2h_data[index_op, index.h2h_won]) -1], dtype='U64')[0]
                h2h_data[index_op, index.h2h_lost] = \
                    np.array( [int(h2h_data[index_op, index.h2h_lost]) +1], dtype='U64')[0]
                data[index_table.row(), index.res] = 'L'
            elif statistics.sets_lost_new < statistics.sets_won_new and statistics.sets_won_new > 1: # still a win
                window.debugText.insertPlainText('Match outcome remains the same \n')
            else: # NA
                h2h_data[index_op, index.h2h_win] = \
                    np.array( [int(h2h_data[index_op, index.h2h_win]) -1], dtype='U64')[0]
                data[index_table.row(), index.res] = 'NA'

        else: # old NA
            if statistics.sets_lost_new > statistics.sets_won_new and statistics.sets_lost_new > 1: # loss
                h2h_data[index_op, index.h2h_lost] = \
                    np.array( [int(h2h_data[index_op, index.h2h_lost]) +1], dtype='U64')[0]
                data[index_table.row(), index.res] = 'L'
            elif statistics.sets_lost_new < statistics.sets_won_new and statistics.sets_won_new > 1: # win
                h2h_data[index_op, index.h2h_won] = \
                    np.array( [int(h2h_data[index_op, index.h2h_won]) +1], dtype='U64')[0]
                data[index_table.row(), index.res] = 'W'
            else: # still NA
                window.debugText.insertPlainText('Match outcome remains the same \n')

    def h2h_result_first(data, h2h_data, index_op, index, index_table, value):
        if statistics.sets_won > statistics.sets_lost and statistics.sets_won > 1:
            h2h_data[-1, index.h2h_op] = str(value)
            h2h_data[-1, index.h2h_won] = 1
            h2h_data[-1, index.h2h_lost] = 0
            data[index_table.row(), index.res] = 'W'
        elif statistics.sets_won < statistics.sets_lost and statistics.sets_lost > 1:
            h2h_data[-1, index.h2h_op] = str(value)
            h2h_data[-1, index.h2h_won] = 0
            h2h_data[-1, index.h2h_lost] = 1
            data[index_table.row(), index.res] = 'L'
        else:
            h2h_data[-1, index.h2h_op] = str(value)
            h2h_data[-1, index.h2h_won] = 0
            h2h_data[-1, index.h2h_lost] = 0
            data[index_table.row(), 2] = 'NA'

    def h2h_result_update(data, h2h_data, index_op, index, index_table):
        if statistics.sets_won > statistics.sets_lost and statistics.sets_won > 1:
            h2h_data[index_op, index.h2h_won] = \
                np.array( [int(h2h_data[index_op, index.h2h_won]) +1], dtype='U64')[0]
            data[index_table.row(), index.res] = 'W'
        elif statistics.sets_won < statistics.sets_lost and statistics.sets_lost > 1:
            h2h_data[index_op, index.h2h_lost] = \
                np.array( [int(h2h_data[index_op, index.h2h_lost]) +1], dtype='U64')[0]
            data[index_table.row(), index.res] = 'L'
        else:
            data[index_table.row(), 2] = 'NA'

    def h2h_result_remove(data, h2h_data, index_op, index, index_table):
        if statistics.sets_won > statistics.sets_lost and statistics.sets_won > 1:
             h2h_data[index_op, index.h2h_won] = \
                np.array( [int(h2h_data[index_op, index.h2h_won]) -1], dtype='U64')[0]
        elif statistics.sets_won < statistics.sets_lost and statistics.sets_lost > 1:
            h2h_data[index_op, index.h2h_lost] = \
                np.array( [int(h2h_data[index_op, index.h2h_lost]) -1], dtype='U64')[0]

    #------------------------------------------ Stats Table Functions ------------------------------------------------------------------------        
    def init_stats(stats_data):
        for ii in range(0, stats_data['All Time'].size):#delete
            stats_data['All Time'][ii] = '0-0' # initialize 

    def stats_compare_results(data, stats_data, stats_header, stats_years, index, index_table, window):

        if statistics.sets_lost > statistics.sets_won and statistics.sets_lost > 1: # old loss
            if statistics.sets_lost_new > statistics.sets_won_new and statistics.sets_lost_new > 1: # still a loss
                window.debugText.insertPlainText('No stats change \n')
            elif statistics.sets_lost_new < statistics.sets_won_new and statistics.sets_won_new > 1: # win
                for ii in range(0, stats_data.size):
                    if stats_header[ii] == 'Overall':
                        statistics.getWL(stats_data, ii)
                        statistics.L2W(stats_data, statistics.W, statistics.L, ii)
                    elif stats_header[ii] == 'Clay' and data[index_table.row(), index.surf] == 'clay':
                        statistics.getWL(stats_data, ii)
                        statistics.L2W(stats_data, statistics.W, statistics.L, ii)
            else: # NA
                for ii in range(0, stats_data.size):
                    if stats_header[ii] == 'Overall':
                        statistics.getWL(stats_data, ii)
                        statistics.L2NA(stats_data, statistics.W, statistics.L, ii)
                    elif stats_header[ii] == 'Clay' and data[index_table.row(), index.surf] == 'clay':
                        statistics.getWL(stats_data, ii)
                        statistics.L2NA(stats_data, statistics.W, statistics.L, ii)
        elif statistics.sets_lost < statistics.sets_won and statistics.sets_won > 1: # old win
            if statistics.sets_lost_new > statistics.sets_won_new and statistics.sets_lost_new > 1: # loss
                for ii in range(0, stats_data.size):
                    if stats_header[ii] == 'Overall':
                        statistics.getWL(stats_data, ii)
                        statistics.W2L(stats_data, statistics.W, statistics.L, ii)
                    elif stats_header[ii] == 'Clay' and data[index_table.row(), index.surf] == 'clay':
                        statistics.getWL(stats_data, ii)
                        statistics.W2L(stats_data, statistics.W, statistics.L, ii)
            elif statistics.sets_lost_new < statistics.sets_won_new and statistics.sets_won_new > 1: # win
                window.debugText.insertPlainText('No stats change \n')
            else: # NA
                for ii in range(0, stats_data.size):
                    if stats_header[ii] == 'Overall':
                        statistics.getWL(stats_data, ii)
                        statistics.W2NA(stats_data, statistics.W, statistics.L, ii)
                    elif stats_header[ii] == 'Clay' and data[index_table.row(), index.surf] == 'clay':
                        statistics.getWL(stats_data, ii)
                        statistics.W2NA(stats_data, statistics.W, statistics.L, ii)
        else: # old NA 
            if statistics.sets_lost_new > statistics.sets_won_new and statistics.sets_lost_new > 1: # loss
                for ii in range(0, stats_data.size):
                    if stats_header[ii] == 'Overall':
                        statistics.getWL(stats_data, ii)
                        statistics.NA2L(stats_data, statistics.W, statistics.L, ii)
                    elif stats_header[ii] == 'Clay' and data[index_table.row(), index.surf] == 'clay':
                        statistics.getWL(stats_data, ii)
                        statistics.NA2L(stats_data, statistics.W, statistics.L, ii)
            elif statistics.sets_lost_new < statistics.sets_won_new and statistics.sets_won_new > 1: # win
                for ii in range(0, stats_data.size):
                    if stats_header[ii] == 'Overall':
                        statistics.getWL(stats_data, ii)
                        statistics.NA2W(stats_data, statistics.W, statistics.L, ii)
                    elif stats_header[ii] == 'Clay' and data[index_table.row(), index.surf] == 'clay':
                        statistics.getWL(stats_data, ii)
                        statistics.NA2W(stats_data, statistics.W, statistics.L, ii)
            else: # NA
                window.debugText.insertPlainText('No stats change \n')

    def getWL(stats_data, index):
        index_line = np.char.find(stats_data[index], '-')[0]
        statistics.W = int(stats_data[index][0][0:index_line])
        statistics.L = int(stats_data[index][0][index_line+1:])

    def NA2L(stats_data, W, L, index):
        L = L +1
        stats_data[index][0] = np.array([str(W) + '-' + str(L)], dtype = 'U64')[0]

    def NA2W(stats_data, W, L, index):
        W = W +1
        stats_data[index][0] = np.array([str(W) + '-' + str(L)], dtype = 'U64')[0]

    def W2L(stats_data, W, L, index):
        W = W -1
        L = L +1
        stats_data[index][0] = np.array([str(W) + '-' + str(L)], dtype = 'U64')[0]

    def W2NA(stats_data, W, L, index):
        W = W -1
        stats_data[index][0] = np.array([str(W) + '-' + str(L)], dtype = 'U64')[0]

    def L2NA(stats_data, W, L, index):
        L = L -1
        stats_data[index][0] = np.array([str(W) + '-' + str(L)], dtype = 'U64')[0]

    def L2W(stats_data, W, L, index):
        W = W +1
        L = L -1
        stats_data[index][0] = np.array([str(W) + '-' + str(L)], dtype = 'U64')[0]