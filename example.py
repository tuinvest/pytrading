from trading.gateway.yahoo import YahooGateway
from trading.model.data import StockData
from trading.analysis.oscillator import fstoc, sstoc, rsi

import matplotlib.pyplot as plt

gateway = YahooGateway()

data = StockData()
data.set_gateway(gateway)
data.load("ADS.DE")

K, D = sstoc(data)
rsi = rsi(data)

#plt.plot(data.data[:,5])
plt.plot(rsi)
plt.show()