# -*- coding: utf-8 -*-
# TODO: Find a better name for this module
import pandas as pd
from pandas_datareader import data as web
from datetime import datetime


def load(symbol, provider='yahoo', start=datetime(2010, 1, 1), end=None):
    # TODO: Improve Error Handling
    try:
        data = web.DataReader(symbol, data_source=provider,
                              start=start, end=end)
    except:
        raise ValueError('Symbol not found!')

    if data is None:
        raise ValueError('No data found! Could be a wrong provider.')
    return data
