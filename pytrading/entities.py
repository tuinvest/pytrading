# -*- coding: utf-8 -*-
from . import dataprovider
from abc import ABC, abstractmethod


class Portfolio(object):
    def __init__(self, cash=10000.0, positions={}):
        self.cash = cash
        self.positions = positions

    def update(self, security, quantity, price):
        if quantity * price > self.cash:
            raise ValueError('Not enough cash to execute order. Security: {}, '
                             'Quantity: {}, Price: {}, Portfolio Cash: {}'
                             .format(security, quantity, price, self.cash))
        self.positions.setdefault(security, Position()).update(quantity, price)
        self.cash -= quantity * price
        # print(security, ":", quantity, "@", price)

    def total_value(self, prices):
        value = 0.0
        for s, p in self.positions.items():
            value += prices[s] * p.quantity
        return value + self.cash

    def position_quantity(self, security):
        if security in self.positions:
            return self.positions[security].quantity
        return 0

    def __repr__(self):
        # positions = ','.join(
        #    ['({}, {})'.format(s, p) for s, p in self.positions.items()])
        return 'Portfolio(Cash: {}, {})'.format(self.cash, self.positions)


class Position(object):
    def __init__(self, quantity=0, vwap=0.0):
        self.quantity = quantity
        self.vwap = vwap

    def update(self, quantity, price):
        # Update Volume Weighted Average Price and Quantity
        # VWAP = SUM(Number of Shares Bought x SharePrice) / TotalSharesBought
        if self.quantity + quantity == 0:
            self.vwap = 0.0
        else:
            self.vwap = ((self.quantity * self.vwap) + (quantity * price)) / (self.quantity + quantity)
        self.quantity += quantity

    def __repr__(self):
        return 'Position(quantity={}, vwap={})'.format(
            self.quantity, self.vwap)


class StrategyContext(object):
    def __init__(self, universe,
                 skip_days=0, indicators={}):
        self.universe = universe
        self.skip_days = skip_days
        self.indicators = indicators

        self.portfolio = Portfolio()


class AbstractStrategy(ABC):
    def __init__(self, context, environment=None):
        self.context = context
        self.environment = environment

    def set_environment(self, environment):
        self.environment = environment

    @abstractmethod
    def before(self):
        raise NotImplementedError('Function not implemented!')

    @abstractmethod
    def handle_data(self, data, indicators=None):
        raise NotImplementedError('Function not implemented!')


class BacktestingEnvironment(object):
    def __init__(self, strategy):
        self.strategy = strategy
        self.context = strategy.context
        self.portfolio = strategy.context.portfolio
        self.strategy.set_environment(self)

        self.data = {}
        self.indicator_data = {}
        self.current_day = 0 + strategy.context.skip_days

    def _load_data(self):
        for security in self.context.universe:
            self.data[security] = dataprovider.load(security)
            for i_label, i_callable in self.context.indicators.items():
                # indicator_data example: {'AAPL': {'ATR': ..., 'SMA_14': ...}}
                i_data = i_callable(self.data[security])
                self.indicator_data.setdefault(security, {})[i_label] = i_data

    def _next_price(self, security):
        # The next price is considered the next possible buy/sell price
        # portfolio.update should always be called with this price
        return self.data[security]['Adj Close'][self.current_day + 1]

    def _next_prices(self):
        prices = {}
        for s, df in self.data.items():
            prices[s] = df['Adj Close'][self.current_day + 1]
        return prices

    def backtest(self):
        self._load_data()
        bt_data = {}
        bt_indicators = {
            security: {}
            for security in self.context.universe
        }

        # Simulate progression of the stock market by feeding the strat data
        rows = max(len(s) for s in self.data.values())  # Max. days
        for i in range(self.current_day, rows - 1):
            # rows - 1 is the last day trading is possible
            self.current_day = i
            for security in self.context.universe:
                if len(self.data[security]) > i:  # New data available?
                    bt_data[security] = self.data[security][:i + 1]

                # Update indicators
                for i_label, i_data in self.indicator_data[security].items():
                    bt_indicators[security][i_label] = self.indicator_data[security][i_label][:i + 1]

            # Let the strategy handle the 'new' data
            self.strategy.handle_data(data=bt_data, indicators=bt_indicators)

        print(self.portfolio)
        print(self.portfolio.total_value(self._next_prices()))

    # Order the specified amount of the security @ the next day's opening price
    # and add it to the portfolio
    def order(self, security, quantity):
        price = self._next_price(security)
        self.portfolio.update(security, quantity, price)

    def order_target_percent(self, security, percent):
        if percent < 0.0 or percent > 1.0:
            raise ValueError('Percent must be between 0.0 and 1.0!')
        price = self._next_price(security)
        pf_value = self.portfolio.total_value(self._next_prices())

        current_quantity = self.portfolio.position_quantity(security)
        quantity = int((pf_value * percent) / price) - current_quantity
        if quantity != 0:
            self.portfolio.update(security, quantity, price)
