import numpy as np
import math
from average import ma_raw

CLOSE_ROW_ID = 5

# ----
# STOC
# ----

def sstoc(stockdata, interval=14, k_smooth=3, d_smooth=3):
    K, D = stoc_raw(stockdata.data[:, CLOSE_ROW_ID], interval, k_smooth, d_smooth)
    stockdata.set_extra('SSTOC_'+str(interval)+'_'+str(d_smooth)+'_K', K)
    stockdata.set_extra('SSTOC_'+str(interval)+'_'+str(d_smooth)+'_D', D)
    return K, D

def fstoc(stockdata, interval=14, d_smooth=3):
    K, D = stoc_raw(stockdata.data[:, CLOSE_ROW_ID], interval, 0, d_smooth)
    stockdata.set_extra('FSTOC_'+str(interval)+'_'+str(d_smooth)+'_K', K)
    stockdata.set_extra('FSTOC_'+str(interval)+'_'+str(d_smooth)+'_D', D)
    return K, D

def stoc_raw(data, interval=14, k_smooth=0, d_smooth=3):
    K = np.zeros((data.shape[0], ))
    D = np.zeros((data.shape[0], ))

    K[:interval] = 50.0
    D[:interval] = 50.0

    for i in range(interval, data.shape[0]):
        K[i] = (data[i] - np.min(data[i-interval:i+1])) / (np.max(data[i-interval:i+1]) - np.min(data[i-interval:i+1])) * 100.0

    if k_smooth != 0:
        K = ma_raw(K, k_smooth)
    D = ma_raw(K, d_smooth)

    return K, D

# ---
# RSI
# ---

def rsi(stockdata, interval=14):
    rsi = rsi_raw(stockdata.data[:, CLOSE_ROW_ID], interval)
    stockdata.set_extra('RSI_'+str(interval), rsi)
    return rsi

def rsi_raw(data, interval=14):
    rsi = np.zeros((data.shape[0]-1, ))
    returns = data[1:] - data[:data.shape[0]-1]
    for i in range(returns.shape[0]):
        if i < interval:
            interval_returns = returns[:i+1]
        else:
            interval_returns = returns[i-interval:i+1]
        avg_up = np.average(interval_returns[np.where(interval_returns > 0)])
        avg_down = np.abs(np.average(interval_returns[np.where(interval_returns < 0)]))

        avg_up = 0.0 if math.isnan(avg_up) else avg_up
        avg_down = 0.0 if math.isnan(avg_down) else avg_down

        rsi[i] = avg_up / (avg_up + avg_down) * 100.0
    return rsi