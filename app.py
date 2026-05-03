from flask import Flask, render_template,send_from_directory, request, jsonify, Response
import os, json
from hashlib import sha1
import csv 
from datetime import datetime
from handlers.util import (
    ALL_QUESTION_METADATA_FILE
)

from handlers.ui import bp as ui_bp 
from handlers.api import bp as api_bp

app = Flask(__name__)
app.register_blueprint(ui_bp, url_prefix='/')
app.register_blueprint(api_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

