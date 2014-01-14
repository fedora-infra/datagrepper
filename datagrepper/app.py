# datagrepper - HTTP API for datanommer and the fedmsg bus
# Copyright (C) 2013  Red Hat, Inc. and others
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
import json
import flask
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy

from bunch import Bunch
import codecs
import docutils
import docutils.examples
import dogpile.cache
from functools import wraps
import jinja2
import markupsafe
import os
import time
import traceback

from datetime import datetime
import fedmsg
import fedmsg.meta
import fedmsg.config
import datanommer.models as dm

from datagrepper.dataquery import DataQuery
from datagrepper.util import assemble_timerange, request_wants_html, message_card, meta_argument

app = flask.Flask(__name__)
app.config.from_object('datagrepper.default_config')
app.config.from_envvar('DATAGREPPER_CONFIG')

# Set up session secret key
app.secret_key = app.config['SECRET_KEY']

# Set up datagrepper database
db = SQLAlchemy(app)
from datagrepper.models import Job, STRSTATUS

# Set up OpenID
oid = OpenID(app)

# Read in the datanommer DB URL from /etc/fedmsg.d/ (or a local fedmsg.d/)
fedmsg_config = fedmsg.config.load_config()
fedmsg.meta.make_processors(**fedmsg_config)

# Initialize a datanommer session.
dm.init(fedmsg_config['datanommer.sqlalchemy.url'])

# Initialize the cache.
cache = dogpile.cache.make_region().configure(
    app.config.get('DATAGREPPER_CACHE_BACKEND', 'dogpile.cache.memory'),
    **app.config.get('DATAGREPPER_CACHE_KWARGS', {})
)


@app.before_request
def check_auth():
    flask.g.auth = Bunch(
        logged_in=False,
        method=None,
        id=None,
    )
    if 'openid' in flask.session:
        flask.g.auth.logged_in = True
        flask.g.auth.method = u'openid'
        flask.g.auth.id = flask.session.get('openid', None)


