from datagrepper import app, db

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
    query_json = db.Column(db.UnicodeText, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=STATUS_FREE)
    filename = db.Column(db.Unicode, nullable=True)
    request_time = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    complete_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, dataquery):
        self.query = dataquery.database_repr()

    @property
    def query(self):
        return json.loads(self.query_json)

    @query.setter
    def set_query(self, value):
        self.query_json = json.dumps(value)
