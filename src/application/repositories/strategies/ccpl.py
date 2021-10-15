import numpy as np
import os


class CPPI:
     """
        The CPPI algorithm class.
        """

       def __init__(self, logger, alpaca_repository, risky_asset: str, cppi_budget: int,
                     safe_asset: str = None, floor_percent: float = 0.8,
                     asset_muliplier: int = 3):
            """

            :param assets :(str) the ticker symbols of the risky assets to
                           invest in. E.g. : 'AAPL' or 'GS'
            :param cppi_budget :(int) the budget to be allocated to CPPI
                                algorithm.
            :param safe_asset :(str) the safe asset ticker symbol. Default is
                                None and will keep the safe allocation as cash
                                in the trading account.
            :param floor_percent :(float) this will be the floor percentage
                                   that the CPPI will try to maintain. Default
                                  is 80% of the initial budget.
            :param asset_muliplier :(int) the risky  asset  multiplier  for the
                                    CPPI. This is  the risk aversion parameter
                                    and usually it is set between 3 and 6.
                                    Default is 3.
            """
            # repositories
            self._logger = logger
            self._alpaca_repository = alpaca_repository
            # set the CPPI strategy params
            self.risky_asset = risky_asset
            self.safe_asset = safe_asset
            self.cppi_value = cppi_budget
            self.floor_percent = floor_percent
            self.floor_value = cppi_budget * floor_percent
            self.m = asset_muliplier
            self.max_cppi_value = cppi_budget
            self.position_value = None
            # check if the account permits the given budget
            self._check_budget(cppi_budget)
            # open a csv file to store the cppi metrics
            self.savefile = f'{risky_asset}_cppi.csv'
            if not os.path.exists(self.savefile):
                with open(self.savefile, 'w', newline='') as file:
                    wr = csv.writer(file)
                    # initialize the header
                    header = ['cppi value', 'floor']
                    wr.writerow(header)

        def _check_budget(self, required_capital: float):
            """
            A function that checks if the current account value 
            meets the CPPI budget.
            """
            available_cash = float(api.get_account().cash)
            if required_capital > available_cash:
                # TODO log instead?
                raise Exception("Not enough available cash")

        def run(self, period_in_days: int = 1):
            """
            Start the CPPI algorithm.

            :param period_in_days :(int) rebalancing period in days.
                                Default is 1 day.
            """
            self._check_market_open()
            # check if any positions already exists for the risky asset
            _, _ = self._check_position()
            while True:
                self.max_cppi_value = max(self.max_cppi_value, self.cppi_value)
                self.floor_value = self.max_cppi_value*self.floor_percent
                # calculate the cushion
                cushion = self.cppi_value - self.floor_value
                # compute the allocations towards safe and risky assets
                risk_alloc = max(min(self.m*cushion, self.cppi_value), 0)
                safe_alloc = self.cppi_value - risk_alloc
                # order the allocation
                self.rebalance(risk_alloc, safe_alloc)
                # sleep till next rebalancing.
                time.sleep(period_in_days*24*60*60)
                self._check_market_open()
                # re-calculate the CPPI value based on the asset holding returns
                risky_ret, safe_ret = self._check_position()
                self.cppi_value = risk_alloc*(1 + risky_ret) + safe_alloc*
                (1 + safe_ret)
                # save the tracking metrics
                self.save_cppi_metrics()

        def run_strategy(self):
            """
            Runs CPPI algorithm.

            the rebalancing will occur the next time the run function is called, should happen
            based on the loop counter
            """
            _, _ = self._check_position()
            self.max_cppi_value = max(self.max_cppi_value, self.cppi_value)
            self.floor_value = self.max_cppi_value*self.floor_percent
            # calculate the cushion
            cushion = self.cppi_value - self.floor_value
            # compute the allocations towards safe and risky assets
            risk_alloc = max(min(self.m*cushion, self.cppi_value), 0)
            safe_alloc = self.cppi_value - risk_alloc
            # order the allocation
            self.rebalance(risk_alloc, safe_alloc)
            # TODO implement delayed jobs somehow?
            # DB data?
            # For now re-calculate instantly
            # sleep till next rebalancing.
            # time.sleep(period_in_days*24*60*60)
            # re-calculate the CPPI value based on the asset holding returns
            risky_ret, safe_ret = self._check_position()
            self.cppi_value = risk_alloc*(1 + risky_ret) + safe_alloc*
            (1 + safe_ret)
            # save the tracking metrics
            self.save_cppi_metrics()

        def place_order(self, symbol: str, dollar_amount: float):
            """
            A function that places a market order in Alpaca based on the
            dollar amount to buy (e.g. $1000) or short (e.g. -$1000)
            for the given asset symbol.
            """
            if np.sign(dollar_amount) > 0:
                side = 'buy'
            elif np.sign(dollar_amount) < 0:
                side = 'sell'
            current_asset_price = api.get_last_trade(symbol).price
            qty = int(abs(dollar_amount) / current_asset_price)
            if qty > 0:
                self._alpaca_repository.buy_sell_stock(side, symbol, qty)


def rebalance(self, risk_alloc: float, safe_alloc: float):
    """
    This function will check if any rebalancing is required based on the
    recent CPPI risk budget allocation.
    """
    if self.position_value is None:
        # long the entire budget
        self.place_order(self.risky_asset, risk_alloc)
        # buy the safe asset also if given
        if self.safe_asset is not None:
            self.place_order(self.safe_asset, safe_alloc)
        else:
            # get the excess risk allocation
            excess_risk_alloc = risk_alloc - self.position_value[0]
            excess_safe_alloc = safe_alloc - self.position_value[1]
            # check if rebalancing is required
            if abs(excess_risk_alloc) > 0:
                # rebalance the risky asset
                self.place_order(self.risky_asset, excess_risk_alloc)
                # rebalance the safe asset if available
                if self.safe_asset is not None:
                    self.place_order(self.safe_asset, excess_safe_alloc)

    def _check_position(self):
        """
        A function to retrieve the current position value and return of
        risky and safe assets.
        """
        risky_position, risky_ret = self.get_position_value(self.risky_asset)
        if risky_position is not None:
        if self.safe_asset is not None:
            safe_position, safe_ret = self.get_position_value(self.safe_asset)
            if safe_position is not None:
                # both position exists
                self.position_value = [risky_position, safe_position]
            else:
                # safe asset position doesn't exists
                self.position_value = [risky_position, 0]
                safe_ret = 0

        elif self.safe_asset is not None:
            safe_position, safe_ret = self.get_position_value(self.safe_asset)
            if safe_position is not None:
                # only safe asset position exists
                self.position_value = [0, safe_position]
                risk_ret = 0
        else:
            # no position exists for either
            self.position_value = None
            risky_ret = 0
        return risky_ret, safe_ret

    def save_cppi_metrics(self):
        # TODO change to send metrics to the app
        with open(savefile, 'w', newline='') as file:
            wr = csv.writer(file)
            wr.writerow([self.cppi_value, self.floor_value])
        # send to discord via function
