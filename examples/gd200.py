from gateway.yahoo import YahooGateway
from model.data import StockData
from strategies.average import Gd200

gateway = YahooGateway()

data = StockData()
data.set_gateway(gateway)
data.load("ADS.DE")

strategy = Gd200()
strategy.set_data(data)

