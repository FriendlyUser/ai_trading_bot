import asyncio

import pandas as pd
import numpy as np

from statsmodels.tsa.arima.model import ARIMA


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

        while True:
            self._logger.info("Running main logic")
            market_open = self._alpaca_repository.is_market_open()
            if market_open:
                # run some main logic here
                self._logger.info("Main loop goes here")
            else: 
                self._logger.info("MARKET IS CLOSED")
            await asyncio.sleep(seconds)
