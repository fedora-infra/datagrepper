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

import flask
from flask.ext.sqlalchemy import SQLAlchemy

import codecs
import docutils
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
    for old, new in substitions.items():
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


def datetime_to_seconds(dt):
    """ Name this, just because its confusing. """
    return time.mktime(dt.timetuple())


def timedelta_to_seconds(td):
    """ Python 2.7 has a handy total_seconds method.
    If we're on 2.6 though, we have to roll our own.
    """

    if hasattr(td, 'total_seconds'):
        return td.total_seconds()
    else:
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6


@app.route('/')
def index():
    return flask.render_template('index.html', docs=load_docs(flask.request))


@app.route('/reference/')
@app.route('/reference')
def reference():
    return flask.render_template('index.html', docs=load_docs(flask.request))


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

    # Response formatting arguments
    callback = flask.request.args.get('callback', None)

    arguments = dict(
        start=datetime_to_seconds(start),
        delta=timedelta_to_seconds(delta),
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

    mimetype = 'application/json'

    if callback:
        mimetype = 'application/javascript'
        body = "%s(%s);" % (callback, body)

    return flask.Response(
        response=body,
        status=status,
        mimetype=mimetype,
    )


# Add a request job to the queue
#@app.route('/submit/')
#@app.route('/submit')
#def submit():
#    pass
