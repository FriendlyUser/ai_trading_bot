import logging
from application.utils.discord_logger import Discord_Handler
from config.config import DISCORD_WEBHOOK

DEBUG_LEVEL_BUY_NUM = 10
DEBUG_LEVEL_SELL_NUM = 11
DEBUG_LEVEL_ALERT_NUM = 12
def buy(self, message, *args, **kws):
    if self.isEnabledFor(DEBUG_LEVEL_BUY_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(DEBUG_LEVELV_NUM, message, args, **kws) 

def sell(self, message, *args, **kws):
    if self.isEnabledFor(DEBUG_LEVEL_SELL_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(DEBUG_LEVELV_NUM, message, args, **kws) 

def alert(self, message, *args, **kws):
    if self.isEnabledFor(DEBUG_LEVEL_ALERT_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(DEBUG_LEVELV_NUM, message, args, **kws) 

class LoggerClient:

    _config = None

    def __init__(self, config):
        self._config = config.LOG_CONFIG
        # TODO add custom logging
        logging.addLevelName(DEBUG_LEVEL_BUY_NUM, "BUY")
        logging.Logger.buy = buy
        logging.addLevelName(DEBUG_LEVEL_SELL_NUM, "SELL")
        logger.Logger.sell = sell
        logging.addLevelName(DEBUG_LEVEL_ALERT_NUM, "ALERT")
        logger.Logger.alert = alert

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
