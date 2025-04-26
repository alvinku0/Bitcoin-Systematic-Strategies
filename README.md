# Bitcoin Systematic Trading Strategies

This project explores and implements systematic trading strategies for Bitcoin, utilizing market data, news articles, and social media posts.

## Project Structure Overview

The project is organized into several key components:

1. **Data Collection:** Gathering Bitcoin market data, news articles, and social media data.
2. **Natural Language Processing (NLP):** Processing text data from news and Reddit.
3. **Technical Analysis:** Deriving technical indicators from market data.
4. **Modelling:** Developing trading models using statistical methods, machine learning, and deep learning approaches.
5. **Backtesting:** Evaluating the performance of trading strategies based on model signals.
6. **Results:** Analyzing the outcomes of the backtested strategies.

## Data Collection

This section covers the acquisition of various data sources used for analysis and model building.

* **Bitcoin Market Data:**
  * Historical market data (Open, High, Low, Close, Volume) for Bitcoin (BTC-USD) were downloaded from [Kaggle Bitcoin Historical Data](https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data).
  * The market data was processed in various data frequencies using the file `bitcoin_historical_price/process_1min_price_kaggle.ipynb` and saved in the folder `bitcoin_historical_price/`.
* **News Articles:**
  * Historical news articles were gathered from [Crypto News API](https://cryptonews-api.com/) using the file `crypto_news/data_processing/1.get_cryptonews_api.py` and saved in the folder `crypto_news/data/1.cryptonews.parquet`.
* **Reddit Posts:**
  * Reddit dataset was obtained from [Academic Torrents](https://academictorrents.com/details/1614740ac8c94505e4ecb9d88be8bed7b6afddd4) and saved in `reddit/Reddit_scripts/Bitcoin_submissions.zst`.
  * `reddit/Reddit_scripts/filter_file.py` filtered out posts created between 2021/01/01 and 2024/12/31 and saved them to `reddit/reddit_hour_raw.parquet.gzip`.

## Natural Language Processing (NLP)

Text data from news and Reddit is processed to extract valuable features:

* **Aspect-Based Sentiment Analysis (ABSA):** Analyzes sentiment towards specific aspects like 'economy', 'regulation', 'technology'. (See `crypto_news/data_processing/3.absa.ipynb`)
* **Named Entity Recognition (NER):** Identifies key entities like people, organizations, cryptocurrencies, and events. (See `crypto_news/data_processing/4b.ner.ipynb`)
* **Sentiment Analysis:** Analyzes sentiment scoring using VADER, FinBERT, CryptoBERT. (See `reddit/reddit_sentiment.ipynb` and `crypto_news/data_processing/5.sentiment.ipynb`)
* **Topic Modeling:** Identifies prevalent topics discussed in the news articles. (See `crypto_news/data_processing/6.topic.ipynb`)

## Technical Analysis

Deriving technical indicators from Bitcoin market data (OHLC).

* **Indicators:** Calculates technical indicators such as moving averages, MACD, RSI, ADX, OBV, etc., in both hourly and daily frequency. (See `technical_indicators/ta_lib.ipynb`)
  * Exported files to `technical_indicators/btcusd_daily_price_indicators.parquet` and `technical_indicators/btcusd_hourly_price_indicators.parquet`.
* **Feature Engineering:** Creates additional features derived from technical indicators that capture trends, momentum, and volatility. (See `technical_indicators/feature_hourly.ipynb`, exported dataset to `technical_indicators/btcusd_hourly_features.parquet`)

## Modelling

Develops various models to generate trading signals.  
For models involving ML, they were all trained on 2021-2023 data and tested on 2024 data.

* **Statistical Models:** EWM-based strategies. (See `modeling_backtesting/statistical/`)
* **Rule-based strategies:** Initiates trading based on technical indicators rule-based signals. (See `technical_indicators/rule-based_strategies.ipynb`)
* **Logistic Regression Model:** `modeling_backtesting/LogisticRegression`
* **Random Forest Classifier:** `modeling_backtesting/RandomForestClassifier`
* **XGBoost Regressor:** `modeling_backtesting/XGBoostRegressor`
* **XGBoost Classifier:** `modeling_backtesting/XGBoostClassifier`
* **Deep Learning strategies:** Deep learning models, including LSTM, NBEATS, and Transformer. (See `modeling_backtesting/Deep Learning`)

## Backtesting

Simulates and evaluates the performance of the trading strategies:

* **Strategy:** Hourly rebalancing portfolio with short selling enabled.
* **Framework:** `utilities/backtest_functions_v2.py`
* **Metrics:** Calculates Annual Return, Sharpe Ratio, Maximum Drawdown, Alpha, Beta, and provides yearly breakdowns.
* **Plotting:** Simulates portfolio returns and plots the cumulative return graph.
* **Functionality:** Handles different data frequencies and calculates returns based on signals and forward returns.

## Key Findings

The Random Forest Classifier applied to alternative datasets (news and social media) achieved a Sharpe ratio of 3.0, an Annualized Percentage Yield (APY) of 185%, and a Maximum Drawdown of -24.89%.

* Alternative datasets (news and social media) demonstrated significant market predictive ability, delivering superior risk-adjusted returns.
* LLM-based approaches, specifically aspect-based sentiment analysis, performed exceptionally well in extracting nuanced features from textual data.
* Machine learning captured patterns more effectively than statistical approaches. In this project, the Random Forest Classifier yielded the best performance.
* Subsequent phase of this research should focus on enhancing model performance by exploring additional deep learning methodologies tailored to limited data volumes.

## Limitation

The following limitations should be considered when interpreting the results:

* **Backtesting Assumptions:** The backtesting framework operates under idealized conditions, excluding considerations for interest rates, transaction costs (fees and slippage), and execution latency. These factors could significantly impact real-world performance.
* **Data Quality:** Reliance on low-budget data sources introduced data quality issues, including missing values and anomalous price jumps, which may affect model robustness and backtesting accuracy.
* **Market Regime Shift:** The models were trained on 2021-2023 historical data and tested on 2024 data. Potential differences in market conditions between the training and testing periods may limit the generalizability of the findings.
