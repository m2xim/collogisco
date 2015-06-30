import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = '__KEY__'

# =============================================================================
# DataBase settings
# -----------------------------------------------------------------------------
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345678@127.0.0.1:5432/collogisco_dev'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# =============================================================================
