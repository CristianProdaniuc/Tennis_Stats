import numpy as np

class statistics(object):
    ##############################################################################################################################################################
    #---------------------------------- h2h Table Stats Functions -----------------------------------------------------------------------------------------------#
    ##############################################################################################################################################################

    def h2h_sets(data, index, index_data, window):

        statistics.sets_won = 0
        statistics.sets_lost = 0

        for col in range(index.set1, index.set1 +3):
            lindex = data[index_data.row(), col].find('-')
            if lindex == -1 and col < index.set3:
                data[index_data.row(), index.res] = 'NA'
                break
            elif lindex == -1 and col >= index.set3:
                break
            elif data[index_data.row(), col][-2:] == 'ab':
                statistics.sets_won = 10
            elif int(data[index_data.row(), col][0:lindex]) > int(data[index_data.row(), col][lindex+1:]) and \
                    int(data[index_data.row(), col][0:lindex]) > 5:
                statistics.sets_won += 1
            elif int(data[index_data.row(), col][0:lindex]) < int(data[index_data.row(), col][lindex+1:]) and \
                    int(data[index_data.row(), col][lindex+1:]) > 5:
                statistics.sets_lost += 1               

    def h2h_sets_update(data, index, index_data, window):
        statistics.sets_won_new = 0
        statistics.sets_lost_new = 0
        statistics.valid_input = True

        for col in range(index.set1, index.set1 +3):
            lindex = data[index_data.row(), col].find('-')
            if lindex == -1 and col < index.set3:
                window.debugText.insertPlainText('Invalid score or empty cell for sets 1 and/or 2. Please input the score in the following format: \'X-Y\'\n')
                if col == index_data.column():
                    statistics.valid_input = False
                    data[index_data.row(), index.res] = 'NA'

                break
            elif lindex == -1 and col >= index.set3:
                break
            elif data[index_data.row(), col][-2:] == 'ab':
                statistics.sets_won_new = 10
            elif data[index_data.row(), col][0:lindex].isdigit() != True or data[index_data.row(), col][lindex+1:].isdigit() != True:
                window.debugText.insertPlainText('Invalid score - Please re-enter the score in the following format: \'X-Y\'\n')
                statistics.valid_input = False
                data[index_data.row(), index.res] = 'NA'
                break
            elif int(data[index_data.row(), col][0:lindex]) > int(data[index_data.row(), col][lindex+1:]) and \
                  int(data[index_data.row(), col][0:lindex]) > 5:
                statistics.sets_won_new += 1
            elif int(data[index_data.row(), col][0:lindex]) < int(data[index_data.row(), col][lindex+1:]) and \
                  int(data[index_data.row(), col][lindex+1:]) > 5:
                statistics.sets_lost_new += 1
            elif int(data[index_data.row(), col][0:lindex]) < 6 and int(data[index_data.row(), col][lindex+1:]) < 6:
                window.debugText.insertPlainText('Invalid score, either the number of games lost or won must be at least 6. Input the score again. \n')
                statistics.valid_input = False
                data[index_data.row(), index.res] = 'NA'
                break 

    def h2h_compare_results(data, h2h_data, index_op, index, index_data, window):  

        if statistics.sets_lost > statistics.sets_won and statistics.sets_lost > 1: # old lost
            if statistics.sets_lost_new > statistics.sets_won_new and statistics.sets_lost_new > 1: # still a loss
                window.debugText.insertPlainText('Match outcome remains the same \n')
            elif statistics.sets_lost_new < statistics.sets_won_new and statistics.sets_won_new > 1: # win
                h2h_data[index_op, index.h2h_won] = np.array( [int(h2h_data[index_op, index.h2h_won]) +1], dtype='U64')[0]
                h2h_data[index_op, index.h2h_lost] = np.array( [int(h2h_data[index_op, index.h2h_lost]) -1], dtype='U64')[0]
                data[index_data.row(), index.res] = 'W'
            else: # NA
                h2h_data[index_op, index.h2h_lost] = np.array( [int(h2h_data[index_op, index.h2h_lost]) -1], dtype='U64')[0]
                h2h_data[index_op, index.h2h_matches] = np.array( [int(h2h_data[index_op, index.h2h_matches]) -1], dtype='U64')[0]
                data[index_data.row(), index.res] = 'NA'

        elif statistics.sets_lost < statistics.sets_won and statistics.sets_won > 1: # old win
            if statistics.sets_lost_new > statistics.sets_won_new and statistics.sets_lost_new > 1: # loss
                h2h_data[index_op, index.h2h_won] = np.array( [int(h2h_data[index_op, index.h2h_won]) -1], dtype='U64')[0]
                h2h_data[index_op, index.h2h_lost] = np.array( [int(h2h_data[index_op, index.h2h_lost]) +1], dtype='U64')[0]
                data[index_data.row(), index.res] = 'L'
            elif statistics.sets_lost_new < statistics.sets_won_new and statistics.sets_won_new > 1: # still a win
                window.debugText.insertPlainText('Match outcome remains the same \n')
            else: # NA
                h2h_data[index_op, index.h2h_won] = np.array( [int(h2h_data[index_op, index.h2h_won]) -1], dtype='U64')[0]
                h2h_data[index_op, index.h2h_matches] = np.array( [int(h2h_data[index_op, index.h2h_matches]) -1], dtype='U64')[0]
                data[index_data.row(), index.res] = 'NA'

        else: # old NA
            if statistics.sets_lost_new > statistics.sets_won_new and statistics.sets_lost_new > 1: # loss
                h2h_data[index_op, index.h2h_lost] = np.array( [int(h2h_data[index_op, index.h2h_lost]) +1], dtype='U64')[0]
                h2h_data[index_op, index.h2h_matches] = np.array( [int(h2h_data[index_op, index.h2h_matches]) +1], dtype='U64')[0]
                data[index_data.row(), index.res] = 'L'
            elif statistics.sets_lost_new < statistics.sets_won_new and statistics.sets_won_new > 1: # win
                h2h_data[index_op, index.h2h_won] = np.array( [int(h2h_data[index_op, index.h2h_won]) +1], dtype='U64')[0]
                h2h_data[index_op, index.h2h_matches] = np.array( [int(h2h_data[index_op, index.h2h_matches]) +1], dtype='U64')[0]
                data[index_data.row(), index.res] = 'W'
            else: # still NA
                window.debugText.insertPlainText('Match outcome remains the same \n')

    def h2h_result_first(data, h2h_data, index_op, index, index_data, value):
        if statistics.sets_won > statistics.sets_lost and statistics.sets_won > 1:
            h2h_data[-1, index.h2h_op] = str(value)
            h2h_data[-1, index.h2h_won] = 1
            h2h_data[-1, index.h2h_lost] = 0
            h2h_data[-1, index.h2h_matches] = 1
            data[index_data.row(), index.res] = 'W'
        elif statistics.sets_won < statistics.sets_lost and statistics.sets_lost > 1:
            h2h_data[-1, index.h2h_op] = str(value)
            h2h_data[-1, index.h2h_won] = 0
            h2h_data[-1, index.h2h_lost] = 1
            h2h_data[-1, index.h2h_matches] = 1
            data[index_data.row(), index.res] = 'L'
        else:
            h2h_data[-1, index.h2h_op] = str(value)
            h2h_data[-1, index.h2h_won] = 0
            h2h_data[-1, index.h2h_lost] = 0
            h2h_data[-1, index.h2h_matches] = 0
            data[index_data.row(), 2] = 'NA'

    def h2h_result_update(data, h2h_data, index_op, index, index_data):
        if statistics.sets_won > statistics.sets_lost and statistics.sets_won > 1:
            h2h_data[index_op, index.h2h_won] = np.array( [int(h2h_data[index_op, index.h2h_won]) +1], dtype='U64')[0]
            h2h_data[index_op, index.h2h_matches] = np.array( [int(h2h_data[index_op, index.h2h_matches]) +1], dtype='U64')[0]
            data[index_data.row(), index.res] = 'W'
        elif statistics.sets_won < statistics.sets_lost and statistics.sets_lost > 1:
            h2h_data[index_op, index.h2h_lost] = np.array( [int(h2h_data[index_op, index.h2h_lost]) +1], dtype='U64')[0]
            h2h_data[index_op, index.h2h_matches] = np.array( [int(h2h_data[index_op, index.h2h_matches]) +1], dtype='U64')[0]
            data[index_data.row(), index.res] = 'L'
        else:
            data[index_data.row(), 2] = 'NA'

    def h2h_result_remove(data, h2h_data, index_op, index, index_data):
        if statistics.sets_won > statistics.sets_lost and statistics.sets_won > 1:
             h2h_data[index_op, index.h2h_won] = np.array( [int(h2h_data[index_op, index.h2h_won]) -1], dtype='U64')[0]
             h2h_data[index_op, index.h2h_matches] = np.array( [int(h2h_data[index_op, index.h2h_matches]) -1], dtype='U64')[0]
        elif statistics.sets_won < statistics.sets_lost and statistics.sets_lost > 1:
            h2h_data[index_op, index.h2h_lost] = np.array( [int(h2h_data[index_op, index.h2h_lost]) -1], dtype='U64')[0]
            h2h_data[index_op, index.h2h_matches] = np.array( [int(h2h_data[index_op, index.h2h_matches]) -1], dtype='U64')[0]

    ###########################################################################################################################################
    #------------------------------------------ Stats Table Functions ------------------------------------------------------------------------#
    ###########################################################################################################################################   
         
    def init_stats(stats_data):
        for ii in range(0, stats_data['All Time'].size):#delete
            stats_data['All Time'][ii] = '0-0' # initialize 

    def stats_compare_results(data, stats_data, stats_header, stats_years, index, index_data, window):
        for ii in range(0, stats_data.size):
            if stats_header[ii] == 'Overall':
                statistics.WLupdate(stats_data, ii, index, index_data, window)
                statistics.stats_result_update(data, index, index_data)
            elif stats_header[ii] == 'Clay' and data[index_data.row(), index.surf] == 'clay':
                statistics.WLupdate(stats_data, ii, index, index_data, window)
            elif stats_header[ii] == 'Hard' and data[index_data.row(), index.surf] == 'hard':
                statistics.WLupdate(stats_data, ii, index, index_data, window)
            elif stats_header[ii] == 'Tartan' and data[index_data.row(), index.surf] == 'tartan':
                statistics.WLupdate(stats_data, ii, index, index_data, window)
            elif stats_header[ii] == 'Tournament' and data[index_data.row(), index.type] == 'O':
                statistics.WLupdate(stats_data, ii, index, index_data, window)
            elif stats_header[ii] == 'Quarter-Final' and data[index_data.row(), index.round] == 'QF':
                statistics.WLupdate(stats_data, ii, index, index_data, window)
            elif stats_header[ii] == 'Semi-Final' and data[index_data.row(), index.round] == 'SF':
                statistics.WLupdate(stats_data, ii, index, index_data, window)
            elif stats_header[ii] == 'Final' and data[index_data.row(), index.round] == 'F':
                statistics.WLupdate(stats_data, ii, index, index_data, window)

    def stats_date_update(data, stats_data, stats_header, old_year, new_year, index, index_data):
        for ii in range(0,stats_data['All Time'].size):
            if stats_header[ii] == 'Overall':
                statistics.WLupdate_by_result(data, stats_data, old_year, new_year, ii, index, index_data)
            elif stats_header[ii] == 'Clay' and data[index_data.row(), index.surf] == 'clay':
                statistics.WLupdate_by_result(data, stats_data, old_year, new_year, ii, index, index_data)
            elif stats_header[ii] == 'Hard' and data[index_data.row(), index.surf] == 'hard':
                statistics.WLupdate_by_result(data, stats_data, old_year, new_year, ii, index, index_data)
            elif stats_header[ii] == 'Tartan' and data[index_data.row(), index.surf] == 'tartan':
                statistics.WLupdate_by_result(data, stats_data, old_year, new_year, ii, index, index_data)
            elif stats_header[ii] == 'Tournament' and data[index_data.row(), index.type] == 'O':
                statistics.WLupdate_by_result(data, stats_data, old_year, new_year, ii, index, index_data)
            elif stats_header[ii] == 'Quarter-Final' and data[index_data.row(), index.round] == 'QF':
                statistics.WLupdate_by_result(data, stats_data, old_year, new_year, ii, index, index_data)
            elif stats_header[ii] == 'Semi-Final' and data[index_data.row(), index.round] == 'SF':
                statistics.WLupdate_by_result(data, stats_data, old_year, new_year, ii, index, index_data)
            elif stats_header[ii] == 'Final' and data[index_data.row(), index.round] == 'F':
                statistics.WLupdate_by_result(data, stats_data, old_year, new_year, ii, index, index_data)

    def stats_tournament_update(data, value, stats_data, stats_header, stats_years, index, index_data, window):
        ### old Oficial
        if data[index_data.row(), index.type] == 'O':
            if value == 'O':
                window.debugText.insertPlainText('Match type did not change \n')
            else:
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_tour)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_tour)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_tour)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_tour)
        ### old Friendly
        elif data[index_data.row(), index.type] != 'O':
            if value == 'O':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_tour)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_tour)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_tour)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_tour)
            else:
                window.debugText.insertPlainText('Match type did not change \n')

    def stats_round_update(data, value, stats_data, stats_header, stats_years, index, index_data, window):
        ### old QF
        if data[index_data.row(), index.round] == 'QF':
            if value == 'QF':
                window.debugText.insertPlainText('Round value did not change.\n')
            elif value == 'SF':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_qf)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_qf)
                    statistics.getWL(stats_data, index.st_sf)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_sf)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_qf)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_qf)
                    statistics.getWL(stats_data, index.st_sf)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_sf)
            elif value == 'F':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_qf)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_qf)
                    statistics.getWL(stats_data, index.st_f)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_f)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_qf)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_qf)
                    statistics.getWL(stats_data, index.st_f)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_f)
            else:
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_qf)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_qf)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_qf)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_qf)
        ### old SF
        elif data[index_data.row(), index.round] == 'SF':
            if value == 'QF':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_sf)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_sf)
                    statistics.getWL(stats_data, index.st_qf)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_qf)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_sf)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_sf)
                    statistics.getWL(stats_data, index.st_qf)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_qf)
            elif value == 'SF':
                window.debugText.insertPlainText('Round value did not change.\n')
            elif value == 'F':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_sf)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_sf)
                    statistics.getWL(stats_data, index.st_f)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_f)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_sf)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_sf)
                    statistics.getWL(stats_data, index.st_f)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_f)
            else:
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_sf)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_sf)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_sf)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_sf)
        ### old_tartan
        elif data[index_data.row(), index.round] == 'F':
            if value == 'QF':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_f)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_f)
                    statistics.getWL(stats_data, index.st_qf)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_qf)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_f)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_f)
                    statistics.getWL(stats_data, index.st_sf)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_sf)
            elif value == 'SF':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_f)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_f)
                    statistics.getWL(stats_data, index.st_sf)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_sf)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_f)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_f)
                    statistics.getWL(stats_data, index.st_sf)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_sf)
            elif value == 'F':
                window.debugText.insertPlainText('Round value did not change.\n')  
            else:
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_f)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_f)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_f)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_f)
        ### old NA
        else:
            if value == 'QF':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_qf)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_qf)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_qf)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_qf)
            elif value == 'SF':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_sf)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_sf)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_sf)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_sf)
            elif value == 'F':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_f)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_f)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_f)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_f)                   
            else:
                window.debugText.insertPlainText('Round value change not relevant for stats table.\n')            

    def stats_surface_update(data, value, stats_data, stats_header, stats_years, index_data, index, window):
        ### old tartan
        if data[index_data.row(), index.surf] == 'clay':
            if value == 'clay':
                window.debugText.insertPlainText('Incorrect surface name. Only the following options are considered: clay, tartan, hard \n')
            elif value == 'hard':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_clay)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_clay)
                    statistics.getWL(stats_data, index.st_hard)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_hard)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_clay)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_clay)
                    statistics.getWL(stats_data, index.st_hard)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_hard)
            elif value == 'tartan':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_clay)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_clay)
                    statistics.getWL(stats_data, index.st_tartan)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_tartan)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_clay)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_clay)
                    statistics.getWL(stats_data, index.st_tartan)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_tartan)
            else:
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_clay)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_clay)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_clay)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_clay)
        ### old hard
        elif data[index_data.row(), index.surf] == 'hard':
            if value == 'clay':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_hard)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_hard)
                    statistics.getWL(stats_data, index.st_clay)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_clay)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_hard)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_hard)
                    statistics.getWL(stats_data, index.st_clay)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_clay)
            elif value == 'hard':
                window.debugText.insertPlainText('Incorrect surface name. Only the following options are considered: clay, tartan, hard \n')
            elif value == 'tartan':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_hard)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_hard)
                    statistics.getWL(stats_data, index.st_tartan)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_tartan)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_hard)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_hard)
                    statistics.getWL(stats_data, index.st_tartan)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_tartan)
            else:
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_hard)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_hard)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_hard)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_hard)
        ### old_tartan
        elif data[index_data.row(), index.surf] == 'tartan':
            if value == 'clay':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_tartan)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_tartan)
                    statistics.getWL(stats_data, index.st_clay)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_clay)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_tartan)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_tartan)
                    statistics.getWL(stats_data, index.st_clay)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_clay)
            elif value == 'hard':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_tartan)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_tartan)
                    statistics.getWL(stats_data, index.st_hard)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_hard)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_tartan)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_tartan)
                    statistics.getWL(stats_data, index.st_hard)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_hard)
            elif value == 'tartan':
                window.debugText.insertPlainText('Incorrect surface name. Only the following options are considered: clay, tartan, hard \n')    
            else:
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_tartan)
                    statistics.W2NA(stats_data, statistics.W, statistics.L, index.st_tartan)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_tartan)
                    statistics.L2NA(stats_data, statistics.W, statistics.L, index.st_tartan)
        ### old NA
        else:
            if value == 'clay':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_clay)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_clay)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_clay)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_clay)
            elif value == 'hard':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_hard)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_hard)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_hard)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_hard)
            elif value == 'tartan':
                if data[index_data.row(), index.res] == 'W':
                    statistics.getWL(stats_data, index.st_tartan)
                    statistics.NA2W(stats_data, statistics.W, statistics.L, index.st_tartan)
                elif data[index_data.row(), index.res] == 'L':
                    statistics.getWL(stats_data, index.st_tartan)
                    statistics.NA2L(stats_data, statistics.W, statistics.L, index.st_tartan)                   
            else:
                window.debugText.insertPlainText('Incorrect surface name. Only the following options are considered: clay, tartan, hard \n')
        

    ##########################################################################################################################################
    #-------------------------------------- Auxiliary function (employed in other statistics functions) -------------------------------------#
    ##########################################################################################################################################
    
    def WLupdate(stats_data, ii, index, index_data, window):
        if statistics.sets_lost > statistics.sets_won and statistics.sets_lost > 1: # old loss
            if statistics.sets_lost_new > statistics.sets_won_new and statistics.sets_lost_new > 1: # still a loss
                window.debugText.insertPlainText('No stats change \n')
            elif statistics.sets_lost_new < statistics.sets_won_new and statistics.sets_won_new > 1: # win
                statistics.getWL(stats_data, ii)
                statistics.L2W(stats_data, statistics.W, statistics.L, ii)
            else: # NA
                statistics.getWL(stats_data, ii)
                statistics.L2NA(stats_data, statistics.W, statistics.L, ii)
        elif statistics.sets_lost < statistics.sets_won and statistics.sets_won > 1: # old win
            if statistics.sets_lost_new > statistics.sets_won_new and statistics.sets_lost_new > 1: # loss
                statistics.getWL(stats_data, ii)
                statistics.W2L(stats_data, statistics.W, statistics.L, ii)
            elif statistics.sets_lost_new < statistics.sets_won_new and statistics.sets_won_new > 1: # win
                window.debugText.insertPlainText('No stats change \n')
            else: # NA
                statistics.getWL(stats_data, ii)
                statistics.W2NA(stats_data, statistics.W, statistics.L, ii)
        else: # old NA 
            if statistics.sets_lost_new > statistics.sets_won_new and statistics.sets_lost_new > 1: # loss
                statistics.getWL(stats_data, ii)
                statistics.NA2L(stats_data, statistics.W, statistics.L, ii)
            elif statistics.sets_lost_new < statistics.sets_won_new and statistics.sets_won_new > 1: # win
                statistics.getWL(stats_data, ii)
                statistics.NA2W(stats_data, statistics.W, statistics.L, ii)
            else: # NA
                window.debugText.insertPlainText('No stats change \n')

    def WLupdate_by_result(data, stats_data, old_year, new_year, ii, index, index_data):
        if old_year == None or old_year == '':
            if data[index_data.row(), index.res] == 'W':
                statistics.getWL(stats_data[new_year], ii)
                statistics.NA2W(stats_data[new_year], statistics.W, statistics.L, ii)
            elif data[index_data.row(), index.res] == 'L':
                statistics.getWL(stats_data[new_year], ii)
                statistics.NA2L(stats_data[new_year], statistics.W, statistics.L, ii)
        elif new_year == None or new_year == '':
            if data[index_data.row(), index.res] == 'W':
                statistics.getWL(stats_data[old_year], ii)
                statistics.W2NA(stats_data[old_year], statistics.W, statistics.L, ii)
            elif data[index_data.row(), index.res] == 'L':
                statistics.getWL(stats_data[old_year], ii)
                statistics.L2NA(stats_data[old_year], statistics.W, statistics.L, ii)
        else:
            if data[index_data.row(), index.res] == 'W':
                statistics.getWL(stats_data[old_year], ii)
                statistics.W2NA(stats_data[old_year], statistics.W, statistics.L, ii)
                statistics.getWL(stats_data[new_year], ii)
                statistics.NA2W(stats_data[new_year], statistics.W, statistics.L, ii)
            elif data[index_data.row(), index.res] == 'L':
                statistics.getWL(stats_data[old_year], ii)
                statistics.L2NA(stats_data[old_year], statistics.W, statistics.L, ii)
                statistics.getWL(stats_data[new_year], ii)
                statistics.NA2L(stats_data[new_year], statistics.W, statistics.L, ii)

    def stats_result_update(data, index, index_data):
        if statistics.sets_lost_new > statistics.sets_won_new and statistics.sets_lost_new > 1: # loss
            data[index_data.row(), index.res] = 'L'
        elif statistics.sets_lost_new < statistics.sets_won_new and statistics.sets_won_new > 1: # win
            data[index_data.row(), index.res] = 'W'
        else: # NA
            data[index_data.row(), index.res] = 'NA'

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