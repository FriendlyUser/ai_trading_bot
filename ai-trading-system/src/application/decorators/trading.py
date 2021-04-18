#/usr/bin/env python3
#
from time import time
from application.utils.util import prettify_time
from functools import wraps

def Timer(func):
    """ Time execution time
    """
    def _decorator(self, *args, **kwargs):
        # access a from TestSample
        start_time = time()
        result = func(self, *args, **kwargs)
        end_time = time()
        # util function to map seconds to nice format
        nice_time = prettify_time(end_time-start_time)
        msg = f"Execution of {func.__name__}took {nice_time}"
        self._logger.buy(msg)
        return result
    return _decorator


def RunIfMarketOpen(func):
    async def _decorator(self, *args, **kwargs):
        # access a from TestSample
        market_open = self._alpaca_repository.is_market_open()
        trading_cfg = self._config.TRADING_CONFIG
        if market_open or trading_cfg.get('DEBUG', False):
            self._logger.buy("Market open")
            result = await func(self, *args, **kwargs)
            return result
        else:
            self._logger.debug("Market closed")
            def fun(): 
                pass
            return fun
    return _decorator
