import asyncio

import pandas as pd
import numpy as np

from statsmodels.tsa.arima.model import ARIMA
from application.utils.util import reset

class TradingSystem:
    def __init__(self, logger, config, yahoo_repository, ai_repository, alpaca_repository):
        self._config = config
        self._logger = logger

        self._yahoo_repository = yahoo_repository
        self._ai_repository = ai_repository
        self._alpaca_repository = alpaca_repository

    async def monitoring(self, seconds, exec_on_start):
        if not exec_on_start:
            await asyncio.sleep(seconds)
        # load stocks from list
        stocks = ["^GSPC"]
        while True:
            self._logger.info("Running main logic")
            market_open = self._alpaca_repository.is_market_open()
            if market_open:
                # run some main logic here
                self._logger.info("Main loop goes here")
                # scanning S&P 500
                for stock in stocks:
                    data = self._yahoo_repository.get_finance_data(stock)
                    result, forecast = self._ai_repository.get_forecast(data)
                    if (abs(forecast - result) > 0.1):
                        self._logger.info("S&P less than 0.05, preform trade")
            else: 
                self._logger.warning("Market is closed")
            reset()
            await asyncio.sleep(seconds)
