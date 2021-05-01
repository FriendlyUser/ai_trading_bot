# event system to process events
# for example, every 10 iterations
# analyze the S&P 500 and/or nasdaq
# or grab news from server
import asyncio

import pandas as pd
import numpy as np

from statsmodels.tsa.arima.model import ARIMA
from application.utils.util import reset
from application.decorators.trading import Timer, RunIfMarketOpen
from application.utils.state import increment_counter, get_counter
from application.utils.util import fig_to_buffer
from appication.actions.event_system import EventSystem
class EventSystem:
    def __init__(self, logger, config, yahoo_repository, ai_repository, alpaca_repository):
        
        self._config = config
        self._logger = logger
        self._yahoo_repository = yahoo_repository
        self._ai_repository = ai_repository
        self._alpaca_repository = alpaca_repository
        self._event_system = EventSystem(logger, config, yahoo_repository, ai_repository,alpaca_repository)

    # handles events that occur on each iteration
    async def handle_timed_events():
        counter = get_counter()
        if counter % 10 == 0:
            pass
        elif counter % 5 == 0:
            pass
        pass

    async def plot_index(stock: str):
        data = self._yahoo_repository.get_finance_data(index, '5d', '15m')
        plt.title(f"{index} - for 5 days")
        plt.plot(data["plt_date"], data["Close"])
        plt.xlabel(f"{stock}")
        plt.ylabel("Date")
        fig = plt.gcf()
        plt_data = fig_to_buffer(fig)
        return plt_data

