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
import codecs
import itertools
import json
import os
import re
import traceback
from datetime import datetime, timedelta

import arrow
import datanommer.models as dm
import docutils
import docutils.examples
import flask
import jinja2
import markupsafe
import pygal
import pygments
import pygments.formatters
import pygments.lexers
from flask import Flask
from flask_healthz import HealthError, healthz
from pkg_resources import get_distribution
from werkzeug.exceptions import BadRequest

from datagrepper.util import (
    as_bool,
    assemble_timerange,
    DateAwareJSONEncoder,
    get_message_dict,
    json_return,
    message_card,
    request_wants_html,
)


app = Flask(__name__)
app.config.from_object("datagrepper.default_config")
if "DATAGREPPER_CONFIG" in os.environ:
    app.config.from_envvar("DATAGREPPER_CONFIG")
app.config["CORS_DOMAINS"] = list(map(re.compile, app.config.get("CORS_DOMAINS", [])))
app.config["CORS_HEADERS"] = list(map(re.compile, app.config.get("CORS_HEADERS", [])))

# Initialize a datanommer session.
dm.init(app.config.get("DATANOMMER_SQLALCHEMY_URL"))

# Register views
app.register_blueprint(healthz, url_prefix="/healthz")

import datagrepper.widgets  # noqa: E402,F401


@app.context_processor
def inject_variable():
    """Inject some global variables into all templates"""
    extras = {
        "models_version": get_distribution("datanommer.models").version,
        "grepper_version": get_distribution("datagrepper").version,
    }
    return extras


def match_regex_list(val, regexes):
    for regex in regexes:
        if regex.match(val):
            return True
    return False


def filter_regex_list(vals, regexes):
    return [val for val in vals if match_regex_list(val, regexes)]


@app.after_request
def add_cors(response):
    """Allow CORS for domains specified in the config"""
    if "Origin" in flask.request.headers:
        # Handle a CORS request
        origin = flask.request.headers["Origin"]
        if flask.request.method in app.config["CORS_METHODS"] and match_regex_list(
            origin, app.config["CORS_DOMAINS"]
        ):
            response.headers["Access-Control-Allow-Origin"] = origin
            if "Access-Control-Request-Method" in flask.request.headers:
                response.headers["Access-Control-Allow-Methods"] = ", ".join(
                    app.config["CORS_METHODS"]
                )
            if "Access-Control-Request-Headers" in flask.request.headers:
                requested_headers = flask.request.headers[
                    "Access-Control-Request-Headers"
                ]
                requested_headers = [h.strip() for h in requested_headers.split(",")]
                allowed_headers = filter_regex_list(
                    requested_headers, app.config["CORS_HEADERS"]
                )
                if allowed_headers:
                    response.headers["Access-Control-Allow-Headers"] = ", ".join(
                        allowed_headers
                    )
            if flask.request.method == "OPTIONS":
                # Special handling for pre-flight requests
                if "Vary" in response.headers:
                    response.headers["Vary"] = response.headers["Vary"] + ", Origin"
                else:
                    response.headers["Vary"] = "Origin"
                response.headers["Access-Control-Max-Age"] = app.config["CORS_MAX_AGE"]
    return response


@app.teardown_appcontext
def remove_session(exc):
    """Remove the session, which rolls back the transaction in progress.

    This is safe because Datagrepper never makes modifications to the database.
    """
    dm.session.remove()


def modify_rst(rst):
    """Downgrade some of our rst directives if docutils is too old."""

    try:
        # The rst features we need were introduced in this version
        minimum = [0, 9]
        version = map(int, docutils.__version__.split("."))

        # If we're at or later than that version, no need to downgrade
        if version >= minimum:
            return rst
    except Exception:
        # If there was some error parsing or comparing versions, run the
        # substitutions just to be safe.
        pass

    # Otherwise, make code-blocks into just literal blocks.
    substitutions = {
        ".. code-block:: javascript": "::",
    }
    for old, new in substitutions.items():
        rst = rst.replace(old, new)

    return rst


def modify_html(html):
    """Perform style substitutions where docutils doesn't do what we want."""

    substitutions = {
        '<tt class="docutils literal">': "<code>",
        "</tt>": "</code>",
    }
    for old, new in substitutions.items():
        html = html.replace(old, new)

    return html


