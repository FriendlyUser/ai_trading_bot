class AlpacaRepository:
    def __init__(self, logger, config, alpaca_client):
        self._config = config
        self._logger = logger
        self._alpaca_client = alpaca_client

    def is_market_open(self):
        return self._alpaca_client.is_market_open()

    def buy_sell_stock(self, symbol, shares):
        return self._alpaca_client.buy_sell_stock(self, symbol, shares)

    def get_barset(self, symbol, interval, limit):
        return self._alpaca_client.get_barset(symbol, interval, limit)