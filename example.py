from trading.gateway.yahoo import YahooGateway
from trading.model.data import StockData
from trading.analysis.distribution import bb

import matplotlib.pyplot as plt

gateway = YahooGateway()

data = StockData()
data.set_gateway(gateway)
data.load("ADS.DE")

lower, middle, upper = bb(data)

#plt.plot(data.data[:,5])
plt.plot(lower)
plt.plot(middle, '-')
plt.plot(upper)
plt.show()