from datagrepper.app import db

from datetime import datetime
import json

STATUS_FREE = 0
STATUS_OPEN = 1
STATUS_DONE = 2
STATUS_FAILED = 3
STATUS_DELETED = 4


class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    dataquery_json = db.Column(db.UnicodeText, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=STATUS_FREE)
    filename = db.Column(db.Unicode, nullable=True)
    request_time = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    complete_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, dataquery):
        self.dataquery = dataquery.database_repr()
        self.request_time = datetime.now()

    def get_dataquery(self):
        return json.loads(self.dataquery_json)

    def set_dataquery(self, value):
        self.dataquery_json = json.dumps(value)

    dataquery = property(get_dataquery, set_dataquery)
