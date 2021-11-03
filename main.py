"""
Main App logic
"""
import asyncio
import aiohttp

from ai_trading_bot.server import app
from ai_trading_bot.config import config
# TODO import from clients, use __init__.py
from ai_trading_bot.application.clients.logger_client import LoggerClient
from ai_trading_bot.application.clients.yahoo_client import YahooClient
from ai_trading_bot.application.clients.alpaca_client import AlpacaClient
from ai_trading_bot.application.clients.ai_client import AIClient
from ai_trading_bot.application.clients.ta_client import TAClient
# TODO import from repositories, use __init__.py
from ai_trading_bot.application.repositories.yahoo_repository import YahooRepository
from ai_trading_bot.application.repositories.alpaca_repository import AlpacaRepository
from ai_trading_bot.application.repositories.ai_repository import AIRepository
from ai_trading_bot.application.repositories.ta_repository import TARepository
from ai_trading_bot.application.actions.trading_system import TradingSystem
from ai_trading_bot.application import __version__
# from ai_trading_bot.application.utils.util import read_disk_image
# from ai_trading_bot.application.utils.msg_manager import send_image

class Container:
    """Has access to all repositories and logger"""
    def __init__(self):
        self._logger = LoggerClient(config).get_logger()
        self._logger.info("AI trading system starting...", {"version": __version__})

        self._yahoo_client = YahooClient(self._logger, config)
        self._yahoo_repository = YahooRepository(self._logger, config, self._yahoo_client)
        self._ai_client = AIClient(self._logger, config)
        self._ai_repository = AIRepository(self._logger, config, self._ai_client)
        self._alpaca_client = AlpacaClient(self._logger, config)
        self._alpaca_repository = AlpacaRepository(self._logger, config, self._alpaca_client)
        self._ta_client = TAClient(self._logger, config)
        self._ta_repository = TARepository(self._logger, config, self._ta_client)
        self._trading_system = TradingSystem(
            self._logger, config, self._yahoo_repository, 
            self._ai_repository, self._alpaca_repository, 
            self._ta_repository
        )

    async def start_monitoring(self):
        await self._trading_system.monitoring(config.POLLING_CONFIG['yahoo_interval'], exec_on_start=True)

if __name__ == '__main__':
    container = Container()
    asyncio.run(container.start_monitoring())
