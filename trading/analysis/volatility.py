import numpy as np
import pandas as pd


def atr(stockdata, interval=14):
    atr_data = atr_raw(np.array([stockdata['High'], stockdata['Low'], stockdata['Close']]), interval)
    stockdata['ATR'] = atr_data
    stockdata['ATR_{}'.format(interval)] = atr_data
    return atr_data


def atr_raw(data, interval=14):
    atr = np.zeros((data.shape[1], ))
    # ATR for the first value
    atr[0] = data[0, 0] - data[1, 0]
    for i in range(1, data.shape[1]):
        # High - Low
        tr0 = data[0, i] - data[1, i]
        # abs(High - Close_prev)
        tr1 = abs(data[0, i] - data[2, i - 1])
        # abs(Low - Close_prev)
        tr2 = abs(data[1, i] - data[2, i - 1])
        tr = max(tr0, tr1, tr2)

        if i < interval:
            atr[i] = (atr[i - 1] * (i - 1) + tr) / i
        else:
            atr[i] = (atr[i - 1] * (interval - 1) + tr) / interval
    return atr
