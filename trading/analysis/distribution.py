import numpy as np
from average import ma_raw

CLOSE_ROW_ID = 5

# ---------------
# Bollinger Bands
# ---------------

def bb(stockdata, interval=20, stdev_multiplier=2):
    lower, middle, upper = bb_raw(stockdata.data[:,CLOSE_ROW_ID], interval, stdev_multiplier)
    stockdata.set_extra('BB_'+str(interval)+'_'+str(stdev_multiplier)+'_LOWER', lower)
    stockdata.set_extra('BB_'+str(interval)+'_'+str(stdev_multiplier)+'_MIDDLE', middle)
    stockdata.set_extra('BB_'+str(interval)+'_'+str(stdev_multiplier)+'_UPPER', upper)
    return lower, middle, upper

def bb_raw(data, interval=20, stdev_multiplier=2):
    stdev = np.zeros(data.shape)
    for i in range(1, stdev.shape[0]):
        if i < interval:
            stdev[i] = np.std(data[0:i+1])
        else:
            stdev[i] = np.std(data[i-interval:i+1])
    middle = ma_raw(data, interval)
    upper = middle + stdev_multiplier * stdev
    lower = middle - stdev_multiplier * stdev

    return lower, middle, upper