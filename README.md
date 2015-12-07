# algotrading

Python-library for algorithmic trading in python based on technical indicators with backtesting ability. Data is pulled from the Yahoo Finance API.

## Usage

First create a gateway to a datasource. Currently, only Yahoo Finance is available.

```python
from trading.gateway.yahoo import YahooGateway
gateway = YahooGateway()
```

Create a StockData object which holds and manipulates the stock data and load stock data for a specific symbol or index into it.

```python
from trading.model.data import StockData
data = StockData()
data.set_gateway(gateway)
data.load("VOW3.DE")
```

Use the analysis library to calculate indicators for the stock data.

```python
from trading.analysis.average import macd
macd, signal = macd(data)
```

## Documentation

### Analysis

The following functions for technical analysis are available.

#### Package `trading.analysis.average`

```python
ma = ma(stockdata, interval=10)
```
Calculates the moving average for a specific StockData object with a moving window of `interval` days. 
Returns `ma` 1d array, the moving average.

```python
ema = ema(stockdata, interval=8)
```
Calculates the exponential moving average for a specific StockData object with a exponential window of `interval` days.
Returns `ema` 1d array, the exponential moving average.

```python
macd, signal = macd(stockdata, fast=12, slow=26, signal_t=9)
``` 
Calculates the MACD line for a specific StockData object with `fast` and `slow` being the two moving averages to compare. The signal time interval of the MACD indicator can be set with `signal_t`.
Returns `macd` 1d array, the macd indicator.
Returns `signal` 1d array, the signal line.