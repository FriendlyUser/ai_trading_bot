import logging
import os
import sys


LOG_CONFIG = {
    'name': 'ai-trading-bridge',
    'level': logging.DEBUG,
    'stream_handler': logging.StreamHandler(sys.stdout),
    'format': '%(asctime)s: %(module)s: %(levelname)s: %(message)s'
}

POLLING_CONFIG = {
    # 'yahoo_interval': 3000,
    'yahoo_interval': 60,
}

ALPACA_CONFIG = {
    'key_id': os.environ['ALPACA_KEY_ID'],
    'secret_key': os.environ['ALPACA_SECRET_KEY'],
    # Change to https://api.alpaca.markets for live
    'base_url': 'https://paper-api.alpaca.markets'
}

DISCORD_WEBHOOK = os.environ["DISCORD_TRADING_WEBHOOK"]