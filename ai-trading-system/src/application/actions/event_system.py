# event system to process events
# for example, every 10 iterations
# analyze the S&P 500 and/or nasdaq
# or grab news from server
import matplotlib.pyplot as plt
from application.utils.state import get_counter
from application.utils.util import fig_to_buffer
from matplotlib.dates import DateFormatter, WeekdayLocator, MO, WE, FR
class EventSystem:
    def __init__(self, logger, config, yahoo_repository, ai_repository, alpaca_repository, ta_repository):
        
        self._config = config
        self._logger = logger
        self._yahoo_repository = yahoo_repository
        self._ai_repository = ai_repository
        self._alpaca_repository = alpaca_repository
        self._ta_repository = ta_repository

    # handles events that occur on each iteration
    async def handle_timed_events():
        counter = get_counter()
        if counter % 10 == 0:
            pass
        elif counter % 5 == 0:
            pass
        pass

    async def plot_index(self, stock: str):
        data = self._yahoo_repository.get_finance_data(stock, '5d', '15m')
        plt.plot(data["plt_date"], data["Close"])
        plt.title(f"{stock} - for 5 days")
        plt.ylabel(f"Price of {stock}")
        plt.xlabel("Date")
        fig = plt.gcf()
        ax = fig.get_axes()[0]
        # Define the date format
        date_form = DateFormatter("%m-%d")
        ax.xaxis.set_major_formatter(date_form)

        # Ensure a major tick for each week using (interval=1) 
        ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(MO, WE, FR)))
        fig = plt.gcf()
        plt_data = fig_to_buffer(fig)
        fig.clear()
        return plt_data

    async def get_ta_for_ticker(self, stock: str):
        df = self._ta_repository.momentum_stock_ta(stock)
        latest_rsi = df["RSI_14"][0]
        latest_roc = df["ROC_10"][0]
        # send logging to discord here
        self._logger.alert(f"{stock} - index", {
            "latest_rsi": f"{latest_rsi:.2f}",   
            "latest_roc": f"{latest_roc:.2f}",
        })
        return None

