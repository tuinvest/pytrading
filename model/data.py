class StockData(object):
    def __init__(self):
        pass

    def set_gateway(self, gateway):
        self.gateway = gateway

    def load(self, symbol):
        self.gateway.load(symbol)

    def __iter__(self):
        pass