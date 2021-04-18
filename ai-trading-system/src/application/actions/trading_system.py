import asyncio

import pandas as pd
import numpy as np

from statsmodels.tsa.arima.model import ARIMA
from application.utils.util import reset
from application.decorators.trading import Timer, RunIfMarketOpen

class TradingSystem:
    def __init__(self, logger, config, yahoo_repository, ai_repository, alpaca_repository):
        
        self._config = config
        self._logger = logger
        self._yahoo_repository = yahoo_repository
        self._ai_repository = ai_repository
        self._alpaca_repository = alpaca_repository

        self._stocks = ["^GSPC"]

    async def monitoring(self, seconds, exec_on_start):
        if not exec_on_start:
            await asyncio.sleep(seconds)
        # load stocks from list
        while True:
            self._logger.info("Running main logic")
            self._logger.buy("Trying to buy stocks")
            await self.handle_trading()
            await asyncio.sleep(seconds)

    # its fine if decorators dont log to discord
    # right now they only perform timing and tracking
    @RunIfMarketOpen
    @Timer
    async def handle_trading(self):
        # scanning S&P 500
        for stock in self._stocks:
            data = self._yahoo_repository.get_finance_data(stock)
            result, forecast = self._ai_repository.get_forecast(data)
            if (abs(forecast - result) > 0.1):
                self._logger.info("S&P less than 0.05, preform trade")
        reset()
