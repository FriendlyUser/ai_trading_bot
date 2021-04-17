from time import time
class Timer:
    def __init__(self, func):
        self.function = func
  
    def __call__(self, *args, **kwargs):
        start_time = time()
        result = self.function(*args, **kwargs)
        end_time = time()
        print("Execution took {} seconds".format(end_time-start_time))
        return result

class CheckMarketOpen:
    def __init__(self, func):
        self.function = func
  
    def __call__(self, *args, **kwargs):
        parent_obj = args[0]
        market_open = parent_obj._alpaca_repository.is_market_open()
        print(market_open)
        return market_open