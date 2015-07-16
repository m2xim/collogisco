import csv
from datetime import datetime
import glob
import os
from app import models, db
import config


class CDRParser(object):
    def __init__(self):
        self.__cdr_path = config.CDR_DATA_PATH

    def run(self):
        pass

    def refresh_list_files(self):
        listing = glob.glob(os.path.join(self.__cdr_path, config.CDR_DATA_FILENAME_MASK))
        for f in listing:
            f = os.path.basename(f)
            cdrSrcDB = models.CdrSource.query.filter(models.CdrSource.filename == f).all()
            if len(cdrSrcDB) == 0:
                cdrSrc = models.CdrSource()
                cdrSrc.filename = f
                cdrSrc.dt_add = datetime.now()
                cdrSrc.is_parsed = False
                db.session.add(cdrSrc)
                db.session.commit()

    def parse(self, cdrSource):

        if cdrSource.is_parsed:
            return True

        cdr_fpath = os.path.join(self.__cdr_path, cdrSource.filename)
        csv_file = open(cdr_fpath)
        csv_read = csv.reader(csv_file, delimiter=',', quotechar='"')
        for csv_line in csv_read:
            if len(csv_line) < 23:
                continue

            cdrRec = models.CdrRecord()
            cdrRec.source = cdrSource.id
            # ---- CDR DATA ----
            cdrRec.unix_time = self.__fix_int(csv_line[models.CdrRecord.unix_time.info['col']])
            cdrRec.username = self.__fix_str(csv_line[models.CdrRecord.username.info['col']])
            cdrRec.peer_address = self.__fix_str(csv_line[models.CdrRecord.peer_address.info['col']])
            cdrRec.alert_time = self.__fix_datetime(csv_line[models.CdrRecord.alert_time.info['col']])
            cdrRec.clid = self.__fix_str(csv_line[models.CdrRecord.clid.info['col']])
            cdrRec.dnis = self.__fix_str(csv_line[models.CdrRecord.dnis.info['col']])
            cdrRec.h323_connect_time = self.__fix_datetime(csv_line[models.CdrRecord.h323_connect_time.info['col']])
            cdrRec.h323_disconnect_time = self.__fix_datetime(
                csv_line[models.CdrRecord.h323_disconnect_time.info['col']])
            cdrRec.h323_disconnect_cause = \
                self.__fix_int(csv_line[models.CdrRecord.h323_disconnect_cause.info['col']], 16)
            cdrRec.info_type = self.__fix_int(csv_line[models.CdrRecord.info_type.info['col']])
            if cdrRec.h323_disconnect_time is not None and cdrRec.h323_connect_time is not None:
                cdrRec.time_dif = (cdrRec.h323_disconnect_time - cdrRec.h323_connect_time).seconds

            db.session.add(cdrRec)
        cdrSource.is_parsed = True
        cdrSource.dt_import = datetime.now()
        db.session.add(cdrSource)
        db.session.commit()
        csv_file.close()
        return True

    def __fix_str(self, s):
        s = s.strip()
        if len(s) == 0:
            s = None
        return s

    def __fix_int(self, s, base=10):
        s = self.__fix_str(s)
        if s is not None:
            s = int(s, base)
        return s

    def __fix_datetime(self, s):
        if s[:1] is '*':
            s = s[1:]
        s = self.__fix_str(s)
        if s is not None:
            try:
                # TODO: This BIG crutch!!! :) TimeZone -> Moscow??? F*ck!
                s = datetime.strptime(s, '%H:%M:%S.%f Moscow %a %b %d %Y')
            except Exception as e:
                print e
                return None
        return s


def decode_time_dif(time_dif):
    m, s = divmod(time_dif, 60)
    h, m = divmod(m, 60)
    if time_dif == 0:
        result = ''
    elif h != 0:
        result = '%d:%02d:%02d' % (h, m, s)
    else:
        result = '%02d:%02d' % (m, s)
    return result
