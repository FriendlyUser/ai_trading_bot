import asyncio

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from application.utils.util import reset, fig_to_buffer
from application.decorators.trading import Timer, RunIfMarketOpen
from application.utils.state import increment_counter, get_counter
from application.utils.msg_manager import send_image
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
        # change configuration to run different analysis based on config   
        for stock in self._stocks:
            data = self._yahoo_repository.get_finance_data(stock)
            result, forecast = self._ai_repository.get_forecast(data)
            # parameterize forecasting
            # TODO calculate percentage difference
            plt.plot(data)
            fig = plt.gcf()
            data = fig_to_buffer(fig)
            send_image(data)
            if (abs(forecast - result) > 0.1):
                # TODO add percent difference
                self._logger.info("S&P less than 0.05, preform trade", {
                    "forecast": f"{forecast:.2f}",   
                    "result": f"{result:.2f}",
                })

        reset()
        increment_counter()
        await self.handle_timed_events()

    # handles events that occur on each iteration
    async def handle_timed_events(self):

        counter = get_counter()
        indicies = ["^IXIC", "^RUT", "DOW"]
        if counter % 10 == 0:
            for index in indicies:
                data = self._yahoo_repository.get_finance_data(stock)
                # TODO implement new system
                result, forecast = self._ai_repository.get_forecast(data)
                # TODO add percent difference
                self._logger.debug(f"*Event Index* - {index}", {
                    "forecast": f"{forecast:.2f}",   
                    "result": f"{result:.2f}",
                    "index": str(index)
                })
            pass
        if counter % 5 == 0:
            pass
        pass

