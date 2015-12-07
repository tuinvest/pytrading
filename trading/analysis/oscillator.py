import numpy as np
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