import numpy as np
import copy
from datetime import datetime as dt

class tools(object):

    def sort_date(data, index):
        dt_data = copy.deepcopy(data)

        for ii in range(0, data.shape[0]):
            dt_data[ii, index.date] = dt.strptime(dt_data[ii, index.date], '%d.%m.%Y').date()

        data_sorted = data[dt_data[:,index.date].argsort(),:]
        data = data_sorted

        return data

    def sort_h2h(data, index):
        data_copy = copy.deepcopy(data)

        data_sorted = data[data_copy[:, index.h2h_op].argsort(), :]
        data = data_sorted

        return data


