from datetime import datetime
import fedmsg
import fedmsg.consumers
try:
    from lockfile import LockFile
except ImportError:
    from lockfile import FileLock as LockFile
import os

from datagrepper.app import app, db
from datagrepper.dataquery import DataQuery
import datagrepper.models as dgrepm
from datagrepper.models import Job


class DatagrepperRunnerConsumer(fedmsg.consumers.FedmsgConsumer):
    config_key = 'fedmsg.consumers.datagrepper-runner.enabled'

    def __init__(self, hub):
        self.hub = hub
        self.topic = self.hub.config.get('topic_prefix', 'org.fedoraproject')
        self.topic += '.' + self.hub.config.get('environment')
        self.topic += '.datagrepper.job.new'
        super(DatagrepperRunnerConsumer, self).__init__(hub)

    def consume(self, msg):
        print "****** STARTING CONSUME"
        # ignore the message, we do what we want
        lock = LockFile(app.config['RUNNER_LOCKFILE'])
        with lock:
            # get list of open jobs
            while True:
                jobs = Job.query.filter_by(status=dgrepm.STATUS_FREE)
                if jobs.count() == 0:
                    break
                for job in jobs:
                    # run query on jobs
                    dq = DataQuery.from_database(job)
                    job.set_status(dgrepm.STATUS_OPEN)
                    try:
                        job.filename = dq.run_query(
                            'datagrepper_{0}'.format(job.id))
                    except:
                        job.set_status(dgrepm.STATUS_FAILED)
                    else:
                        job.set_status(dgrepm.STATUS_DONE)
            # get list of completed jobs to be deleted
            jobs = Job.query.filter(
                Job.status == dgrepm.STATUS_DONE,
                Job.complete_time < (datetime.now() - app.config['JOB_EXPIRY'])
            )
            for job in jobs:
                os.remove(os.path.join(app.config['JOB_OUTPUT_DIR'],
                                       job.filename))
                job.set_status(dgrepm.STATUS_DELETED)
        print "****** FINISHING CONSUME"
