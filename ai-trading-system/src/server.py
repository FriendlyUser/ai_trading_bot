from flask import Flask
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/')
def test():
    return "Hello World"