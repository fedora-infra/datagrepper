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
import traceback

from datetime import datetime

import fedmsg.config
import fedmsg.meta
import datanommer.models as dm

from datagrepper.util import assemble_timerange

app = flask.Flask(__name__)
app.config.from_object('datagrepper.default_config')
app.config.from_envvar('DATAGREPPER_CONFIG')

# Set up session secret key
app.secret_key = app.config['SECRET_KEY']

# This loads all the openid/user management stuff which is a work in progress.
#import datagrepper.users

# Read in the datanommer DB URL from /etc/fedmsg.d/ (or a local fedmsg.d/)
fedmsg_config = fedmsg.config.load_config()
fedmsg.meta.make_processors(**fedmsg_config)

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

    meta_expected = set(['title', 'subtitle', 'icon', 'secondary_icon',
                         'link', 'usernames', 'packages', 'objects'])
    if len(set(meta).intersection(meta_expected)) != len(set(meta)):
        raise ValueError("meta must be in %s"
                         % ','.join(list(meta_expected)))

    try:
        # This fancy classmethod does all of our search for us.
        total, pages, messages = dm.Message.grep(
            start=datetime.fromtimestamp(start),
            end=datetime.fromtimestamp(end),
            page=page,
            rows_per_page=rows_per_page,
            order=order,
            users=users,
            packages=packages,
            categories=categories,
            topics=topics,
        )

        # Convert our messages from sqlalchemy objects to json-like dicts
        messages = map(dm.Message.__json__, messages)

        if meta:
            for message in messages:
                metas = {}
                for metadata in meta:
                    cmd = 'msg2%s' % metadata
                    metas[metadata] = getattr(
                        fedmsg.meta, cmd)(message, **fedmsg_config)

                    # We have to do this because 'set' is not
                    # JSON-serializable.  In the next version of fedmsg, this
                    # will be handled automatically and we can just remove this
                    # statement https://github.com/fedora-infra/fedmsg/pull/139
                    if isinstance(metas[metadata], set):
                        metas[metadata] = list(metas[metadata])

                message['meta'] = metas

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
