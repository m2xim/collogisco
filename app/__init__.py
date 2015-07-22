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

from utils import cdr

app.jinja_env.globals.update(decode_time_dif=cdr.decode_time_dif)
app.jinja_env.globals.update(enumerate=enumerate)
app.jinja_env.globals.update(int=int)
app.jinja_env.globals.update(cls_cdr_record=models.CdrRecord)
