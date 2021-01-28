from PyQt5.QtCore import Qt

class refresh(object):
    """description of class"""
    def h2h_score(model, index_row, index):
        h2h_indexW = model.createIndex(index_row, index.h2h_won)
        h2h_indexL = model.createIndex(index_row, index.h2h_lost)
        if model._data[index_row, index.h2h_won] == '':
            model.setData(h2h_indexW, model._data[index_row, index.h2h_won], role=Qt.EditRole)
            model.setData(h2h_indexL, model._data[index_row, index.h2h_lost], role=Qt.EditRole)
        else:
            model.setData(h2h_indexW, model._data[index_row, index.h2h_won][0], role=Qt.EditRole)
            model.setData(h2h_indexL, model._data[index_row, index.h2h_lost][0], role=Qt.EditRole)

    def h2h_opponent(model, index_row, index):
        h2h_index = model.createIndex(index_row, index.h2h_op)
        model.setData(h2h_index, model._data[index_row, index.h2h_op], role=Qt.EditRole)

    

    def stats_tab(model, stats_header):
        for ii in range(0, stats_header.size):
            stats_index = model.createIndex(ii, 0)
            model.setData(stats_index, model._data[ii][0])
