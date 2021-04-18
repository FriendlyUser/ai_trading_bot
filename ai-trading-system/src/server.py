from flask import Flask, render_template
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/')
def index():
  """simple index page"""
  return render_template("index.html")