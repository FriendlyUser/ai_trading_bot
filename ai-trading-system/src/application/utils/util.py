import logging
from application.utils.msg_manager import reset_and_send_list
from application.utils.loop_count import reset_loop_count
from application.clients.logger_client import LoggerClient
from config import config

def reset():
  reset_loop_count()
  reset_and_send_list()

def getLogger():
  log_config = config.LOG_CONFIG
  logger = logging.getLogger(log_config['name'])
  return LoggerClient.setup_logger(log_config, logger)