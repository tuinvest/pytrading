# -*- coding: utf-8 -*-
import logging
from abc import ABC, abstractmethod
from . import dataprovider
from .utils import create_fail_method

logger = logging.getLogger(__name__)


class Portfolio(object):
    def __init__(self, cash=10000.0, positions={}):
        self.cash = cash
        self.positions = positions

    def update(self, security, quantity, price, fail_method):
        if quantity * price > self.cash:
            fail_method('Not enough cash to execute order. Security: {}, '
                        'Quantity: {}, Price: {}, Portfolio Cash: {}'
                        .format(security, quantity, price, self.cash),
                        ValueError)
            return
        self.positions.setdefault(security, Position()).update(quantity, price)
        self.cash -= quantity * price

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


class AbstractStrategy(ABC):
    def __init__(self, environment=None):
        self.universe = []
        self.skip_days = 0
        self.indicators = {}
        self.portfolio = Portfolio()
        self.environment = (environment or BacktestingEnvironment)

    def run(self, mode='graceful'):
        self.environment = self.environment(self, mode)
        self.initialize()
        self.environment.backtest()

    @abstractmethod
    def initialize(self):
        raise NotImplementedError('Function not implemented!')

    @abstractmethod
    def handle_data(self, data, indicators=None):
        raise NotImplementedError('Function not implemented!')


class BacktestingEnvironment(object):
    def __init__(self, strategy, mode):
        self.strategy = strategy
        self.portfolio = strategy.portfolio
        self.fail = create_fail_method(mode)

        self.data = {}
        self.indicator_data = {}
        self.current_day = 0 + strategy.skip_days

    def _load_data(self):
        for security in self.strategy.universe:
            self.data[security] = dataprovider.load(security)
            for i_label, i_class in self.strategy.indicators.items():
                # indicator_data example: {'AAPL': {'ATR': ..., 'SMA_14': ...}}
                i_data = i_class._run_calc(self.data[security])
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
            for security in self.strategy.universe
        }

        # Number of rows/days in the df with the most rows/days
        rows = max(len(s) for s in self.data.values())
        for i in range(self.current_day, rows - 1):
            # rows - 1 is the last day on which trading is possible
            self.current_day = i
            for security in self.strategy.universe:
                if len(self.data[security]) > i:  # New data available?
                    # Idea. Wrap df and modify appropriate magic methods to
                    # shift input indices by the number of days that already
                    # have passed 
                    bt_data[security] = self.data[security][:i + 1]

                # Update indicators
                for i_label, i_data in self.indicator_data[security].items():
                    bt_indicators[security][i_label] = self.indicator_data[security][i_label][:i + 1]

            # Let the strategy handle the 'new' data
            self.strategy.handle_data(data=bt_data, indicators=bt_indicators)

        logger.info(self.portfolio)
        logger.info(self.portfolio.total_value(self._next_prices()))

    # Order the specified amount of the security @ the next day's opening price
    # and add it to the portfolio
    def order(self, security, quantity):
        price = self._next_price(security)
        self.portfolio.update(security, quantity, price, self.fail)

    def order_target_percent(self, security, percent):
        logger.info('Ordering {} to {}%.'.format(security, percent*100))
        if percent < 0.0 or percent > 1.0:
            self.fail('Percent must be between 0.0 and 1.0!', ValueError)
            return
        price = self._next_price(security)
        pf_value = self.portfolio.total_value(self._next_prices())

        current_quantity = self.portfolio.position_quantity(security)
        quantity = int((pf_value * percent) / price) - current_quantity
        if quantity != 0:
            self.portfolio.update(security, quantity, price, self.fail)
