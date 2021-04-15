import logging
import requests
import json
from threading import Timer
from logging import Handler
from application.utils.msg_manager import handle_add_record

class Discord_Handler(Handler):

    def __init__(self, url):
        logging.Handler.__init__(self)
        self.url = url

    def mapLogRecord(self, record):
        return record.__dict__

    def emit(self, record):
        self.emitting(record)

    # TODO add logic to add data to queue 
    def emitting(self, record):
        handle_add_record(record)
