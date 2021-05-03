import pandas as pd
import numpy as np
import pandas_ta as ta
from statsmodels.tsa.arima.model import ARIMA
# categories
# ['candles', 'cycles', 'momentum', 'overlap', 'performance', 'statistics', 'trend', 'volatility', 'volume']

#
#    'AO_5_34', 'APO_12_26', 'BIAS_SMA_26', 'BOP', 'AR_26', 'BR_26',
#    'CCI_14_0.015', 'CFO_9', 'CG_10', 'CMO_14', 'COPC_11_14_10', 'CTI_12',
#    'ER_10', 'BULLP_13', 'BEARP_13', 'FISHERT_9_1', 'FISHERTs_9_1',
#    'INERTIA_20_14', 'K_9_3', 'D_9_3', 'J_9_3',
#    'KST_10_15_20_30_10_10_10_15', 'KSTs_9', 'MACD_12_26_9',
#    'MACDh_12_26_9', 'MACDs_12_26_9', 'MOM_10', 'PGO_14', 'PPO_12_26_9',
#    'PPOh_12_26_9', 'PPOs_12_26_9', 'PSL_12', 'PVO_12_26_9', 'PVOh_12_26_9',
#    'PVOs_12_26_9', 'QQE_14_5_4.236', 'QQE_14_5_4.236_RSIMA',
#    'QQEl_14_5_4.236', 'QQEs_14_5_4.236', 'ROC_10', 'RSI_14', 'RSX_14',
#    'RVGI_14_4', 'RVGIs_14_4', 'SLOPE_1', 'SMI_5_20_5', 'SMIs_5_20_5',
#    'SMIo_5_20_5', 'SQZ_20_2.0_20_1.5', 'SQZ_ON', 'SQZ_OFF', 'SQZ_NO',
#    'STC_10_12_26_0.5', 'STCmacd_10_12_26_0.5', 'STCstoch_10_12_26_0.5',
#    'STOCHk_14_3_3', 'STOCHd_14_3_3', 'STOCHRSIk_14_14_3_3',
#    'STOCHRSId_14_14_3_3', 'TRIX_30_9', 'TRIXs_30_9', 'TSI_13_25',
#    'UO_7_14_28', 'WILLR_14'
class TAClient:
    def __init__(self, logger, config):
        self._config = config
        self._logger = logger

    # Grabs full data from yfinance
    def stock_ta_for_cat(self, stock: str, category: str):
        # OR if you have yfinance installed
        df = pd.DataFrame() # Empty DataFrame
        new_df = df.ta.ticker(stock)

        # Calculate Returns and append to the df DataFrame
        new_df.ta.strategy(category, append="true")

        return new_df

    # todo custom strategies with only the attributes I care about
