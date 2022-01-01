import asyncio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from ai_trading_bot.application.utils.util import reset, fig_to_buffer
from ai_trading_bot.application.decorators.trading import Timer, RunIfMarketOpen, RunFuncAndHandleException
from ai_trading_bot.application.utils.state import increment_counter, get_counter
from ai_trading_bot.application.utils.msg_manager import send_image
from ai_trading_bot.application.actions.event_system import EventSystem
class TradingSystem:
    def __init__(self, logger, config, 
        yahoo_repository, ai_repository, 
        alpaca_repository,
        ta_repository
        ):
        
        self._config = config
        self._logger = logger
        self._yahoo_repository = yahoo_repository
        self._ai_repository = ai_repository
        self._alpaca_repository = alpaca_repository
        self._stocks = ["APPL"]
        self._ta_repository = ta_repository
        self._event_system = EventSystem(logger, config, yahoo_repository, ai_repository, alpaca_repository, ta_repository)

    async def monitoring(self, seconds, exec_on_start):
        if not exec_on_start:
            await asyncio.sleep(seconds)
        # load stocks from list
        while True:
            self._logger.info("[monitoring][main loop]")
            await self.handle_trading()
            await asyncio.sleep(seconds)

    # its fine if decorators dont log to discord
    # right now they only perform timing and tracking
    @RunIfMarketOpen
    @Timer
    # TODO consider moving RUNFUNCANDHANDLEEXCEPTION PER STOCK
    # CHANGE CONFIGURATION FOR STOCKS
    @RunFuncAndHandleException
    async def handle_trading(self):
        # scanning S&P 500
        # change configuration to run different analysis based on config
        for stock in self._stocks:
            APPLE_DATA = self._alpaca_repository.get_barset(stock, 'day', limit=100).df
            APPLE_DATA['20_SMA'] = APPLE_DATA['close'].rolling(window=20, min_periods=1).mean()
            APPLE_DATA['10_SMA'] = APPLE_DATA['close'].rolling(window=10, min_periods=1).mean()
            APPLE_DATA['Cross'] = 0.0
            APPLE_DATA['Cross'] = np.where(APPLE_DATA['10_SMA'] > APPLE_DATA['20_SMA'], 1.0, 0.0)
            APPLE_DATA['Signal'] = APPLE_DATA['Cross'].diff()
            map_dict = {-1.0: 'sell', 1.0: 'buy', 0.0: 'none'}
            APPLE_DATA["Signal"] = APPLE_DATA["Signal"].map(map_dict)
            # get last 5 entries in apple data df
            last_5_entries = APPLE_DATA.tail(5)
            # check if signal has buy or sell
            if "buy" in last_5_entries['Signal'].values:
                # buy stock
                self._logger.info("[handle_trading][buy]")
                await self._alpaca_repository.buy_sell_stock("buy", stock, 10)
                self._logger.sell(f"{stock} - {10}", {
                    "price": f"{last_5_entries['close'].values[-1]}",
                })

            if "sell" in last_5_entries['Signal'].values:
                self._logger.info("[handle_trading][buy]")
                await self._alpaca_repository.buy_sell_stock("sell", stock, 10)
                self._logger.sell(f"{stock} - {10}", {
                    "price": f"{last_5_entries['close'].values[-1]}",
                })

        # forecasting stonk price
        # for stock in self._stocks:
        #     data = self._yahoo_repository.get_finance_data(stock)
        #     result, forecast = self._ai_repository.get_forecast(data)
        #     if (abs(forecast - result) > 0.1):
        #         # TODO add percent difference
        #         self._logger.info("S&P less than 0.05, preform trade", {
        #             "forecast": f"{forecast:.2f}",   
        #             "result": f"{result:.2f}",
        #         })

        reset()
        increment_counter()
        await self.handle_timed_events()

    # handles events that occur on each iteration
    async def handle_timed_events(self):
        counter = get_counter()
        indicies = ["^IXIC", "^RUT", "DOW"]
        if counter % 2 == 0:
            for index in indicies:
                plt_data = await self._event_system.plot_index(index)
                send_image(plt_data)
                await self._event_system.get_ta_for_ticker(index)
                # perform ta analysis
            pass
        else:
            pass
        if counter % 5 == 0:
            pass
        pass

