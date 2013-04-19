import flask
from flask.ext.sqlalchemy import SQLAlchemy

import codecs
import docutils.examples
import jinja2
import markupsafe
import os
import time
from datetime import (
    datetime,
    timedelta,
)
import traceback

import fedmsg.config
import datanommer.models as dm

app = flask.Flask(__name__)
app.config.from_object('datagrepper.default_config')
app.config.from_envvar('DATAGREPPER_CONFIG')

# Set up session secret key
app.secret_key = app.config['SECRET_KEY']

# This loads all the openid/user management stuff which is a work in progress.
#import datagrepper.users

# Read in the datanommer DB URL from /etc/fedmsg.d/ (or a local fedmsg.d/)
fedmsg_config = fedmsg.config.load_config()

# Initialize a datanommer session.
dm.init(fedmsg_config['datanommer.sqlalchemy.url'])


def load_docs():
    """ Utility to load API.rst and turn it into fancy HTML. """

    here = os.path.dirname(os.path.abspath(__file__))
    fname = here + '/API.rst'
    with codecs.open(fname, 'r', 'utf-8') as f:
        rst = f.read()

    # TODO -- pull this from the flask config
    URL = "api.fedoraproject.org/datagrepper"

    api_docs = docutils.examples.html_body(rst)
    api_docs = jinja2.Template(api_docs).render(URL=URL)

    # Some style substitutions where docutils doesn't quite do what we want.
    substitutions = {
        '<tt class="docutils literal">': '<code>',
        '</tt>': '</code>',
        '<h1>': '<h3>',
        '</h1>': '</h3>',
    }

    for old, new in substitutions.items():
        api_docs = api_docs.replace(old, new)

    api_docs = markupsafe.Markup(api_docs)
    return api_docs

api_docs = load_docs()


def datetime_to_seconds(dt):
    """ Name this, just because its confusing. """
    return time.mktime(dt.timetuple())


@app.route('/')
def index():
    return flask.render_template('index.html', api_documentation=api_docs)


# Instant requests
@app.route('/raw/')
@app.route('/raw')
def raw():
    """ Main API entry point. """

    # Complicated combination of default start, end, delta arguments.
    now = datetime_to_seconds(datetime.now())
    end = datetime.fromtimestamp(
        float(flask.request.args.get('end', now)))

    delta = timedelta(
        seconds=float(flask.request.args.get('delta', 600)))

    then = datetime_to_seconds(end - delta)
    start = datetime.fromtimestamp(
        float(flask.request.args.get('start', then))
    )

    # Further filters, all ANDed together in CNF style.
    users = flask.request.args.getlist('user')
    packages = flask.request.args.getlist('package')
    categories = flask.request.args.getlist('category')
    topics = flask.request.args.getlist('topic')

    # Paging arguments
    page = int(flask.request.args.get('page', 1))
    rows_per_page = int(flask.request.args.get('rows_per_page', 20))

    arguments = dict(
        start=datetime_to_seconds(start),
        delta=delta.total_seconds(),
        end=datetime_to_seconds(end),
        users=users,
        packages=packages,
        categories=categories,
        topics=topics,
        page=page,
        rows_per_page=rows_per_page,
    )

    if page < 1:
        raise ValueError("page must be > 0")

    if rows_per_page > 100:
        raise valueError("rows_per_page must be <= 100")

    try:
        # This fancy classmethod does all of our search for us.
        total, pages, messages = dm.Message.grep(
            start=start,
            end=end,
            page=page,
            rows_per_page=rows_per_page,
            users=users,
            packages=packages,
            categories=categories,
            topics=topics,
        )

        output = dict(
            raw_messages=messages,
            total=total,
            pages=pages,
            count=len(messages),
            arguments=arguments,
        )
        status = "200 OK"
    except Exception as e:
        output = dict(
            error=str(e),
            arguments=arguments,
        )

        # :D
        if app.config.get('DEBUG', False):
            output['tb'] = traceback.format_exc().split('\n')

        status = "500 error"

    body = fedmsg.encoding.dumps(output)
    return flask.Response(
        response=body,
        status=status,
        mimetype='application/json',
    )


# Add a request job to the queue
#@app.route('/submit/')
#@app.route('/submit')
#def submit():
#    pass
