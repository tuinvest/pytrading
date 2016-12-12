# pytrading

[![GitHub license](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)](http://goldsborough.mit-license.org)
[![Code Climate](https://codeclimate.com/github/tuinvest/pytrading/badges/gpa.svg)](https://codeclimate.com/github/tuinvest/pytrading)

Python-library for algorithmic trading based on technical indicators with backtesting ability. Data is pulled from the Yahoo Finance API.

## Installation

Clone repository, setup virtual environment, and install dependencies:

```shell
git clone git@github.com:tuinvest/pytrading.git
cd pytrading/
python3 -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
```

## Basics

To create a PyTrading strategy you only have to subclass the `AbstractStrategy` class from the `pytrading.entities` module. You are required to implement two methods: `initialize` and `handle_data`. The `initialize` method requires you to set a few configuration variables that specify how the strategy is executed. Below we create a strategy whose asset universe include *Pepsi* (**PEP**) and *Coca-Cola* (**KO**).

```python
from pytrading.entities import AbstractStrategy

class ExampleStrategy(AbstractStrategy):
    def initialize(self):
        self.universe = ['PEP', 'KO']

    def handle_data(self, data, indicators=None):
		pass

strategy = ExampleStrategy()
strategy.run()
```

The `handle_data` will be called for every trading day with a `data` dictionary that uses the security tickers as keys and `pandas.DataFrame` objects as values. These `pandas.DataFrame` objects contain `Low`, `High`, `Open`, `Close` and `Adj Close` as columns. PyTrading relies heavily on the data structures provided by `pandas`.

## Indicators

Since no behavior is defined for the `handle_data` method the above strategy will do nothing. Indicators can be used to generate trading signals. They can be utilized by passing a dictionary of the form `{'INDICATOR_NAME': indicator_method}` to the context constructor. `INDICATOR_NAME` is the name by which the indicator data can be accessed later on. `indicator_method` is a method which takes a security's `DataFrame` object as an input and returns the calculated indicator. The indicator data is provided to a strategy's `handle_data` method as well.

```python
from pytrading.entities import AbstractStrategy
from pytrading.indicators import with_series


@with_series('Adj Close')
def momentum(series):
    return series - series.shift()  # Change to previous day


class ExampleStrategy(AbstractStrategy):
    def initialize(self):
        self.universe=['PEP', 'KO']
        self.indicators={ 'MOMENTUM': momentum }

    def handle_data(self, data, indicators=None):
        pass
```

Simply passing the `momentum` method as an indicator method will not work since it takes a series instead of data frame as an argument. The `with_series` decorator can be used to create a method that will call the indicator method with only the data from the specified column label (in this case `Adj Close`).

The indicators can be used to define a simple strategy:

```python
from pytrading.entities import AbstractStrategy
from pytrading.indicators import with_series


@with_series('Adj Close')
def momentum(series):
    return series - series.shift()  # Change to previous day


class MomentumStrategy(AbstractStrategy):
    def initialize(self):
        self.universe=['PEP', 'KO']
        self.skip_days=1  # Skip the first day
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
```

We buy the stocks that performed well and sell those that did perform well during the last day. We additionally set the variable `skip_days` since we cannot calculate momentum data for the first day since that would require the closing price of the day before the first day.
