#/usr/bin/env python3
#
from time import time
from functools import wraps

def Timer(func):
    """ Times 
    """
    def _decorator(self, *args, **kwargs):
        # access a from TestSample
        start_time = time()
        result = func(self, *args, **kwargs)
        end_time = time()
        # util function to map seconds to nice format
        self._logger.buy("Execution took {} seconds".format(end_time-start_time))
        return result
    return _decorator


# def Timer(method):
#     @wraps(method)
#     async def _impl(self, *method_args, **method_kwargs):
#         start_time = time()
#         method_output = await method(self, *method_args, **method_kwargs)
#         end_time = time()
#     return _impl

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
