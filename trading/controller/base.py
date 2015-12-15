from trading.controller.example import *


# The Portfolio object contains all current positions and the current amount of cash
class Portfolio(object):
    def __init__(self, cash=10000.0, positions={}):
        self.cash = cash
        self.positions = positions

    def add(self, security, quantity, price):
        if security not in self.positions:
            self.positions[security] = Position()
        self.positions[security].add(quantity, price)


class Position(object):
    def __init__(self):
        self.quantity = 0
        self.vwap = 0.0

    def add(self, quantity, price):
        # VWAP = SUM(Number of Shares Bought x SharePrice) / TotalSharesBought
        self.vwap = ((self.quantity * self.vwap) + (quantity * price)) / (self.quantity + quantity)
        self.quantity += quantity

    def remove(self, quantity):
        self.quantity -= quantity


class StrategyContext(object):
    def __init__(self, universe=[], portfolio=Portfolio):
        self.universe = universe
        self.portfolio = portfolio


class AbstractEnvironment(object):
    # Load historical data for every security in the strategy universe
    def load_data(self):
        raise NotImplementedError('Function not implemented!')

    # Orders as much shares of the security as the specified amount allows for
    def order(self, security, amount):
        raise NotImplementedError('Function not implemented!')

    def order_percent(self, security, amount):
        raise NotImplementedError('Function not implemented!')

    def order_target(self, security, amount):
        raise NotImplementedError('Function not implemented!')

    def order_target_value(self, security, amount):
        raise NotImplementedError('Function not implemented!')

    def order_target_percent(self, security, amount):
        raise NotImplementedError('Function not implemented!')

    def set_strategy(self, strategy):
        self.strategy = strategy


class AbstractStrategy(object):
    def __init__(self, environment=AbstractEnvironment, context=StrategyContext):
        self.environment = environment
        self.context = context

    def handle_data(self, data):
        raise NotImplementedError('Function not implemented!')

