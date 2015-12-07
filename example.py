from trading.gateway.yahoo import YahooGateway
from trading.model.data import StockData
from trading.analysis.average import ma, ema, macd

import matplotlib.pyplot as plt

gateway = YahooGateway()

data = StockData()
data.set_gateway(gateway)
data.load("VOW3.DE")

macd, signal = macd(data)

plt.plot(data.data[:,5])
plt.plot(macd)
plt.plot(signal)
plt.show()