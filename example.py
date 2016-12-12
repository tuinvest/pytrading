# -*- coding: utf-8 -*-
from pytrading.entities import AbstractStrategy
from pytrading.indicators import with_series


@with_series('Adj Close')
def momentum(series):
    return series - series.shift()  # Change to previous day


class MomentumStrategy(AbstractStrategy):
    def initialize(self):
        self.universe=['PEP', 'KO']
        self.skip_days=1  # Automate this
        self.indicators={ 'MOMENTUM': momentum }

    def handle_data(self, data, indicators=None):
        sec_weight = 1 / len(self.universe)

        for sec in self.universe:
            if indicators[sec]['MOMENTUM'][-1] > 0.0:
                # Buy at next price, if security closed with an uptick
                self.environment.order_target_percent(sec, sec_weight)
            else:
                # Sell at next price, if security closed with a downtick
                self.environment.order_target_percent(sec, 0.0)


strategy = MomentumStrategy()
strategy.run()
