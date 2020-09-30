# get index for last row
def last_row(ws):
    for row in range(4, ws.max_row):
        if ws.cell(row=row, column=2).value == None:
            last_row.end = row-1
            break