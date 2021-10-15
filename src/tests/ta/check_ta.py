import sys
sys.path.insert(0,'..')
from application.clients.logger_client import LoggerClient
from application.clients.ta_client import TAClient
from config import config
logger = LoggerClient(config)
taClient = TAClient(logger,config)

df = taClient.stock_ta_for_cat("aapl", "momentum")
df.to_csv('read.csv')
df_interest = df[["RSI_14", "RSX_14", "RVGI_14_4", "ROC_10"]]
last_row = df_interest.iloc[[-1]]
print(last_row)
print(last_row["RSI_14"][0])