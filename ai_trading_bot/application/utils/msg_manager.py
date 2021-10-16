import logging
import requests
import json
from config.config import DISCORD_WEBHOOK
from ai_trading_bot.application.utils.state import get_loop_count, increment_loop_count
from threading import Timer

# list of records to send to discord
record_list: list = []

def get_list():
    global record_list
    return record_list

def handle_add_record(record: logging.LogRecord):
    global record_list
    # max list length, convert all records to discord embeds
    if len(record_list) >= 8:
      # split errors and non errors
      # split errors and messages
      error_list, other_list = split_record_by_category(record_list)
      send_msgs_to_discord(error_list)
      send_msgs_to_discord(other_list)
      reset_list()
      return None
    if record == None:
      return None
    record_list.append(record)


def split_record_by_category(input_record_list: list, category_list: list = ["ERROR"]):
  category_list = [r for r in input_record_list if r.levelname in category_list]
  other_list = [r for r in input_record_list if r.levelname not in category_list]
  return category_list, other_list

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
    for name, value in record.args.items():
      field = {
        "name": name,
        "value": value,
        "inline": "true"
      }
      fields.append(field)
    embed["fields"] = fields
  return embed 

# sends image to correct chat service
def send_image(image: str, name: str = 'file.png'):
  """ sends buffer image to discord
  """
  url = DISCORD_WEBHOOK
  loop_count = get_loop_count()
  delay = loop_count * 5
  t = Timer(delay, post_image_to_discord, [url, image, name])
  t.start()
  increment_loop_count()

# TODO update name to reflect how it should work
def send_msgs_to_discord(record_list: list, url = DISCORD_WEBHOOK):
  if len(record_list) == 0:
    return
  # map each record 
  embeds = []
  # split errors into another list
  for record in record_list:
    embed = map_record_to_embed(record)
    embeds.append(embed)
  loop_count = get_loop_count()
  delay = loop_count * 5
  t = Timer(delay, post_webhook_content, [url, embeds])
  t.start()
  increment_loop_count()

def post_image_to_discord(url: str, file: str, filename: str = 'file'):
  url = url
  result = requests.post(
      url, files={filename: file}
  )

  try:
      result.raise_for_status()
  except requests.exceptions.HTTPError as err:
      print(err)
  else:
      print("Image Delivered {}.".format(result.status_code))

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
        "PLOT": "	15299665"
    }
  return switcher.get(level, "29647")