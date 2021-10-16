import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from ai_trading_bot.application.utils.util import fig_to_buffer
from ai_trading_bot.application.utils.msg_manager import send_image
def get_finance_data(stock="^GSPC", period='5d', interval="1m"):
    """Get data from yahoo finance for a particular ticker"""

    ticker = yf.Ticker(stock)
    df = ticker.history(period=period, interval=interval)
    df['plt_date'] = df.index
    df['date'] = pd.to_datetime(df.index).time
    df.set_index('date', inplace=True)
    return df

data = get_finance_data("^GSPC", '5d', '15m')
plt.plot(data["plt_date"], data["Close"])
fig = plt.gcf()
data = fig_to_buffer(fig)
send_image(data)