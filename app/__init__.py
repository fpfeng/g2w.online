from flask import Flask

app = Flask(__name__)

from .utils import ListConverter

app.url_map.converters['list'] = ListConverter
