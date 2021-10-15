import sys
import os
sys.path.insert(0,'..')
sys.path.insert(0,'../../..')
sys.path.insert(0,'../../')
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from application.clients.logger_client import LoggerClient
from application.clients.ta_client import TAClient
from config import config
# content of test_sample.py
def sample_func():
    logger = LoggerClient(config)
    taClient = TAClient(logger,config)
    df = taClient.stock_ta_for_cat("aapl", "momentum")
    df_interest = df[["RSI_14", "RSX_14", "RVGI_14_4", "ROC_10"]]
    last_row = df_interest.iloc[[-1]]


def generate_test():
    sample_func()
    assert True