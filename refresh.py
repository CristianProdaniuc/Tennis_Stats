from PyQt5.QtCore import Qt

class refresh(object):
    """description of class"""
    def h2h_score(model, index_row, index):
        h2h_index = model.createIndex(index_row, index.h2h_won)
        model.setData(h2h_index, model._data[index_row, index.h2h_won][0], role=Qt.EditRole)
        h2h_index = model.createIndex(index_row, index.h2h_lost)
        model.setData(h2h_index, model._data[index_row, index.h2h_lost][0], role=Qt.EditRole)

    def h2h_opponent(model, index_row, index):
        h2h_index = model.createIndex(index_row, index.h2h_op)
        model.setData(h2h_index, model._data[index_row, index.h2h_op], role=Qt.EditRole)
