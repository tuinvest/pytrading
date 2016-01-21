from trading.gateway.dataprovider import *
from trading.analysis.distribution import *
from trading.analysis.volatility import *
from trading.analysis.average import *
import matplotlib.pyplot as plt

# gateway = YahooGateway()

# data = SecurityData()
# data.set_gateway(gateway)
# data.load("ADS.DE")

#environment = BacktestingEnvironment()
#context = StrategyContext(["SPY"], Portfolio())
#strategy = ExampleStrategy(environment, context)
#environment.set_strategy(strategy)

#environment.do_test()

y = YahooGateway()
data = y.load("GOOG")

bb(data)
ema(data)
ma(data)
macd(data)
atr(data)

print(data)
plt.plot(data['Close'])
plt.plot(data['MA'])
plt.plot(data['EMA'])
plt.plot(data['MACD'])
plt.plot(data['MACD_Signal'])
plt.plot(data['BB_Lower'])
plt.plot(data['BB_Middle'])
plt.plot(data['BB_Upper'])
plt.plot(data['ATR'])
plt.show()