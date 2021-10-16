import logging
import os
import sys
import random

LOG_CONFIG = {
    'name': 'ai-trading-bridge',
    'level': logging.INFO,
    'stream_handler': logging.StreamHandler(sys.stdout),
    'format': '%(asctime)s: %(module)s: %(levelname)s: %(message)s'
}

POLLING_CONFIG = {
    # 'yahoo_interval': 3000,
    'yahoo_interval': 60*20,
}

ALPACA_CONFIG = {
    'key_id': os.environ.get('ALPACA_KEY_ID'),
    'secret_key': os.environ.get('ALPACA_SECRET_KEY'),
    # Change to https://api.alpaca.markets for live
    'base_url': 'https://paper-api.alpaca.markets'
}


TRADING_CONFIG = {
    'DEBUG': True
}

DISCORD_WEBHOOK = os.environ.get("DISCORD_TRADING_WEBHOOK")

PORT = 8080