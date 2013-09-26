import os

config = {
    # We don't really want to *run* datanommer, but we do want
    # access to its DB.
    'datanommer.enabled': False,
    # This is generally not safe.. you probably want to use a real DB.
    'datanommer.sqlalchemy.url': 'sqlite:////tmp/datanommer.db',

    # Enable this to enable the datagrepper job runner.
    'fedmsg.consumers.datagrepper-runner.enabled': True,

    'datagrepper.flask.base_url': 'http://localhost:5000/',
    'datagrepper.openid.endpoint': 'https://id.fedoraproject.org/',
    # Flask secret key -- you will want to change this
    'datagrepper.flask.secret_key': 'change me',
    # datagrepper database, for storing job info and whatnot
    'datagrepper.sqlalchemy.url': 'sqlite:////tmp/datagrepper.db',
    # dogpile.cache backend and options
    'datagrepper.cache.backend': 'dogpile.cache.memory',
    'datagrepper.cache.kwargs': {},
    # Job runner config
    'datagrepper.runner.lockfile': os.path.join(os.getenv('HOME'), '.datagrepper_lockfile'),
    'datagrepper.runner.output_dir': os.path.join(os.getenv('HOME'), 'datagrepper_output'),
    'datagrepper.runner.output_url': 'file://' + os.path.join(os.getenv('HOME'), 'datagrepper_output'),
    'datagrepper.runner.job_expiry': 7 * 86400,
}
