# Bitcoin Systematic Trading Strategies

This project explores and implements systematic trading strategies for Bitcoin, utilizing market data, news sentiment, and social media data.

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
  * Historical price data (Open, High, Low, Close, Volume) for Bitcoin (BTC-USD) downloaded from [Kaggle Bitcoin Historical Data](https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data).
  * The market data was processed in varies data frequencies using the file `bitcoin_historical_price/process_1min_price_kaggle.ipynb`.
* **News Articles:**
  * Historical news articles were gathered from [Crypto News API](https://cryptonews-api.com/) using the file `crypto_news/data_processing/1.get_cryptonews_api.py` and saved in the folder `crypto_news/data/`.
* **Reddit Posts:**
  * xxxxxxxxxxxxxxxxxxxxxxxxxx

## Natural Language Processing (NLP)

Text data from news and Reddit is processed to extract valuable features:

* **Aspect-Based Sentiment Analysis (ABSA):** Analyzes sentiment towards specific aspects like 'economy', 'regulation', 'technology'. (See `crypto_news/data_processing/3.absa.ipynb`)
* **Named Entity Recognition (NER):** Identifies key entities like people, organizations, cryptocurrencies, and events. (See `crypto_news/data_processing/4b.ner.ipynb`)
* **Sentiment Analysis:** General sentiment scoring using models like VADER, FinBERT, or CryptoBERT. (See `crypto_news/data_processing/5.sentiment.ipynb`)
* **Topic:** Identifies prevalent topics discussed in the news articles. (See `crypto_news/data_processing/6.topic.ipynb`)

## Technical Analysis

Bitcoin price data from Kaggle (OHLC) in `bitcoin_historical_price`

* **Indicators:** Calculation done in `technical_indicators/ta_lib.ipynb` using daily and hourly data from `bitcoin_historical_price`.
  (Export file to `technical_indicators/btcusd_daily_price_indicators.parquet` for daily and `technical_indicators/btcusd_hourly_price_indicators.parquet` for hourly)
* **Feature Engineering:** Manual feature engineering (See `technical_indicators/feature_hourly.ipynb`, export full price dataset to `technical_indicators/btcusd_hourly_features.parquet`)
  
## Modelling

Various models are developed to generate trading signals (-1: Sell, 0: Hold, 1: Buy):

* **Statistical Models:** EWM-based strategies. (See `modeling_backtesting/statistical/`)
* **Rule-based strategies:** Initiation of trading using technical indicators in daily frequency (See `technical_indicators/rule-based_strategies.ipynb`)


## Backtesting

Simulates and evaluates the performance of the trading strategies:

* **Strategy:** Hourly rebalancing portfolio with short sell enabled.
* **Framework:** `utilities/backtest_functions_v2.py`
* **Metrics:** Calculates Annual Return, Sharpe Ratio, Maximum Drawdown, Alpha, Beta, and provides yearly breakdowns.
* **Plotting:** Simulate portfolio returns and plot the cumulative return graph.
* **Functionality:** Handles different data frequencies and calculates returns based on signals and forward returns.

## Key Findings

* Alternative dataset (news and social media) demonstrated market predictive ability and delivered superior risk-adjusted returns (Sharpe>3.0)
* LLM-based approaches, specifically aspect-based sentiment analysis, performed exceptionally well in extracting nuanced features from textual data.
* Machine learning capture patterns more effectively than statistical approach. In the project, random forest classifier yieded the best perfomanace.
* Subsequent phase of this research should focus on enhancing model performance by exploring deep learning methodologies tailored to limited data volume.
