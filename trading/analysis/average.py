import numpy as np

CLOSE_ROW_ID = 3

def ma(stockdata, interval=10):
    average = np.zeros((stockdata.data.shape[0], ))

    for i in range(stockdata.data.shape[0]):
        if i < interval:
            average[i] = np.average(stockdata.data[0:i+1, CLOSE_ROW_ID])
        else:
            average[i] = np.average(stockdata.data[i-interval:i+1, CLOSE_ROW_ID])

        stockdata.set_extra('MA_'+str(interval), average)

def ema(stockdata, interval=8):
    average = np.zeros((stockdata.data.shape[0], ))

    average[0:interval] = np.average(stockdata.data[0:interval, CLOSE_ROW_ID])

    for i in range(interval, stockdata.data.shape[0]):
        average[i] = average[i-1] * (1-2/float(interval)) + stockdata.data[i, CLOSE_ROW_ID] * 2/float(interval)

    stockdata.set_extra('EMA_'+str(interval), average)