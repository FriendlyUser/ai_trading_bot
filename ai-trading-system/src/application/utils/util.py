import logging
# importing matplotlib modules
import base64
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from application.utils.msg_manager import reset_and_send_list
from application.utils.state import reset_loop_count
from application.clients.logger_client import LoggerClient
from config import config
from io import BytesIO
def reset():
  """reset the loop iteration for messages and thread delays"""
  reset_loop_count()
  reset_and_send_list()

def prettify_time(time):
  """numeric time in seconds"""
  if time < 1e-6 and time > 1e-9:
    #
    return f"{time*1e6:.2} microseconds" 
    pass
  elif time < 1e-9:
    return f"{time*1e9:.2} nanoseconds"
  elif time < 1e-3 and time > 1e-6:
    return f"{time*1e3:.2} milliseconds"
    # millseconds string
  else:
    return f"{time:.2} seconds"

def read_disk_image():
  file_path = 'ai-trading-system/assets/HyunWoo_Avatar.png'
  with open(file_path, "rb") as image_file:
    encoded_string = image_file.read()
  return encoded_string

def fig_to_buffer(fig):
  buf = BytesIO()
  fig.savefig(buf, format='png')
  buf.seek(0)
  imgdata = buf.read()
  return imgdata

# Sample Code to send an image via discord
# def read_disk_image():
#   plt.plot(range(10, 20))
#   fig = plt.gcf()

#   buf = BytesIO()
#   fig.savefig(buf, format='png')
#   buf.seek(0)
#   imgdata = buf.read()
#   return imgdata