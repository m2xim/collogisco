#!/usr/bin/env python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

__version__ = 'pre-alpha___tc_VERSION__'

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

def get_version_app():
    return __version__

from app import views, models
