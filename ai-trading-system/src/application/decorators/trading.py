from time import time
#/usr/bin/env python3
from functools import wraps
from application.utils.util import getLogger

class TimerOld:
    def __init__(self, func):
        self.function = func
  
    def __call__(self, *args, **kwargs):
        start_time = time()
        result = self.function(*args, **kwargs)
        end_time = time()
        print("Execution took {} seconds".format(end_time-start_time))
        return result


def Timer(method):
    @wraps(method)
    async def _impl(self, *method_args, **method_kwargs):
        start_time = time()
        method_output = await method(self, *method_args, **method_kwargs)
        end_time = time()
    return _impl

class CheckMarketOpen:
    def __init__(self, func):
        self.function = func
  
    def __call__(self, *args, **kwargs):
        parent_obj = args[0]
        market_open = parent_obj._alpaca_repository.is_market_open()
        print(market_open)
        return market_open