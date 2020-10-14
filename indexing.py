class indexing(object):    
    
    def origin(ws):
        for col in range(1, ws.max_column+1): # looping done considering XL indexing
            _break = False
            for row in range(1, ws.max_row+1):
                if ws.cell(row=row, column=col).value == 'Data':
                    indexing.header_py = row-1
                    indexing.header_xl = row
                    indexing.row_start_py = row
                    indexing.row_start_xl = row+1
                    indexing.col_start_py = col-1
                    indexing.col_start_xl = col
                    _break = True

            if _break == True:
                break

    def columns(ws):
        for col in range(indexing.col_start_xl, ws.max_column+1): # looping done considering XL indexing
            if ws.cell(row=indexing.header_xl, column=col).value == 'Data':
                indexing.data_xl = col
                indexing.data_py = col-1

            if ws.cell(row=indexing.header_xl, column=col).value == 'Adversar':
                indexing.name_xl = col
                indexing.name_py = col-1

            if ws.cell(row=indexing.header_xl, column=col).value == 'Rezultat':
                indexing.rezultat_xl = col
                indexing.rezultat_py = col-1

            if ws.cell(row=indexing.header_xl, column=col).value == 'Column8' or 'Set1':
                indexing.set1_xl = col
                indexing.set1_py = col-1

            if ws.cell(row=indexing.header_xl, column=col).value == 'Tip':
                indexing.tip_xl = col
                indexing.tip_py = col-1

            if ws.cell(row=indexing.header_xl, column=col).value == 'Oras':
                indexing.oras_xl = col
                indexing.oras_py = col-1

            if ws.cell(row=indexing.header_xl, column=col).value == 'Round':
                indexing.round_xl = col
                indexing.round_py = col-1

            if ws.cell(indexing.header_xl, column=col).value == 'Locatie':
                indexing.loc_xl = col
                indexing.loc_py = col-1

            if ws.cell(row=indexing.header_xl, column=col).value == 'Suprafata':
                indexing.area_xl = col
                indexing.area_py = col-1

            if ws.cell(row=indexing.header_xl, column=col).value == 'Rate':
                indexing.grade_xl = col
                indexing.grade_py = col-1

            if ws.cell(row=indexing.header_xl, column=col).value == 'Observatii':
                indexing.obs_xl = col
                indexing.obs_py = col-1
                indexing.col_end_xl = col+1
                indexing.col_end_py = col

    def rows(ws):
        for row in range(indexing.row_start_xl, ws.max_row+2):
            if ws.cell(row=row, column=indexing.col_start_xl).value == None:
                indexing.row_end_xl = row
                indexing.row_end_py = row-1
                break

