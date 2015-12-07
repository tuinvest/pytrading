from trading.gateway.yahoo import YahooGateway
from trading.model.data import StockData
from trading.analysis.oscillator import fstoc, sstoc

import matplotlib.pyplot as plt

gateway = YahooGateway()

data = StockData()
data.set_gateway(gateway)
data.load("VOW3.DE")

K, D = sstoc(data)

#plt.plot(data.data[:,5])
plt.plot(K)
plt.plot(D)
plt.show()