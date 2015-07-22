import time
import datetime
from app import models
import config


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


class UCdrRecordFilter(object):
    def __init__(self):
        self.__filter_coll = None
        self.__columns = None
        self.__query = None

        self.__result = None

    def __reInit(self):
        self.__result = None
        self.__columns = get_columns_model_record()
        self.__query = models.db.session.query(models.CdrRecord)

    def build(self, filters_collection):
        self.__reInit()
        for f in filters_collection:
            cname = f['f']
            cond = f['c']
            val = f['v']

            t = self.__get_column_type(cname)

            if cond == '<':
                # ---- begin COND : <

                if t in ('BIGINT', 'INTEGER',):
                    self.__query = self.__query.filter(getattr(models.CdrRecord, cname) < int(val))
                elif t in ('DATETIME',):
                    dt_val = datetime.datetime.fromtimestamp(time.mktime(
                        time.strptime(val, config.FORMAT_DATETIME_FILTER)
                    ))
                    self.__query = self.__query.filter(getattr(models.CdrRecord, cname) < dt_val)

                pass
                # ---- end COND : <
            elif cond == '>':
                # ---- begin COND : >

                if t in ('BIGINT', 'INTEGER',):
                    self.__query = self.__query.filter(getattr(models.CdrRecord, cname) > int(val))
                elif t in ('DATETIME',):
                    dt_val = datetime.datetime.fromtimestamp(time.mktime(
                        time.strptime(val, config.FORMAT_DATETIME_FILTER)
                    ))
                    self.__query = self.__query.filter(getattr(models.CdrRecord, cname) > dt_val)

                pass
                # ---- end COND : <
            elif cond == '=':
                # ---- begin COND : =

                if t in ('BIGINT', 'INTEGER',):
                    self.__query = self.__query.filter(getattr(models.CdrRecord, cname) == int(val))
                elif t in ('VARCHAR(255)',):
                    self.__query = self.__query.filter(getattr(models.CdrRecord, cname) == val)

                pass
                # ---- end COND : =
            elif cond == '!=':
                # ---- begin COND : !=

                if t in ('BIGINT', 'INTEGER',):
                    self.__query = self.__query.filter(getattr(models.CdrRecord, cname) != int(val))

                pass
                # ---- end COND : !=
            elif cond == '<=':
                # ---- begin COND : <=

                if t in ('BIGINT', 'INTEGER',):
                    self.__query = self.__query.filter(getattr(models.CdrRecord, cname) <= int(val))

                pass
                # ---- end COND : <=
            elif cond == '>=':
                # ---- begin COND : >=

                if t in ('BIGINT', 'INTEGER',):
                    self.__query = self.__query.filter(getattr(models.CdrRecord, cname) >= int(val))

                pass
                # ---- end COND : >=
            elif cond == '%':
                # ---- begin COND : %

                if len(val) >= 2:
                    if val[:1] == '%':
                        val = '%' + val
                    elif val[-1:] == '%':
                        val += '%'

                    self.__query = self.__query.filter(getattr(models.CdrRecord, cname).like(val))
                pass
                # ---- begin COND : %
        self.__result = self.__query \
            .order_by(models.CdrRecord.unix_time.desc()) \
            .limit(config.VIEW_LIMIT_VISIBLE_RECORDS) \
            .all()
        return self.__result

    def __get_column_type(self, col_name):
        for c in self.__columns:
            if c['key'] == col_name:
                return c['type']
