import logging
from application.utils.discord_logger import Discord_Handler
from config.config import DISCORD_WEBHOOK
class LoggerClient:

    _config = None

    def __init__(self, config):
        self._config = config.LOG_CONFIG

    def get_logger(self):
        logger = logging.getLogger(self._config['name'])
        logger.setLevel(self._config['level'])
        log_handler = self._config['stream_handler']
        formatter = logging.Formatter(self._config['format'])
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        discord_handler = Discord_Handler(DISCORD_WEBHOOK)
        logger.addHandler(discord_handler)
        return logger
