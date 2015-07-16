from app import models, db


def get_columns_model_record():
    columnCollection = models.CdrRecord.__table__.columns

    columns = []
    for c in columnCollection._all_columns:
        column = {
            'key': c.key,
            'info_name': None if 'name' not in c.info else c.info['name'],
            'type': str(c.type)
        }
        columns.append(column)
    return columns