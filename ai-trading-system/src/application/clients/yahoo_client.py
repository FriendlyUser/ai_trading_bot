import yfinance as yf
# TODO consider switching out yfinance with 
import pandas as pd


class YahooClient:
    def __init__(self, logger, config):
        self._config = config
        self._logger = logger

    def get_finance_data(self, stock="^GSPC", period='5d', interval="1m"):
        """Get data from yahoo finance for a particular ticker"""
        self._logger.info('Getting data from Yahoo Finance...')

        ticker = yf.Ticker(stock)
        df = ticker.history(period=period, interval=interval)
        self._logger.info(f'Data found. Last value dated on {df.index[-1]} for {stock}  ')
        df['date'] = pd.to_datetime(df.index).time
        df['plt_date'] = df.index
        df.set_index('date', inplace=True)
        return df
