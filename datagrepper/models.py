from datagrepper import app, db

from datetime import datetime
import simplejson

STATUS_FREE = 0
STATUS_OPEN = 1
STATUS_DONE = 2


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Unicode(32), unique=True, nullable=False)
    query_json = db.Column(db.UnicodeText, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=STATUS_FREE)
    request_time = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    complete_time = db.Column(db.DateTime, nullable=True)

    @property
    def query(self):
        return simplejson.loads(self.query_json)

    @query.setter
    def set_query(self, value):
        self.query_json = simplejson.dumps(value)
