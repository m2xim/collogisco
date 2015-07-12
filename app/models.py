# coding=utf-8
from app import db


class CdrSource(db.Model):
    __tablename__ = 'cdr_source'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), index=True, nullable=False, unique=True)
    dt_add = db.Column(db.DateTime, nullable=False)
    dt_import = db.Column(db.DateTime, nullable=True)
    is_parsed = db.Column(db.Boolean, default=False, index=True)

    def __repr__(self):
        return '<cdrFile %r>' % self.id


class CdrRecord(db.Model):
    __tablename__ = 'cdr_records'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    source = db.Column(db.BigInteger, db.ForeignKey('cdr_source.id'))
    # ---- CDR DATA ----

    #  0    Long    System time stamp when CDR is captured.
    unix_time = db.Column(db.Integer, nullable=True, info={'col': 0, 'name': 'Unix time'}, index=True)  # 0
    # 20    String    Username for authentication. Usually this is the same as the calling number.
    username = db.Column(db.String(255), nullable=True, info={'col': 20, 'name': 'Username'}, index=True)  # 20
    #  5    String    Number that this call was connected to in E.164 format.
    peer_address = db.Column(db.String(255), nullable=True, info={'col': 5, 'name': 'Peer address'}, index=True)  # 5
    #  8    String    Time at which call is alerting.
    alert_time = db.Column(db.DateTime, nullable=True, info={'col': 8, 'name': 'Alert time'})  # 8
    # 21    String    Calling number.
    clid = db.Column(db.String(255), nullable=True, info={'col': 21, 'name': 'Calling number'}, index=True)  # 21
    # 22    String    Called number.
    dnis = db.Column(db.String(255), nullable=True, info={'col': 22, 'name': 'Called number'}, index=True)  # 22
    #  9    String    Connect time in NTP format
    h323_connect_time = db.Column(db.DateTime, nullable=True, info={'col': 9, 'name': 'Connect time'})  # 9
    # 10    String    Disconnect time in NTP format
    h323_disconnect_time = db.Column(db.DateTime, nullable=True, info={'col': 10, 'name': 'Disconnect time'})  # 10
    # 11    String    Q.931 disconnect cause code retrieved from Cisco IOS call-control app prog interface
    h323_disconnect_cause = db.Column(db.Integer, nullable=True, info={'col': 11, 'name': 'Disconnect cause'})  # 11
    # 15    String    Type of information carried by media.
    info_type = db.Column(db.String(255), nullable=True, info={'col': 15, 'name': 'Info Type'})  # 15

    # Diff h323_connect_time and h323_disconnect_time
    time_dif = db.Column(db.Integer, nullable=True, info={'name': 'Duration'})

    def __repr__(self):
        return '<cdrRecord %r>' % self.id
