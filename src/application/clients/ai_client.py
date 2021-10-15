import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

class AIClient:
    def __init__(self, logger, config):
        self._config = config
        self._logger = logger

    def get_forecast(self, finance_data):
        self._logger.info('Calculating forecast with the given data...')
        # Assuming that we've properly trained the model before and that the 
        # hyperparameters are correctly tweaked, we use the full dataset to fit

        # add more logic to catch errors
        y = finance_data['Low'].values
        model = ARIMA(y, order=(5,0,1)).fit()
        forecast = model.forecast(steps=1)[0]
        # byte indicies must be intergers or slices not str
        # Returning the last real data and the forecast for the next minute
        return (y[len(y)-1], forecast)