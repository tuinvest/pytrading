from trading.gateway.yahoo import YahooGateway
from trading.model.data import StockData
from trading.analysis.average import ma, ema


gateway = YahooGateway()

data = StockData()
data.set_gateway(gateway)
data.load("ADS.DE")

ma(data, 10)
ma(data, 200)
ema(data, 8)