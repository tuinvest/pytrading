# pytrading

[![GitHub license](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)](http://goldsborough.mit-license.org)
[![Code Climate](https://codeclimate.com/github/tuinvest/pytrading/badges/gpa.svg)](https://codeclimate.com/github/tuinvest/pytrading)

Python-library for algorithmic trading based on technical indicators with backtesting ability. Data is pulled from the Yahoo Finance API.

## Installation

Setup virtual environment and install dependencies:

```shell
python3 -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
```


## Basics

There are two components needed to run a trading strategy. The strategy itself and the environment in which it is executed (e.g. backtesting environment). 

PyTrading provides a `BacktestingEnvironment` which is initizalized with a strategy as an argument. A strategy can be created by subclassing `AbstractStrategy`. Strategies are initizalized with a context that stores information such as the securities universe and the current portfolio. 

To start off, subclass `AbstractStrategy`, create a context and use it to initizalize the strategy. The `BacktestingEnvironment` can be used to backtest this strategy.

```python
from pytrading.entities import AbstractStrategy, StrategyContext, BacktestingEnvironment

class ExampleStrategy(AbstractStrategy):
    def before(self):
        pass

    def handle_data(self, data, indicators=None):
		pass

context = StrategyContext(['PEP', 'KO'])
strategy = ExampleStrategy(context)
environment = BacktestingEnvironment(strategy)
environment.backtest()
```

The `handle_data` will be called for every trading day with a `data` dictionary that uses the security tickers as keys and `pandas.DataFrame` objects as values. These `pandas.DataFrame` objects contain `Low`, `High`, `Open`, `Close` and `Adj Close` as columns. PyTrading relies heavily on the data structures provided by `pandas`.

## Indicators

Since no behavior is defined for the `handle_data` method the above strategy will do nothing. Indicators can be used to generate trading signals. They can be utilized by passing a dictionary of the form `{'INDICATOR_NAME': indicator_method}` to the context constructor. `INDICATOR_NAME` is the name by which the indicator data can be accessed later on. `indicator_method` is a method which takes a security's `DataFrame` object as an input and returns the calculated indicator. The indicator data is provided to a strategy's `handle_data` method.

```python
from pytrading.indicators import series_indicator

def momentum(self, series):
	return series - series.shift() # Close price - Previous close price

indicators = {
    'MOMENTUM': series_indicator(momentum, 'Adj Close')
}
```

Simply passing the `momentum` method as an indicator method will not work since it takes a series instead of data frame as an argument. `series_indicator` can be used to create a method that will call the indicator method with only the data from the specified column. In this example, the `momentum` method will be called with the data from the `Adj Close` column.

The indicators can be used to define a simple strategy:

```python
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
```