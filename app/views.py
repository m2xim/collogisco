from flask import render_template, send_from_directory
from app import app, get_version_app
import os

__base_path__ = os.path.dirname(os.path.abspath(__file__))


@app.route('/', methods=['GET'])
def index():
    return render_template(
        "base.html",
        _version_=get_version_app()
    )


@app.route('/_static/<path:path>')
def send_static(path):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)) + '/../_static', path)
