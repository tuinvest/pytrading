import numpy as np

CLOSE_ROW_ID = 4

def moving_average(stockdata, interval=10):
    average = np.zeros((stockdata.data.shape[0], ))

    for i in range(stockdata.data.shape[0]):
        if i < interval:
            average[i] = np.average(stockdata.data[0:i+1, CLOSE_ROW_ID])
        else:
            average[i] = np.average(stockdata.data[i-interval:i+1, CLOSE_ROW_ID])

        stockdata.set_extra('moving_average_'+str(interval), average)

if __name__ == '__main__':
    from trading.gateway import YahooGateway
    from trading.model.data import StockData

    gateway = YahooGateway()

    data = StockData()
    data.set_gateway(gateway)
    moving_average(data)

    print data.data