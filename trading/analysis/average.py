import numpy as np

CLOSE_ROW_ID = 5

# --
# MA
# --


def ma(stockdata, interval=10):
    average = ma_raw(stockdata['Close'], interval)
    stockdata['MA'] = average
    stockdata['MA_{}'.format(interval)] = average
    return average


def ma_raw(data, interval):
    average = np.zeros((data.shape[0], ))
    for i in range(data.shape[0]):
        if i < interval:
            average[i] = np.average(data[0:i+1])
        else:
            average[i] = np.average(data[i-interval:i+1])
    return average

# ---
# EMA
# ---


def ema(stockdata, interval=8):
    average = ema_raw(stockdata['Close'], interval)
    stockdata['EMA'.format(interval)] = average
    stockdata['EMA_{}'.format(interval)] = average
    return average


def ema_raw(data, interval):
    average = np.zeros((data.shape[0], ))
    average[0:interval] = np.average(data[0:interval])
    for i in range(interval, data.shape[0]):
        average[i] = average[i-1] * (1-2/float(interval)) + data[i] * 2/float(interval)
    return average

# ----
# MACD
# ----

def macd(stockdata, fast=12, slow=26, signal_t=9):
    macd, signal = macd_raw(stockdata['Close'], fast, slow, signal_t)
    stockdata['MACD'] = macd
    stockdata['MACD_Signal'] = signal
    stockdata['MACD_{}_{}_{}'.format(fast, slow, signal_t)] = macd
    stockdata['MACD_Signal_{}_{}_{}'.format(fast, slow, signal_t)] = signal
    return macd, signal


def macd_raw(data, fast, slow, signal_t):
    macd = ema_raw(data, fast) - ema_raw(data, slow)
    signal = ema_raw(macd, signal_t)
    return macd, signal