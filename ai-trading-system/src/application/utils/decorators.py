# importing time module
from time import time
class Timer:
    def __init__(self, func, test):
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
        
        print("Execution took {} seconds".format(end_time-start_time))
        return result