def preload_docs(endpoint):
    """Utility to load an RST file and turn it into fancy HTML."""

    here = os.path.dirname(os.path.abspath(__file__))
    default = os.path.join(here, "docs")
    directory = app.config.get("DATAGREPPER_DOC_PATH", default)
    fname = os.path.join(directory, endpoint + ".rst")
    with codecs.open(fname, "r", "utf-8") as f:
        rst = f.read()

    rst = modify_rst(rst)

    api_docs = docutils.examples.html_body(rst)

    api_docs = modify_html(api_docs)

    api_docs = markupsafe.Markup(api_docs)
    return api_docs


htmldocs = dict.fromkeys(["index", "reference", "widget", "charts"])
for key in htmldocs:
    htmldocs[key] = preload_docs(key)


def load_docs(request):
    URL = app.config.get("DATAGREPPER_BASE_URL", request.url_root)
    docs = htmldocs[request.endpoint]
    docs = jinja2.Template(docs).render(URL=URL)
    return markupsafe.Markup(docs)


def count_all_messages():
    """Return a count of all messages in the db.

    In some cases, doing a full count of all the message on a postgres database
    takes too long (many tens of seconds).  We can produce a much faster query
    like this, but it only returns the approximate number of messages in the
    db.
    """

    if app.config.get("DATAGREPPER_APPROXIMATE_COUNT"):
        query = "SELECT * FROM approximate_row_count('messages');"
        total = dm.session.execute(query).first()[0]
    else:
        total = dm.Message.grep(defer=True)[0]

    return int(total)


POSSIBLE_SIZES = ["small", "medium", "large", "extra-large"]


@app.route("/")
def index():
    total = count_all_messages()
    docs = load_docs(flask.request)
    return flask.render_template("index.html", docs=docs, total=total)


@app.route("/reference/")
@app.route("/reference")
def reference():
    return flask.render_template("index.html", docs=load_docs(flask.request))


@app.route("/charts/")
@app.route("/charts")
def charts():
    return flask.render_template("index.html", docs=load_docs(flask.request))


@app.route("/widget/")
@app.route("/widget")
def widget():
    return flask.render_template("index.html", docs=load_docs(flask.request))


@app.route("/raw", methods=["GET"], strict_slashes=False)
@app.route("/v2/search", methods=["GET"], strict_slashes=False)
def raw():
    """Main API entry point."""

    # Perform our complicated datetime logic
    start = flask.request.args.get("start", None)
    end = flask.request.args.get("end", None)
    delta = flask.request.args.get("delta")
    start, end, delta = assemble_timerange(start, end, delta)

    # Further filters, all ANDed together in CNF style.
    users = flask.request.args.getlist("user")
    packages = flask.request.args.getlist("package")
    categories = flask.request.args.getlist("category")
    topics = flask.request.args.getlist("topic")
    contains = flask.request.args.getlist("contains")
    # Validate the "contains" argument
    _contains_limit = datetime.utcnow() - timedelta(weeks=4 * 8)
    if contains and datetime.fromtimestamp(start or 0) < _contains_limit:
        raise BadRequest(
            "When using contains, specify a start at most eight months into the past"
        )
    if contains and not (categories or topics):
        raise BadRequest(
            "When using contains, specify either a topic or a category as well"
        )

    # Still more filters.. negations of the previous ones.
    not_users = flask.request.args.getlist("not_user")
    not_packages = flask.request.args.getlist("not_package")
    not_categories = flask.request.args.getlist("not_category")
    not_topics = flask.request.args.getlist("not_topic")

    # Paging arguments
    page = int(flask.request.args.get("page", 1))
    if page < 1:
        raise BadRequest("page must be > 0")
    rows_per_page = int(flask.request.args.get("rows_per_page", 25))
    if rows_per_page > 100:
        raise BadRequest("rows_per_page must be <= 100")
    order = flask.request.args.get("order", "desc")
    if order not in ["desc", "asc"]:
        raise BadRequest("order must be either 'desc' or 'asc'")
    # adding size as paging arguments
    size = flask.request.args.get("size", "large")
    if size not in POSSIBLE_SIZES:
        raise BadRequest(f"size must be in one of these: {POSSIBLE_SIZES!r}")
    # adding chrome as paging arguments
    try:
        chrome = flask.request.args.get("chrome", "true", as_bool)
    except ValueError:
        raise BadRequest("chrome should be either 'true' or 'false'")

    # Response formatting arguments
    callback = flask.request.args.get("callback", None)
    meta = flask.request.args.getlist("meta")

    arguments = dict(
        start=start,
        delta=delta,
        end=end,
        users=users,
        packages=packages,
        categories=categories,
        topics=topics,
        contains=contains,
        not_users=not_users,
        not_packages=not_packages,
        not_categories=not_categories,
        not_topics=not_topics,
        page=page,
        rows_per_page=rows_per_page,
        order=order,
        meta=meta,
    )

    is_html = request_wants_html() and not callback

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
            contains=contains,
            not_users=not_users,
            not_packages=not_packages,
            not_categories=not_categories,
            not_topics=not_topics,
        )
    except Exception as e:
        traceback.print_exc()

        # TODO: return HTML when is_html is True
        output = dict(
            error=str(e),
            arguments=arguments,
        )
        # :D
        if app.config.get("DEBUG", False):
            output["tb"] = traceback.format_exc().split("\n")
        return json_return(output, 500, callback)

    # return HTML content else json
    if is_html:
        # removes boilerlate codes if chrome value is false
        template = "base.html" if chrome else "raw.html"
        return flask.render_template(
            template,
            size=size,
            response=[message_card(msg) for msg in messages],
            arguments=arguments,
            autoscroll=chrome,
        )

    else:
        output = dict(
            raw_messages=[get_message_dict(msg, meta) for msg in messages],
            total=total,
            pages=pages,
            count=len(messages),
            arguments=arguments,
        )
        return json_return(output, 200, callback)