@oid.after_login
def after_openid_login(resp):
    if 'openid_error' in flask.session:
        message = dict(flask.g.auth)
        message['error'] = flask.session['openid_error']
        return flask.Response(
            response=fedmsg.encoding.dumps(message),
            status=400,
            mimetype='application/json',
        )
    flask.session['openid'] = resp.identity_url
    return flask.redirect(flask.url_for('auth_status'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not flask.g.auth.logged_in:
            return flask.Response(
                response=fedmsg.encoding.dumps({'error': 'no_auth'}),
                status=400,
                mimetype='application/json',
            )
        return f(*args, **kwargs)
    return decorated_function


def modify_rst(rst):
    """ Downgrade some of our rst directives if docutils is too old. """

    try:
        # The rst features we need were introduced in this version
        minimum = [0, 9]
        version = map(int, docutils.__version__.split('.'))

        # If we're at or later than that version, no need to downgrade
        if version >= minimum:
            return rst
    except Exception:
        # If there was some error parsing or comparing versions, run the
        # substitutions just to be safe.
        pass

    # Otherwise, make code-blocks into just literal blocks.
    substitutions = {
        '.. code-block:: javascript': '::',
    }
    for old, new in substitutions.items():
        rst = rst.replace(old, new)

    return rst


def modify_html(html):
    """ Perform style substitutions where docutils doesn't do what we want.
    """

    substitutions = {
        '<tt class="docutils literal">': '<code>',
        '</tt>': '</code>',
    }
    for old, new in substitutions.items():
        html = html.replace(old, new)

    return html


def preload_docs(endpoint):
    """ Utility to load an RST file and turn it into fancy HTML. """

    here = os.path.dirname(os.path.abspath(__file__))
    fname = os.path.join(here, 'docs', endpoint + '.rst')
    with codecs.open(fname, 'r', 'utf-8') as f:
        rst = f.read()

    rst = modify_rst(rst)

    api_docs = docutils.examples.html_body(rst)

    api_docs = modify_html(api_docs)

    api_docs = markupsafe.Markup(api_docs)
    return api_docs

htmldocs = dict.fromkeys(['index', 'reference'])
for key in htmldocs:
    htmldocs[key] = preload_docs(key)


def load_docs(request):
    URL = app.config.get('DATAGREPPER_BASE_URL', request.url_root)
    docs = htmldocs[request.endpoint]
    docs = jinja2.Template(docs).render(URL=URL)
    return markupsafe.Markup(docs)


@app.route('/')
def index():
    total = dm.Message.grep()[0]
    return flask.render_template('index.html', docs=load_docs(flask.request), total=total)


@app.route('/reference/')
@app.route('/reference')
def reference():
    return flask.render_template('index.html', docs=load_docs(flask.request))


# Instant requests
@app.route('/raw/')
@app.route('/raw')
def raw():
    """ Main API entry point. """

    # Perform our complicated datetime logic
    start = flask.request.args.get('start', None)
    end = flask.request.args.get('end', None)
    delta = flask.request.args.get('delta', None)
    start, end, delta = assemble_timerange(start, end, delta)

    # Further filters, all ANDed together in CNF style.
    users = flask.request.args.getlist('user')
    packages = flask.request.args.getlist('package')
    categories = flask.request.args.getlist('category')
    topics = flask.request.args.getlist('topic')

    # Paging arguments
    page = int(flask.request.args.get('page', 1))
    rows_per_page = int(flask.request.args.get('rows_per_page', 20))
    order = flask.request.args.get('order', 'asc')
    # adding size as paging arguments
    size = flask.request.args.get('size', 'large')
    # adding chrome as paging arguments
    chrome = flask.request.args.get('chrome', 'true')
    # adding fedpkg as paging argument
    fedpkg = flask.request.args.get('fedpkg','false')

    # Response formatting arguments
    callback = flask.request.args.get('callback', None)
    meta = flask.request.args.getlist('meta')

    arguments = dict(
        start=start,
        delta=delta,
        end=end,
        users=users,
        packages=packages,
        categories=categories,
        topics=topics,
        page=page,
        rows_per_page=rows_per_page,
        order=order,
        meta=meta,
    )

    if page < 1:
        raise ValueError("page must be > 0")

    if rows_per_page > 100:
        raise ValueError("rows_per_page must be <= 100")

    if order not in ['desc', 'asc']:
        raise ValueError("order must be either 'desc' or 'asc'")

    # check size value
    if size not in ['small', 'medium', 'large']:
        raise ValueError("size must be in one of these 'small', 'medium' or 'large'")

    # checks chrome value
    if chrome not in ['true', 'false']:
        raise ValueError("chrome should be either 'true' or 'false'")

    # checks fedpkg value
    if fedpkg not in ['true', 'false']:
        raise ValueError("chrome should be either 'true' or 'false'")

    try:
        # This fancy classmethod does all of our search for us.
        total, pages, messages = dm.Message.grep(
            start=start and datetime.fromtimestamp(start),
            end=end and datetime.fromtimestamp(end),
            page=page,
            rows_per_page=rows_per_page,
            order=order,
            users=users,
            packages=packages,
            categories=categories,
            topics=topics,
        )

        # Convert our messages from sqlalchemy objects to json-like dicts
        messages = [msg.__json__() for msg in messages]
        if meta:
            for message in messages:
                message = meta_argument(message, meta)

        output = dict(
            raw_messages=messages,
            total=total,
            pages=pages,
            count=len(messages),
            arguments=arguments,
        )
        status = 200
    except Exception as e:
        output = dict(
            error=str(e),
            arguments=arguments,
        )

        # :D
        if app.config.get('DEBUG', False):
            output['tb'] = traceback.format_exc().split('\n')

        status = 500

    body = fedmsg.encoding.dumps(output)

    mimetype = flask.request.headers.get('Accept')

    if callback:
        mimetype = 'application/javascript'
        body = "%s(%s);" % (callback, body)

    # return HTML content else json
    if request_wants_html():
        # convert string into python dictionary
        obj = json.loads(body)
        # extract the messages
        raw_message_list = obj["raw_messages"]

        final_message_list = []

        for msg in raw_message_list:
            # message_card module will handle size
            message = message_card(msg, size)
            # add msg_id to the message dictionary
            if (msg["msg_id"] != None):
                message['msg_id'] = msg["msg_id"]
            final_message_list.append(message)

        if fedpkg == 'true':
            final = final_message_list[:5]
            final_message_list = final

        # removes boilerlate codes if chrome value is false
        if chrome == 'true':
            return flask.render_template("base.html", response=final_message_list, heading="Raw Messages")
        else:
            return flask.render_template("raw.html", response=final_message_list)

    else:
        return flask.Response(
            response=body,
            status = status,
            mimetype = mimetype,
        )


@app.route('/id/')
@app.route('/id')
def msg_id():
    if 'id' not in flask.request.args:
        flask.abort(400)
    msg = dm.Message.query.filter_by(msg_id=flask.request.args['id']).first()
    mimetype = flask.request.headers.get('Accept')

    # get paging argument for size and chrome
    size = flask.request.args.get('size', 'large')
    chrome = flask.request.args.get('chrome', 'true')
    # get paging argument for is_raw
    # is_raw checks if card comes from /raw url
    is_raw = flask.request.args.get('is_raw', 'false')

    meta = flask.request.args.getlist('meta')

    # check size value
    if size not in ['small', 'medium', 'large']:
        raise ValueError("size must be in one of these 'small', 'medium' or 'large'")
    # checks chrome value
    if chrome not in ['true', 'false']:
        raise ValueError("chrome should be either 'true' or 'false'")
    # checks is_raw value
    if is_raw not in ['true', 'false']:
        raise ValueError("is_raw should be either 'true' or 'false'")

    if msg:
        # converts message from sqlalchemy objects to json-like dicts
        msg = msg.__json__()
        if meta:
            msg = meta_argument(msg, meta)

        if request_wants_html():
            # convert string into python dictionary
            obj = json.loads(fedmsg.encoding.dumps(msg))
            message = []
            if is_raw == 'true':
                message_dict = message_card(obj, size)
                message_dict['is_raw'] = 'true'
                message.append(message_dict)
            else:
                message.append(message_card(obj, size))

            if chrome=='true':
                return flask.render_template("base.html", response=message, heading="Message by ID")
            else:
                return flask.render_template("raw.html", response=message)

        else:
            return flask.Response (
                response=fedmsg.encoding.dumps(msg),
                status=200,
                mimetype=mimetype,
            )
    else:
        flask.abort(404)


@app.route('/messagecount/')
@app.route('/messagecount')
def messagecount():
    total = {}
    total['messagecount'] = dm.Message.grep()[0]
    total = flask.jsonify(total)
    return total


# Add a request job to the queue
@app.route('/submit/')
@app.route('/submit')
@login_required
def submit():
    try:
        job = Job(flask.g.auth,
                  DataQuery.from_request_args(flask.request.args))
        db.session.add(job)
        db.session.commit()
        fedmsg.publish(topic='job.new', msg=job)
        status = 200
        msg = {'id': job.id,
               'options': job.dataquery['options']}
    except ValueError as exc:
        msg = {'error': 'invalid_arg',
               'value': exc.message}
        status = 400
    return flask.Response(
        response=fedmsg.encoding.dumps(msg),
        status=status,
        mimetype='application/json',
    )


@app.route('/status/')
@app.route('/status')
def status():
    if 'id' not in flask.request.args:
        return flask.Response(
            response=fedmsg.encoding.dumps({'error': 'missing_argument',
                                            'argument': 'id'}),
            status=400,
            mimetype='application/json',
        )
    job = Job.query.get_or_404(flask.request.args['id'])
    msg = {'id': job.id, 'status': STRSTATUS[job.status]}
    if job.filename:
        msg['url'] = app.config['JOB_OUTPUT_URL'] + '/' + job.filename
    return flask.Response(
        response=fedmsg.encoding.dumps(msg),
        status=200,
        mimetype='application/json',
    )


@cache.cache_on_arguments(expiration_time=3600)
def topics_cached():
    msg = [i.topic for i in dm.Message.query.distinct(dm.Message.topic)]
    return fedmsg.encoding.dumps(msg)


@app.route('/topics/')
@app.route('/topics')
def topics():
    return flask.Response(
        response=topics_cached(),
        status=200,
        mimetype='application/json',
    )


@app.route('/auth/')
@app.route('/auth')
def auth_status():
    return flask.Response(
        response=fedmsg.encoding.dumps(flask.g.auth),
        status=200,
        mimetype='application/json',
    )


@app.route('/auth/openid/')
@app.route('/auth/openid')
@oid.loginhandler
def openid_login():
    if flask.g.auth.logged_in:
        return flask.redirect(flask.url_for('auth_status'))
    return oid.try_login(app.config['DATAGREPPER_OPENID_ENDPOINT'])


@app.route('/auth/logout/')
@app.route('/auth/logout')
def openid_logout():
    flask.session.pop('openid')
    return flask.redirect(flask.url_for('auth_status'))


@app.errorhandler(404)
def not_found(error):
    return flask.Response(
        response=fedmsg.encoding.dumps({'error': 'not_found'}),
        status=404,
        mimetype='application/json',
    )
