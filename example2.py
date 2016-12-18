import logging
from pytrading.entities import AbstractStrategy
from pytrading.indicators import with_series, sma, sstoc, macd


logger = logging.getLogger(__name__)


@with_series('Adj Close')
def momentum(series):
    return sma(series, window=20) - sma(series, window=50)


@with_series('Adj Close')
def momentum3(series):
    return macd(series)


class MomentumStrategy(AbstractStrategy):
    def initialize(self):
        self.universe = ['V', 'GS']
        self.skip_days = 50
        self.indicators = {
            'MOMENTUM_1': momentum,
            'MOMENTUM_2': sstoc,
            'MOMENTUM_3': momentum3,
        }

    def handle_data(self, data, indicators=None):
        sec_weight = 1 / len(self.universe)

        for sec in self.universe:
            sec_indicators = indicators[sec]
            if (sec_indicators['MOMENTUM_1'][-1] > 0.0
                and sec_indicators['MOMENTUM_2']['%K'][-1] < 20.0
                and sec_indicators['MOMENTUM_3']['MACD'][-1] > 0.0):
                self.environment.order_target_percent(sec, sec_weight)
            elif (sec_indicators['MOMENTUM_1'][-1] < 0.0
                  and sec_indicators['MOMENTUM_2']['%K'][-1] > 80.0
                  and sec_indicators['MOMENTUM_3']['MACD'][-1] < 0.0):
                self.environment.order_target_percent(sec, 0.0)


strategy = MomentumStrategy()
strategy.run()
