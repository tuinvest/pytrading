class SecurityData(object):

    def __init__(self):
        self.extra = {}

    def set_gateway(self, gateway):
        self.gateway = gateway

    def load(self, symbol):
        self.symbol = symbol
        self.data = self.gateway.load(symbol)

    def set_extra(self, key, values):
        self.extra[key] = values

    def __getitem__(self, item):
        if item in ['open', 'high', 'low', 'close', 'volume', 'x']:
            if item == 'open':
                return self.data[:, 0]
            elif item == 'high':
                return self.data[:, 1]
            elif item == 'low':
                return self.data[:, 2]
            elif item == 'close':
                return self.data[:, 3]
            elif item == 'volume':
                return self.data[:, 4]
        return self.extra[item]

    def __iter__(self):
        pass