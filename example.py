from trading.gateway.yahoo import *
from trading.model.data import StockData
from trading.analysis.average import *
from trading.analysis.volatility import atr
import numpy as np

import matplotlib.pyplot as plt

gateway = YahooGateway()

data = StockData()
data.set_gateway(gateway)
data.load("ADS.DE")

# lower, middle, upper = bb(data)
ema_data = ema(data)
ma_data = ma(data)
macd_data = macd(data)

#print(averagetruerange)

# plt.plot(data.data[:,5])
# plt.plot(lower)
# plt.plot(middle, '-')
# plt.plot(upper)

plt.plot(data.data['Close'])
plt.plot(ema_data)
plt.plot(ma_data)
plt.plot(macd_data)
plt.show()