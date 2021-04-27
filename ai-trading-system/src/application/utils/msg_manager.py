import logging
import requests
import json
from config.config import DISCORD_WEBHOOK
from application.utils.state import get_loop_count, set_loop_count
from threading import Timer

# list of records to send to discord
record_list: list = []

def get_list():
    global record_list
    return record_list

def handle_add_record(record: logging.LogRecord):
    global record_list
    # max list length, convert all records to discord embeds
    if len(record_list) >= 4:
      send_msgs_to_discord(record_list)
      reset_list()
      return None
    if record == None:
      return None
    record_list.append(record)


def reset_list():
    global record_list
    record_list = []

# send what records are available and clear list
def reset_and_send_list():
    global record_list
    send_msgs_to_discord(record_list)
    reset_list()

def map_record_to_embed(record: logging.LogRecord):
  color = map_log_level_to_color(record.levelname)
  # title = f"{record.module} - {record.funcName}"
  title = f"{record.filename} - (L.{record.lineno}) | {record.funcName}"
  embed = {
    "color": color,
    "title": title,
    "timestamp": record.asctime,
    "description": record.getMessage()
  }
  fields = []
  # map args to field
  if type(record.args) == dict:
    # grab attached files
    # assume files are attached as base64 data
    args = record.args
    # assume one image for log record at most
    if "file" in args:
      embed["file"] = [args.file]
    del args["file"]
    for name, value in args.items():
      field = {
        "name": name,
        "value": value,
        "inline": "true"
      }
      fields.append(field)
    print(fields)
    embed["fields"] = fields
  return embed 

# sends image to correct chat service
def send_image(image: str, name: str = 'file'):
  url = DISCORD_WEBHOOK
  loop_count = get_loop_count()
  delay = loop_count * 2
  t = Timer(delay, post_image_to_discord, [image, name])
  t.start()
  set_loop_count(loop_count+1)

# TODO update name to reflect how it should work
def send_msgs_to_discord(record_list: list):
  # map each record 
  url = DISCORD_WEBHOOK
  embeds = []
  for record in record_list:
    embed = map_record_to_embed(record)
    embeds.append(embed)
  loop_count = get_loop_count()
  delay = loop_count * 2
  t = Timer(delay, post_webhook_content, [url, embeds])
  t.start()
  set_loop_count(loop_count+1)

def post_image_to_discord(url: str, file: str, filename):
  url = url
  result = requests.post(
      url, files=dict(filename: file)
  )

  try:
      result.raise_for_status()
  except requests.exceptions.HTTPError as err:
      print(err)
  else:
      print("Payload delivered successfully, code {}.".format(result.status_code))

# TODO add emergency logging
def post_webhook_content(url: str, embeds: list):
    url = url
    data = {}
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data["embeds"] = embeds

    result = requests.post(
        url, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

# TODO hardcode colors, move elsewhere later
def map_log_level_to_color(level: str):
  switcher = {
        'DEBUG': "11119017",
        'INFO': "29647",
        "WARNING": "16774656",
        "ERROR": "7350627",
        "CRITICAL": "14876706",
        "BUY": "52377",
        "SELL": "11737883",
        "ALERT": "99BADD",
    }
  return switcher.get(level, "29647")