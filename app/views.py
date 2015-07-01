import config
from flask import render_template, send_from_directory, abort, redirect
from app import app, get_version_app, models
import os
from utils import cdr

__base_path__ = os.path.dirname(os.path.abspath(__file__))


@app.route('/', methods=['GET'])
def index():
    cdrRecs = models.CdrRecord.query \
        .order_by(models.CdrRecord.unix_time.desc()) \
        .limit(config.VIEW_LIMIT_VISIBLE_RECORDS)

    return render_template(
        "_blocks/_b_main.html",
        cdr_records=cdrRecs,
        _version_=get_version_app()
    )


@app.route('/import', methods=['GET'])
def import_cdr():
    cdrParser = cdr.CDRParser()
    cdrParser.refresh_list_files()
    cdrSrc = models.CdrSource.query.order_by(models.CdrSource.dt_add.desc()).all()
    return render_template(
        "_blocks/_b_import.html",
        cdr_sources=cdrSrc,
        _version_=get_version_app()
    )


@app.route('/import/<int:source_id>', methods=['GET'])
def import_cdr_parse(source_id):
    cdrSrc = models.CdrSource.query.get(source_id)
    if cdrSrc is None:
        abort(404)
    cdrParser = cdr.CDRParser()
    cdrParser.parse(cdrSrc)
    return redirect('/import')


@app.route('/_static/<path:path>')
def send_static(path):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)) + '/../_static', path)
