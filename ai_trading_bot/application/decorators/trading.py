#/usr/bin/env python3
import traceback
import sys
import os
from time import time
from ai_trading_bot.application.utils.util import prettify_time, reset
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
        msg = f"Execution of {func.__name__} took {nice_time}"
        # self._logger.debug(msg)
        return result
    return _decorator


def RunIfMarketOpen(func):
    async def _decorator(self, *args, **kwargs):
        # access a from TestSample
        market_open = self._alpaca_repository.is_market_open()
        trading_cfg = self._config.TRADING_CONFIG
        if market_open or trading_cfg.get('DEBUG', False):
            result = await func(self, *args, **kwargs)
            return result
        else:
            # return empty function
            def fun(): 
                pass
            return fun
    return _decorator

def RunFuncAndHandleException(func):
    async def _decorator(self, *args, **kwargs):
        try:
            result = await func(self, *args, **kwargs)
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            func_name = func.__name__
            message = f"[HandleException][{func_name}]"
            self._logger.warning(message, {
                "error": str(e),
                "type": str(exc_type),
                'fname': str(fname)
            })
            reset()
            return None
    return _decorator
