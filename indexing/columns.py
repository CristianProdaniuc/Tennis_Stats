# obtain indexes for relevant columns in singles sheet
def singles(ws):    
    for col in range(1, ws.max_column):
        if ws.cell(row=3, column=col).value == 'Data':
            singles.data = col

        if ws.cell(row=3, column=col).value == 'Adversar':
            singles.name = col

        if ws.cell(row=3, column=col).value == 'Rezultat':
            singles.rezultat = col

        if ws.cell(row=3, column=col).value == 'Column8':
            singles.set1 = col

        if ws.cell(row=3, column=col).value == 'Tip':
            singles.tip = col

        if ws.cell(row=3, column=col).value == 'Oras':
            singles.oras = col

        if ws.cell(row=3, column=col).value == 'Round':
            singles.round = col

        if ws.cell(row=3, column=col).value == 'Locatie':
            singles.loc = col

        if ws.cell(row=3, column=col).value == 'Suprafata':
            singles.area = col

        if ws.cell(row=3, column=col).value == 'Rate':
            singles.grade = col
