# simple forecast functions
class TARepository:
    def __init__(self, logger, config, ta_client):
        self._config = config
        self._logger = logger
        self._ta_client = ta_client

    def stock_ta_for_cat(self, stock: str = "aapl", category="momentum"):
        return self._ta_client.stock_ta_for_cat(stock, category)

    # returns the last row with all the TA characteristics
    def momentum_stock_ta(self, stock: str = "^GSPC"):
        df = self._ta_client.stock_ta_for_cat(stock, "momentum")
        df_interest = df[["RSI_14", "RSX_14", "RVGI_14_4", "ROC_10"]]
        last_row = df_interest.iloc[[-1]]
        return last_row

    # TODO momentum stock ta df - input df
