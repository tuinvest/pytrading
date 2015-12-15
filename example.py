from trading.gateway.dataprovider import *
from trading.model.data import SecurityData
from trading.analysis.average import *
from trading.analysis.volatility import atr
from trading.analysis.distribution import *
from trading.controller.example import *
from trading.controller.base import *
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


# gateway = YahooGateway()

# data = SecurityData()
# data.set_gateway(gateway)
# data.load("ADS.DE")

# lower, middle, upper = bb(data)
# ema_data = ema(data)
# ma_data = ma(data)
# macd_data = macd(data)
# atr_data = atr(data)

# plt.plot(ema_data)
# plt.plot(ma_data)
# plt.plot(macd_data)
# plt.plot(atr_data)
# plt.show()


environment = BacktestingEnvironment()
context = StrategyContext(["SPY"], Portfolio())
strategy = ExampleStrategy(environment, context)
environment.set_strategy(strategy)

environment.do_test()

