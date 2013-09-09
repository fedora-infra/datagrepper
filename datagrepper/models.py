from datagrepper.app import db

from datetime import datetime
import fedmsg
import json

STATUS_FREE = 0
STATUS_OPEN = 1
STATUS_DONE = 2
STATUS_FAILED = 3
STATUS_DELETED = 4

STRSTATUS = {
    STATUS_FREE: 'free',
    STATUS_OPEN: 'open',
    STATUS_DONE: 'done',
    STATUS_FAILED: 'failed',
    STATUS_DELETED: 'deleted',
}


class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    auth_method = db.Column(db.Unicode, nullable=False)
    auth_id = db.Column(db.Unicode, nullable=False)
    dataquery_json = db.Column(db.UnicodeText, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=STATUS_FREE)
    filename = db.Column(db.Unicode, nullable=True)
    request_time = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    complete_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, auth, dataquery):
        self.auth_method = auth.method
        self.auth_id = auth.id
        self.dataquery = dataquery.database_repr()
        self.request_time = datetime.now()

    def __json__(self):
        return dict(
            id=self.id,
            dataquery=self.dataquery,
            status=STRSTATUS[self.status],
            filename=self.filename,
            request_time=self.request_time,
            start_time=self.start_time,
            complete_time=self.complete_time,
        )

    def get_dataquery(self):
        return json.loads(self.dataquery_json)

    def set_dataquery(self, value):
        self.dataquery_json = json.dumps(value)

    def set_status(self, status, commit=True):
        if status == STATUS_OPEN:
            self.start_time = datetime.now()
        elif status in (STATUS_DONE, STATUS_FAILED):
            self.complete_time = datetime.now()
        self.status = status
        fedmsg.publish(topic='job.status.change',
                       msg={'status': STRSTATUS[status], 'job': self})
        db.session.add(self)
        db.session.commit()

    dataquery = property(get_dataquery, set_dataquery)
