# -*- coding: utf-8 -*-
from pytrading.entities import AbstractStrategy, StrategyContext, Portfolio,\
                               BacktestingEnvironment
from pytrading.indicators import series_indicator


class MomentumStrategy(AbstractStrategy):
    def before(self):
        pass

    def handle_data(self, data, indicators=None):
        sec_weight = 1/len(self.context.universe)

        for sec in self.context.universe:
            if indicators[sec]['MOMENTUM'][-1] > 0.0:
                # Buy at next price, if security closed with an uptick
                self.environment.order_target_percent(sec, sec_weight)
            else:
                # Sell at next price, if security closed with a downtick
                self.environment.order_target_percent(sec, 0.0)


def momentum(series):
    return series - series.shift()  # Change to previous day

indicators = {
    'MOMENTUM': series_indicator(momentum, 'Adj Close')
}

# (Current close - Previous close) cannot be calculated for day zero,
# so we skip the first trading day.
context = StrategyContext(['PEP'], skip_days=1, indicators=indicators)

strategy = MomentumStrategy(context)
environment = BacktestingEnvironment(strategy)
environment.backtest()
