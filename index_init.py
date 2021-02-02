class index_init(object):
    """description of class"""
    def columns(header):
        for col in range(0, len(header)):
            
            if header[col] == 'Date':
                index_init.date = col 

            if header[col] == 'Opponent':
                index_init.op = col 

            if header[col] == 'Result':
                index_init.res = col 

            if header[col] == 'Set1':
                index_init.set1 = col 

            if header[col] == 'Set2':
                index_init.set2 = col 

            if header[col] == 'Set3':
                index_init.set3 = col 

            if header[col] == 'Type':
                index_init.type = col 

            if header[col] == 'City':
                index_init.city = col 

            if header[col] == 'Round':
                index_init.round = col 

            if header[col] == 'Venue':
                index_init.loc = col 

            if header[col] == 'Surface':
                index_init.surf = col 

            if header[col] == 'Rating':
                index_init.rating = col 

            if header[col] == 'Observations':
                index_init.obs = col 

    def h2h_columns(header):
        for col in range(0, len(header)):
            if header[col] == 'Won':
                index_init.h2h_won = col 

            if header[col] == 'Lost':
                index_init.h2h_lost = col 

            if header[col] == 'Opponent':
                index_init.h2h_op = col 

            if header[col] == 'Matches':
                index_init.h2h_matches = col 

    def stats_rows(header):
        for row in range(0, len(header)):
            if header[row] == 'Overall':
                index_init.st_overall = row

            if header[row] == 'Clay':
                index_init.st_clay = row

            if header[row] == 'Hard':
                index_init.st_hard = row

            if header[row] == 'Tartan':
                index_init.st_tartan = row

            if header[row] == 'Tournament':
                index_init.st_tour = row

            if header[row] == 'Quarter-Final':
                index_init.st_qf = row

            if header[row] == 'Semi-Final':
                index_init.st_sf = row

            if header[row] == 'Final':
                index_init.st_f = row