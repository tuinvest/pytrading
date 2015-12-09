from trading.gateway.yahoo import YahooGateway
from trading.model.data import StockData
from trading.analysis.distribution import bb
from trading.analysis.volatility import atr
import numpy as np

import matplotlib.pyplot as plt

gateway = YahooGateway()

data = StockData()
data.set_gateway(gateway)
data.load("ADS.DE")

# lower, middle, upper = bb(data)
averagetruerange = atr(data)

print averagetruerange

# plt.plot(data.data[:,5])
# plt.plot(lower)
# plt.plot(middle, '-')
# plt.plot(upper)

plt.plot(averagetruerange)
plt.show()