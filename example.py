from trading.gateway.yahoo import YahooGateway
from trading.model.data import StockData
from trading.analysis.average import moving_average

gateway = YahooGateway()

data = StockData()
data.set_gateway(gateway)
data.load("ADS.DE")

moving_average(data)