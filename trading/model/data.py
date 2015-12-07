class StockData(object):

    def __init__(self):
        self.extra = {}

    def set_gateway(self, gateway):
        self.gateway = gateway

    def load(self, symbol):
        self.symbol = symbol
        self.days, self.data = self.gateway.load(symbol)

    def set_extra(self, key, values):
        self.extra[key] = values

    def __getitem__(self, item):
        return self.extra[item]

    def __iter__(self):
        pass

if __name__ == '__main__':
    from trading.gateway import YahooGateway

    gateway = YahooGateway()

    data = StockData()
    data.set_gateway(gateway)

    data.load("ADS.DE")