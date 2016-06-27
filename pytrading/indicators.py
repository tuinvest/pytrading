# -*- coding: utf-8 -*-
import pandas as pd
from pandas import np
from functools import partial


# TODO: Some indicators do not make sense with min_periods=0, maybe
# enforce min_periods=window for those?

def indicator_partial(indicator, **kwargs):
    return partial(indicator, **kwargs)


def series_indicator(indicator, df_column, **kwargs):
    return partial(_series_indicator, indicator=indicator,
                   df_column=df_column, **kwargs)


def _series_indicator(df, indicator, df_column, **kwargs):
    series = df[df_column]
    return indicator(series, **kwargs)


# Average Indicators

def sma(series, window=50, min_periods=0):
    # Center must always be False to circumvent look-ahead bias
    sma = series.rolling(window=window, min_periods=min_periods,
                         center=False).mean()
    sma.rename(index='SMA', inplace=True)
    return sma


def ema(series, window=50, min_periods=0):
    ema = series.ewm(span=window, min_periods=min_periods, adjust=False).mean()
    ema.rename(index='EMA', inplace=True)
    return ema


def macd(series, fast_window=12, slow_window=26, signal_window=9):
    macd = ema(series, window=fast_window) - ema(series, window=slow_window)
    signal = ema(macd, window=signal_window)
    return pd.DataFrame({'MACD': macd, 'MACD_SIGNAL': signal})


# Distribution Indicators


def bbands(series, window=20, min_periods=0, stdev_multiplier=2):
    middle = sma(series, window=window, min_periods=min_periods)
    std = series.rolling(window=window,
                         min_periods=min_periods).std() * stdev_multiplier
    std.iloc[0] = 0.0  # We define the std of one element to be 0
    upper = middle + std
    lower = middle - std
    return pd.DataFrame({'BBANDS_LOWER': lower,
                         'BBANDS_MIDDLE': middle,
                         'BBANDS_UPPER': upper})


# Oscillators


def rsi(series, window=14, min_periods=0):
    change = series.diff()
    change.iloc[0] = 0.0  # Set gain/loss of first day to zero
    # Using arithmetic mean, not exponential smoothing here
    avg_up = (change.where(lambda x: x > 0, other=0.0)
                    .rolling(window=window, min_periods=min_periods)
                    .mean())
    avg_down = (change.where(lambda x: x < 0, other=0.0)
                      .abs()
                      .rolling(window=window, min_periods=min_periods)
                      .mean())
    rsi = avg_up / (avg_up + avg_down) * 100
    # If avg_up+avg_down = 0 the rsi should be around 50... I think
    rsi.replace(to_replace=[np.inf, np.NaN], value=50, inplace=True)
    if min_periods > 0:
        rsi[:min_periods-1] = np.NaN
    rsi.rename(index='RSI', inplace=True)
    return rsi


def stoc(df, col_labels=('Low', 'High', 'Close'),
         k_smooth=0, d_smooth=3, window=14, min_periods=0):
    # Should col_labels be a dictionary? i.e. {'low':'Low', ...}
    low = df[col_labels[0]]
    high = df[col_labels[1]]
    close = df[col_labels[2]]

    # min_periods should always be 0 for this
    lowest_low = low.rolling(window=window, min_periods=0).min()
    highest_high = high.rolling(window=window, min_periods=0).max()

    k = (close - lowest_low) / (highest_high - lowest_low) * 100

    if min_periods > 0:
        k[:min_periods] = np.NaN

    if k_smooth != 0:
        k = sma(k, window=k_smooth)
    d = sma(k, window=d_smooth)

    return pd.DataFrame({'%K': k, '%D': d})


def fstoc(df, col_labels=('Low', 'High', 'Close'),
          k_smooth=0, d_smooth=3, window=14):
    return stoc(df, col_labels=col_labels, k_smooth=k_smooth,
                d_smooth=d_smooth, window=window, min_periods=0)


def sstoc(df, col_labels=('Low', 'High', 'Close'),
          k_smooth=3, d_smooth=3, window=14):
    return stoc(df, col_labels=col_labels, k_smooth=k_smooth,
                d_smooth=d_smooth, window=window, min_periods=0)


# Volatility Indicators

def atr(df, col_labels=('Low', 'High', 'Close'), window=14):
    low = df[col_labels[0]]
    high = df[col_labels[1]]
    close = df[col_labels[2]]

    tr_1 = high - low
    tr_2 = (high - close.shift()).abs()  # High - Previous Close
    tr_3 = (low - close.shift()).abs()

    max_tr = pd.concat([tr_1, tr_2, tr_3], axis=1).max(axis=1)

    atr = pd.Series(0.0, index=max_tr.index, name='ATR')
    atr[:window-1] = np.NaN
    atr[window-1] = max_tr[:window].mean()

    for i in range(window, len(atr)):
        atr[i] = (atr[i - 1] * (window - 1) + max_tr[i]) / window

    return atr
