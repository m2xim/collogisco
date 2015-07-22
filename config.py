import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = '__KEY__'

# =============================================================================
# DataBase settings
# -----------------------------------------------------------------------------
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345678@127.0.0.1:5432/db_collogisco'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# =============================================================================

CDR_DATA_PATH = os.path.join(basedir, '_data')
CDR_DATA_FILENAME_MASK = 'cdr.*'

VIEW_FORMAT_DATETIME = '%H:%M:%S'
VIEW_LIMIT_VISIBLE_RECORDS = 1500

FORMAT_DATETIME_FILTER = '%H:%M:%S %d.%m.%Y'
