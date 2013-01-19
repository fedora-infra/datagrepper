import flask
from flask.ext.fas import FAS
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config.from_object('datagrepper.default_config')
app.config.from_envvar('DATAGREPPER_CONFIG')

# set up SQLAlchemy
db = SQLAlchemy(app)

from datagrepper import models, util

# set up FAS
fas = FAS(app)


# Provide documentation of all topics from fedmsg.meta.
@app.route('/')
def index():
    if util.request_wants_json():
        return util.json_return({'error': 'Hello, world!'})
    return 'Hello, world!'


# Log the user in + woo cookies
@app.route('/login')
def login():
    pass


# Log the user out
@app.route('/logout')
def logout():
    pass


# Instant requests
@app.route('/raw')
def raw():
    pass


# Add a request job to the queue
@app.route('/submit')
def submit():
    pass
