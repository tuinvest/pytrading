import numpy as np
from trading.analysis.average import ma_raw

CLOSE_ROW_ID = 5

# ---------------
# Bollinger Bands
# ---------------


def bb(stockdata, interval=20, stdev_multiplier=2):
    lower, middle, upper = bb_raw(
        stockdata['Close'],
        interval,
        stdev_multiplier
    )
    stockdata['BB_Lower'] = lower
    stockdata['BB_Middle'] = middle
    stockdata['BB_Upper'] = upper
    stockdata['BB_Lower_{}_{}'.format(interval, stdev_multiplier)] = lower
    stockdata['BB_Middle_{}_{}'.format(interval, stdev_multiplier)] = middle
    stockdata['BB_Upper_{}_{}'.format(interval, stdev_multiplier)] = upper
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
