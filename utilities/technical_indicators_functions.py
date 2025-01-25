import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_OBV(open, close, volume):
  OBV_daily = np.where(close > open, volume,
                      np.where(close < open, -volume, 0))
  return OBV_daily.cumsum()

def calculate_SMA(series, window):
  return series.rolling(window=window).mean()

def calculate_EMA(series, span):
  return series.ewm(span=span, adjust=False).mean()

def calculate_MACD(close, short_window=12, long_window=26, signal_window=9):
  # Calculate the MACD Line
  short_ema = close.ewm(span=short_window, adjust=False).mean()
  long_ema = close.ewm(span=long_window, adjust=False).mean()
  MACD = short_ema - long_ema

  # Calculate the Signal Line
  MACD_signal_line = MACD.ewm(span=signal_window, adjust=False).mean()

  # Calculate the Histogram
  MACD_histogram = MACD - MACD_signal_line
  return MACD, MACD_signal_line, MACD_histogram

def plot_MACD(timestamp, MACD, MACD_signal_line, MACD_histogram):
  plt.figure(figsize=(15, 8))
  plt.plot(MACD, label='MACD', color='blue')
  plt.plot(MACD_signal_line, label='Signal Line', color='red')
  plt.bar(timestamp, MACD_histogram, label='Histogram', color='gray')
  plt.legend(loc='upper left')
  plt.title('MACD Indicator')
  plt.show()

def calculate_RSI(close, window=7):
  delta = close.diff()
  gain = (delta.where(delta > 0, 0)).ewm(alpha=1/window, adjust=False).mean()
  loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/window, adjust=False).mean()
  RS = gain / loss
  return 100 - (100 / (1 + RS))

def calculate_ADX(high, low, close, n=14):
  df = pd.DataFrame({'high': high, 'low': low, 'close': close})

  # Calculate True Range (TR)
  df['TR'] = np.maximum(df['high'] - df['low'], 
                        np.maximum(abs(df['high'] - df['close'].shift(1)), 
                                    abs(df['low'] - df['close'].shift(1))))

  # Calculate Directional Movement
  df['+DM'] = np.where((df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']), 
                        np.maximum(df['high'] - df['high'].shift(1), 0), 0)
  
  df['-DM'] = np.where((df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)), 
                        np.maximum(df['low'].shift(1) - df['low'], 0), 0)

  # Smooth the indicators
  df['TR_smooth'] = df['TR'].rolling(window=n).sum()
  df['+DM_smooth'] = df['+DM'].rolling(window=n).sum()
  df['-DM_smooth'] = df['-DM'].rolling(window=n).sum()

  # Calculate +DI and -DI
  df['+DI'] = 100 * (df['+DM_smooth'] / df['TR_smooth'])
  df['-DI'] = 100 * (df['-DM_smooth'] / df['TR_smooth'])

  # Calculate DX
  df['DX'] = 100 * (abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI']))

  # Calculate ADX
  df['ADX'] = df['DX'].rolling(window=n).mean()

  return df['ADX']

def calculate_ATR(high, low, close, period):
  tr1 = high - low
  tr2 = (high - close.shift(1)).abs()
  tr3 = (low - close.shift(1)).abs()
  tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
  atr = tr.ewm(alpha=1/period, adjust=False).mean()
  return atr
  