# Get a message by msg_id
@app.route("/id", methods=["GET"], strict_slashes=False)
@app.route("/v2/id", methods=["GET"], strict_slashes=False)
def msg_id():
    if "id" not in flask.request.args:
        flask.abort(400)
    msg = dm.Message.query.filter_by(msg_id=flask.request.args["id"]).first()
    if not msg:
        flask.abort(404)

    # get paging argument for size and chrome
    size = flask.request.args.get("size", "large")
    if size not in POSSIBLE_SIZES:
        raise ValueError(f"size must be in one of these: {POSSIBLE_SIZES!r}")
    try:
        chrome = flask.request.args.get("chrome", "true", as_bool)
    except ValueError:
        raise ValueError("chrome should be either 'true' or 'false'")
    # get paging argument for is_raw
    # is_raw checks if card comes from the search endpoint
    try:
        is_raw = flask.request.args.get("is_raw", "false", as_bool)
    except ValueError:
        raise ValueError("is_raw should be either 'true' or 'false'")

    callback = flask.request.args.get("callback", None)
    meta = flask.request.args.getlist("meta")

    # converts message from sqlalchemy objects to json-like dicts
    msg_dict = get_message_dict(msg, meta)

    if request_wants_html() and not callback:
        # convert string into python dictionary
        msg_string = pygments.highlight(
            json.dumps(msg_dict, indent=2, sort_keys=True, cls=DateAwareJSONEncoder),
            pygments.lexers.JavascriptLexer(),
            pygments.formatters.HtmlFormatter(
                noclasses=True,
                style="emacs",
            ),
        ).strip()

        template = "base.html" if chrome else "raw.html"
        return flask.render_template(
            template,
            size=size,
            response=[message_card(msg)],
            msg_string=msg_string,
            heading="Message by ID",
            is_raw=is_raw,
        )
    else:
        return json_return(msg_dict, callback=callback)


