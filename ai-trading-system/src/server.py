from flask import Flask, render_template
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/')
def index():
  return render_template("index.html")