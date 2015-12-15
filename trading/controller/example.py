from trading.gateway.dataprovider import *
from trading.model.data import *
from trading.controller.base import *


class BacktestingEnvironment(AbstractEnvironment):
    def load_data(self):
        self.historical_data = {}
        for security in self.strategy.context.universe:
            sec_data = SecurityData()
            sec_data.set_gateway(YahooGateway())
            sec_data.load(security)
            self.historical_data[security] = sec_data

    def do_test(self):
        self.load_data()
        self.data = {}

        # Simulate progression of the stock market by expanding the data set one by one
        for i in range(0, len(self.historical_data.values()[0].data.index) - 1):
            # Set data[security] to be the 'current' data available to the strategy
            for security in self.strategy.context.universe:
                self.data[security] = self.historical_data[security].data[:i]
            # Let the strategy handle the 'new' data
            self.strategy.handle_data(data=self.data)

    # Order the specified amount of the security @ the next day's opening price and it to the portfolio
    def order(self, security, amount):
        next_day = len(self.data[security]) + 1
        price = self.historical_data[security].data.iloc[next_day]["Open"]
        quantity = int(amount / price)
        self.strategy.context.portfolio.add(security, quantity, price)
        print security, ":", quantity, "@", price


class ExampleStrategy(AbstractStrategy):
    def handle_data(self, data):
        for sec in self.context.universe:
            self.environment.order(security=sec, amount=1000.0)