@app.route("/charts/<chart_type>", methods=["GET"])
def make_charts(chart_type):
    """Return SVGs graphing db content."""

    # Perform our complicated datetime logic
    start = flask.request.args.get("start", None)
    end = flask.request.args.get("end", None)
    delta = flask.request.args.get("delta", None)
    start, end, delta = assemble_timerange(start, end, delta)

    # Further filters, all ANDed together in CNF style.
    users = flask.request.args.getlist("user")
    packages = flask.request.args.getlist("package")
    categories = flask.request.args.getlist("category")
    topics = flask.request.args.getlist("topic")
    contains = flask.request.args.getlist("contains")

    # Still more filters.. negations of the previous ones.
    not_users = flask.request.args.getlist("not_user")
    not_packages = flask.request.args.getlist("not_package")
    not_categories = flask.request.args.getlist("not_category")
    not_topics = flask.request.args.getlist("not_topic")

    end = end and datetime.fromtimestamp(end)
    start = start and datetime.fromtimestamp(start)
    end = end or datetime.utcnow()
    start = start or end - timedelta(days=365)

    human_readable = flask.request.args.get("human_readable", True, as_bool)
    logarithmic = flask.request.args.get("logarithmic", False, as_bool)
    show_x_labels = flask.request.args.get("show_x_labels", True, as_bool)
    show_y_labels = flask.request.args.get("show_y_labels", True, as_bool)
    show_dots = flask.request.args.get("show_dots", True, as_bool)
    fill = flask.request.args.get("fill", False, as_bool)

    title = flask.request.args.get("title", "fedmsg events")
    width = flask.request.args.get("width", 800, int)
    height = flask.request.args.get("height", 800, int)

    interpolation = flask.request.args.get("interpolation", None)
    interpolation_types = [
        None,
        "quadratic",
        "cubic",
    ]
    if interpolation not in interpolation_types:
        flask.abort(404, f"{interpolation} not in {interpolation_types!r}")

    chart_types = {
        "line": "Line",
        "stackedline": "StackedLine",
        "xy": "XY",
        "bar": "Bar",
        "horizontalbar": "HorizontalBar",
        "stackedbar": "StackedBar",
        "horizontalstackedbar": "HorizontalStackedBar",
        "funnel": "Funnel",
        "pyramid": "Pyramid",
        "verticalpyramid": "VerticalPyramid",
        "dot": "Dot",
        "gauge": "Gauge",
    }
    if chart_type not in chart_types:
        flask.abort(404, f"{chart_type} not in {chart_types!r}")

    style = flask.request.args.get("style", "default")
    if style not in pygal.style.styles:
        flask.abort(404, f"{style} not in {pygal.style.styles!r}")
    style = pygal.style.styles[style]

    chart = getattr(pygal, chart_types[chart_type])(
        human_readable=human_readable,
        logarithmic=logarithmic,
        show_x_labels=show_x_labels,
        show_y_labels=show_y_labels,
        show_dots=show_dots,
        fill=fill,
        title=title,
        width=width,
        height=height,
        interpolate=interpolation,
        x_label_rotation=45,
        style=style,
    )

    lookup = locals()
    factor_names = flask.request.args.getlist("split_on")
    factor_names = [name for name in factor_names if lookup[name]]
    factor_values = [lookup[name] for name in factor_names]
    factors = list(itertools.product(*factor_values))

    N = int(flask.request.args.get("N", 10))
    if N < 3:
        flask.abort(500, "N must be greater than 3")
    if N > 15:
        flask.abort(500, "N must be less than 15")

    try:
        labels = []

        kwargs = dict(
            users=users,
            packages=packages,
            categories=categories,
            topics=topics,
            contains=contains,
        )

        dates = [i for i, _ in daterange(start, end, N)]
        if human_readable:
            labels = [arrow.get(i).humanize() for i in dates]
        else:
            labels = [str(arrow.get(i).date()) for i in dates]

        for factor in factors:
            for i, name in enumerate(factor_names):
                kwargs[name] = [factor[i]]

            values = []

            for i, j in daterange(start, end, N):
                count, _, _ = dm.Message.grep(
                    start=i,
                    end=j,
                    rows_per_page=None,
                    defer=True,
                    not_users=not_users,
                    not_packages=not_packages,
                    not_categories=not_categories,
                    not_topics=not_topics,
                    **kwargs,
                )
                values.append(count)
            tag = factor and " & ".join(factor) or "events"

            # Truncate things to make charts prettier
            if tag.startswith("org.fedoraproject.prod."):
                tag = tag[len("org.fedoraproject.prod.") :]

            chart.add(tag, values)

        chart.x_labels = labels
        output = chart.render()
        status = 200
        mimetype = "image/svg+xml"
    except Exception as e:
        import traceback

        traceback.print_exc()
        output = "Error, %r" % e
        status = 500
        mimetype = "text/html"

    return flask.Response(
        response=output,
        status=status,
        mimetype=mimetype,
    )


def daterange(start, stop, steps):
    """A generator for stepping through time."""
    delta = (stop - start) / steps
    current = start
    while current + delta <= stop:
        yield current, current + delta
        current += delta


@app.route("/messagecount", methods=["POST"])
def post_messagecount():
    flask.abort(405)


# Instant requests
@app.route("/messagecount/")
@app.route("/messagecount")
def messagecount():
    total = {}
    total["messagecount"] = count_all_messages()
    total = flask.jsonify(total)
    return total


@app.errorhandler(404)
def not_found(error):  # TODO test this
    return flask.Response(
        response=json.dumps({"error": "not_found"}),
        status=404,
        mimetype="application/json",
    )


@app.errorhandler(500)
def internal_error(error):  # TODO test this
    return flask.Response(
        response=json.dumps(
            {
                "error": "internal_error",
                "detail": str(error),
                "traceback": traceback.format_exc(),
            }
        ),
        status=500,
        mimetype="application/json",
    )


def liveness():
    pass


def readiness():
    try:
        dm.session.execute("SELECT 1")
    except Exception:
        raise HealthError("Can't connect to the database")
