import numpy as np


def atr(stockdata, interval=14):
    atr = atr_raw(np.array([stockdata.data[:, 1], stockdata.data[:, 2], stockdata.data[:, 3]]), interval)
    stockdata.set_extra('ATR_'+str(interval), atr)
    return atr


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
            print tr
            atr[i] = (atr[i - 1] * (i - 1) + tr) / i
        else:
            atr[i] = (atr[i - 1] * (interval - 1) + tr) / interval
    return atr
