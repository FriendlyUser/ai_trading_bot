import logging
import requests
import json
from logging import Handler
class Discord_Handler(Handler):

    def __init__(self, url):
        logging.Handler.__init__(self)
        self.url = url

    def mapLogRecord(self, record):
        return record.__dict__

    def emit(self, record):
        self.emitting(record)

    def emitting(self, record):
        try:
            msg = self.format(record)
            url = self.url
            data = self.mapLogRecord(record)
            #can't do anything with the result
            if len(msg) > 1900:
                msg_list = [msg[i: i+1900] for i in range(0, len(msg), 1900)]
                for i in msg_list:
                    self.post_webhook_content(i)
            else:
                self.post_webhook_content(msg)
        except Exception:
            self.handleError(record)

    def post_webhook_content(self, content: str):
        url = self.url
        data = {}
        # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
        data["content"] = f"```{content}```"

        result = requests.post(
            url, data=json.dumps(data), headers={"Content-Type": "application/json"}
        )

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(result.status_code))