import logging
from flask import Flask, render_template
app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/')
def index():
  """simple index page"""
  return render_template("index.html")