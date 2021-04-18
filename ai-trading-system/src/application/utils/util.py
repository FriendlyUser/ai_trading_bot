import logging
from application.utils.msg_manager import reset_and_send_list
from application.utils.loop_count import reset_loop_count
from application.clients.logger_client import LoggerClient
from config import config

def reset():
  reset_loop_count()
  reset_and_send_list()
