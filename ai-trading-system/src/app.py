import asyncio

from application.clients.logger_client import LoggerClient
from application.clients.yahoo_client import YahooClient
from application.clients.alpaca_client import AlpacaClient
from application.clients.ai_client import AIClient
from application.repositories.yahoo_repository import YahooRepository
from application.repositories.alpaca_repository import AlpacaRepository
from application.repositories.ai_repository import AIRepository
from application.actions.trading_system import TradingSystem
from application import __version__
from application.utils.util import read_disk_image
from application.utils.msg_manager import send_image
from threading import Timer
from server import app
from config import config
from application import __version__

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
        self._trading_system = TradingSystem(
            self._logger, config, self._yahoo_repository, self._ai_repository, self._alpaca_repository)

    async def start_monitoring(self):
        """Main loop to monitor stock market"""
        await self._trading_system.monitoring(config.POLLING_CONFIG['yahoo_interval'], exec_on_start=True)

def start_app():
    """start server app"""
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    container = Container()
    asyncio.run(container.start_monitoring())
