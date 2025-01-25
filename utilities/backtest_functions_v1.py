import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import warnings
import yfinance as yf
warnings.filterwarnings("ignore")

# df must have index as date, and 'signal' column
# for day freq trading only
# if 'return_forward_1d' is not present, it will be fetched automatically
def run_backtest(df):

  # ------------------ Data check ------------------
  if df['signal'].isnull().values.any():
    raise ValueError("DataFrame contains NA values")
  if 'signal' not in df.columns:
    raise ValueError("DataFrame is missing required column: 'signal'")
  if 'return_forward_1d' not in df.columns:
    df = concat_return(df)

  # ------------------ Average Return & Sharpe ------------------
  # Calculate daily returns
  df['strategy_return'] = df['signal'] * df['return_forward_1d']

  # Overall Geometric Annual Return and Sharpe Ratio
  num_days = len(df)
  annual_return = (1 + df['strategy_return']).prod()**(365/num_days) - 1

  daily_std = df['strategy_return'].std()
  annual_std = daily_std * np.sqrt(365)
  overall_sharpe = annual_return / annual_std

  print(f"Overall Annual Return: {round(annual_return*100, 2)}%")
  print("Overall Annual Sharpe Ratio:", round(overall_sharpe, 4))

  # ------------------ Maximum Drawdown ------------------
  df['cum_return'] = (1 + df['strategy_return']).cumprod()
  rolling_max = df['cum_return'].cummax()
  df['drawdown'] = (df['cum_return'] - rolling_max) / rolling_max
  max_drawdown = df['drawdown'].min()
  print("Maximum Drawdown:", round(max_drawdown * 100, 2), "%")

  # ------------------ Win/Loss Ratio ------------------
  # Count the number of winning vs losing days
  winning_trades = (df['strategy_return'] > 0).sum()
  losing_trades = (df['strategy_return'] < 0).sum()
  if losing_trades > 0:
    win_loss_ratio = winning_trades / losing_trades
  else:
    win_loss_ratio = np.nan # no losing trades (advoid division by zero)
  print("Win/Loss Ratio:", round(win_loss_ratio, 2))

  # ------------------ Alpha and Beta ------------------
  # Beta = Cov(strategy_return, return_forward_1d) / Var(return_forward_1d)
  cov_matrix = np.cov(df['strategy_return'], df['return_forward_1d'])
  beta = cov_matrix[0, 1] / cov_matrix[1, 1]

  # Alpha = mean(strategy_return) - Beta * mean(return_forward_1d)
  alpha_daily = df['strategy_return'].mean() - beta * df['return_forward_1d'].mean()

  # Annualize alpha
  alpha_annualized = (1 + alpha_daily) ** 365 - 1

  print("Alpha:", round(alpha_annualized, 4))
  print("Beta:", round(beta, 4))

  # ------------------- Yearly Metrics -------------------
  df['year'] = df.index.year

  yearly_data = df.groupby('year').apply(lambda subdf: pd.Series({
    'yearly_return': (1 + subdf['strategy_return']).prod()**(365/len(subdf)) - 1,
    'yearly_std': subdf['strategy_return'].std() * np.sqrt(365),
    'yearly_beta': np.cov(subdf['strategy_return'], subdf['return_forward_1d'])[0,1] /
                    np.cov(subdf['strategy_return'], subdf['return_forward_1d'])[1,1],
    'yearly_alpha': (
      subdf['strategy_return'].mean()
      - (
        np.cov(subdf['strategy_return'], subdf['return_forward_1d'])[0,1]
        / np.cov(subdf['strategy_return'], subdf['return_forward_1d'])[1,1]
      )
      * subdf['return_forward_1d'].mean()
    ) * 365
  })).reset_index()

  yearly_data['yearly_sharpe'] = yearly_data['yearly_return'] / yearly_data['yearly_std']
  print("\nYearly Metrics:")
  print(yearly_data)

  # ------------------------- Plots ----------------------
  df['cum_return_plot'] = (1 + df['strategy_return']).cumprod() - 1
  df['bh_cum_return_plot'] = (1 + df['return_forward_1d']).cumprod() - 1

  # cumulative return plot
  plt.figure(figsize=(8,4))
  plt.plot(df.index, df['cum_return_plot'], label='Strategy Return')
  plt.plot(df.index, df['bh_cum_return_plot'], label='Buy and Hold')
  plt.title('Strategy Cumulative Return')
  plt.xlabel('Date')
  plt.ylabel('Cumulative Return')
  plt.legend()
  plt.show()

  # Signal weight plot
  plt.figure(figsize=(8,4))
  plt.plot(df.index, df['signal'], label='Signal')
  plt.title('Signal Weight Over Time')
  plt.xlabel('Date')
  plt.ylabel('Weight')
  plt.legend()
  plt.show()

def fetch_bitcoin_return_daily():
  price_df = yf.download("BTC-USD", interval="1d", start='2015-01-01', end='2025-01-02')
  price_df = price_df.xs('Close', level='Price', axis=1)
  price_df.columns = ['price']
  price_df['daily_return'] = price_df['price'].pct_change()
  price_df['return_forward_1d'] = price_df['daily_return'].shift(-1)
  price_df.drop(columns=['price', 'daily_return'], inplace=True)
  price_df = price_df[:-1]
  if len(price_df) == 0:
    print("Failed: fetch_bitcoin_return_daily")
    print("length of price dataframe = 0")
  price_df.to_parquet('btc_return_daily.parquet')

def concat_return(df):
  file_path = "btc_return_daily.parquet"
  if os.path.exists(file_path):
    df_btc_return = pd.read_parquet(file_path)
  else:
    fetch_bitcoin_return_daily()
    df_btc_return = pd.read_parquet(file_path)
  merged_df = pd.merge(df, df_btc_return, left_index=True, right_index=True, how='inner')
  return merged_df