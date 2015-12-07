# algotrading

Python-library for algorithmic trading based on technical indicators with backtesting ability. Data is pulled from the Yahoo Finance API.

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
Calculates the *moving average* for a specific StockData object with a moving window of `interval` days. 
Returns `ma` 1d array, the moving average.

```python
ema = ema(stockdata, interval=8)
```
Calculates the *exponential moving average* for a specific StockData object with a exponential window of `interval` days.
Returns `ema` 1d array, the exponential moving average.

```python
macd, signal = macd(stockdata, fast=12, slow=26, signal_t=9)
``` 
Calculates the *MACD* line for a specific StockData object with `fast` and `slow` being the two moving averages to compare. The signal time interval of the MACD indicator can be set with `signal_t`.
Returns `macd` 1d array, the macd indicator.
Returns `signal` 1d array, the signal line.

#### Package `trading.analysis.oscillator`

```python
K, D = fstoc(stockdata, interval=14, d_smooth=3)
```
Calculates the *fast stochastic oscillator* indicators K and D for a given StockData object, `interval` being the look-back period and `d_smooth` being the smoothing period for indicator D.
Returns `K` 1d array, the %K indicator.
Returns `D` 1d array, the %D indicator.

```python
K, D = sstoc(stockdata, interval=14, k_smooth=3, d_smooth=3)
```
Calculates the *slow stochastic oscillator* indicators K and D for a given StockData object, `interval` being the look-back period, `k_smooth` being the smoothing period for indicator K and `d_smooth` being the smoothing period for indicator D.
Returns `K` 1d array, the %K indicator.
Returns `D` 1d array, the %D indicator.

```python
rsi = rsi(stockdata, interval=14)
```
Calculates the *relative strength* indicator for a given StockData object, `interval` being the look-back period.
Returns `rsi` 1d array, the RSI indicator.

#### Package `trading.analysis.distribution`
```python
lower, middle, upper = bb(stockdata, interval=20, stdev_multiplier=2)
```
Calculates the *Bollinger bands* for a given StockData object, `interval` being the look-back period and `stdev_multiplier` being the multiplication factor of the standard deviation as the distance between the middle and the upper and lower bollinger band.
Returns `lower` 1d array, the lower Bollinger band.
Returns `middle` 1d array, the middle (moving average) band.
Returns `upper` 1d array, the upper Bollinger band.