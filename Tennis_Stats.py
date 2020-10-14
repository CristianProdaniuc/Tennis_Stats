from openpyxl import load_workbook, Workbook, styles, worksheet
import numpy as np
import sys, os 
from main_window import main
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) #get project root directory
# start the GUI
app = QApplication(sys.argv)
main(ROOT_DIR + '\\GUI\\main.ui')
sys.exit(app.exec_())




#XLpalmares = load_workbook("E:\\Documents\\palmares_AR2.xlsx")
#XLpalmares.active = 0
#ws_singles = XLpalmares.active

#XLmodified = Workbook()
#ws_out = XLmodified.active

#columns.singles(ws_singles)
#rows.last_row(ws_singles)

## head 2 head statistics
#opponents = []

#for row in range(4, rows.last_row.end):
#    opponents.append(ws_singles.cell(row=row, column=columns.singles.name).value)

#opponents = sorted(list(dict.fromkeys(opponents)))
#opponents = [i for i in opponents if i not in ('Trupa', 'singur', 'singur & Marius Tamas', 'trupa', 'turneu', 'turneu dublu')]
 
#Nop = len(opponents)
#op_index = -1
#h2h_score = np.zeros((Nop, 2))

#for name in opponents:
#    op_index += 1

#    for row in range(4, rows.last_row.end):
#        if ws_singles.cell(row=row, column=columns.singles.name).value == name and ws_singles.cell(row=row, column=columns.singles.set1).value != None:
#            set = 0
#            print('\n')
#            sets_won = 0
#            sets_lost = 0
#            while ws_singles.cell(row=row, column=columns.singles.set1 +set).value != None and ws_singles.cell(row=row, column=columns.singles.set1 +set).value != 'F' and set < 3:
#                print(ws_singles.cell(row=row, column=columns.singles.set1 +set).value)
#                lindex = ws_singles.cell(row=row, column=columns.singles.set1 +set).value.find('-')
#                if ws_singles.cell(row=row, column=columns.singles.set1 +set).value[-2:] == 'ab':
#                    sets_won = 10
#                elif int(ws_singles.cell(row=row, column=columns.singles.set1 +set).value[0:lindex]) > int(ws_singles.cell(row=row, column=columns.singles.set1 +set).value[lindex+1:]) and \
#                     int(ws_singles.cell(row=row, column=columns.singles.set1 +set).value[0:lindex]) > 5:
#                    sets_won += 1
#                elif int(ws_singles.cell(row=row, column=columns.singles.set1 +set).value[0:lindex]) < int(ws_singles.cell(row=row, column=columns.singles.set1 +set).value[lindex+1:]) and \
#                     int(ws_singles.cell(row=row, column=columns.singles.set1 +set).value[lindex+1:]) > 5:
#                    sets_lost += 1

#                set += 1

#            if sets_won > sets_lost and sets_won > 1:
#                h2h_score[op_index][0] += 1
#            elif sets_lost > sets_won and sets_lost > 1:
#                h2h_score[op_index][1] += 1


#ws_out.column_dimensions['A'].width = 4
#ws_out.column_dimensions['B'].width = 3
#ws_out.column_dimensions['C'].width = 4
#ws_out.column_dimensions['D'].width = 30
#for ii in range(0, Nop):
#    ws_out.cell(row=ii+1, column=1).value = h2h_score[ii][0]
#    ws_out.cell(row=ii+1, column=2).value = '-'
#    ws_out.cell(row=ii+1, column=3).value = h2h_score[ii][1]
#    ws_out.cell(row=ii+1, column=4).value = opponents[ii]
#    print(opponents[ii], h2h_score[ii][0], '-', h2h_score[ii][1], '\n')


#XLmodified.save('E:\\Documents\\palmares_moldificat.xlsx')
