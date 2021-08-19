import json
from datetime import datetime

import arrow
import fedmsg
import flask
from dateutil import tz
from dateutil.parser import parse


# http://flask.pocoo.org/snippets/45/
# accept header returns json type content only
# However, if the accept header is */*, then return json.
def request_wants_html():
    best = flask.request.accept_mimetypes.best_match(
        ["application/json", "text/html", "text/plain"]
    )
    return best == "text/html"


def json_return(data):
    return flask.Response(json.dumps(data), mimetype="application/json")


def datetime_to_seconds(dt):
    """Name this, just because its confusing."""
    return dt.timestamp()


def timedelta_to_seconds(td):
    """Python 2.7 has a handy total_seconds method.
    If we're on 2.6 though, we have to roll our own.
    """

    if hasattr(td, "total_seconds"):
        return td.total_seconds()
    else:
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6


def datetime_to_timestamp(datetime_str_or_timestamp):
    try:
        return float(datetime_str_or_timestamp)
    except ValueError:
        pass

    time = parse(datetime_str_or_timestamp)
    # Assume default timezone is UTC
    if time.tzinfo is None:
        time = time.replace(tzinfo=tz.tzutc())
    return time.timestamp()


def now_seconds():
    return datetime_to_seconds(datetime.now(tz.tzutc()))


def assemble_timerange(start, end, delta):
    """Util to handle our complicated datetime logic."""

    # Normalize arguments
    if start is not None:
        start = datetime_to_timestamp(start)
    if end is not None:
        end = datetime_to_timestamp(end)
    if delta is not None:
        delta = float(delta)

    default_delta = float(flask.current_app.config["DEFAULT_QUERY_DELTA"])

    # Figure out values for unset arguments.
    valid_args = (start is not None, end is not None, delta is not None)
    if valid_args == (False, False, False):
        if default_delta >= 1:
            end = now_seconds()
            start = end - default_delta
            delta = default_delta
    elif valid_args == (False, False, True):
        end = now_seconds()
        start = end - delta
    elif valid_args == (False, True, False):
        if default_delta >= 1:
            start = end - default_delta
            delta = default_delta
        else:
            start = 0
    elif valid_args == (False, True, True):
        start = end - delta
    elif valid_args == (True, False, False):
        end = now_seconds()
        delta = end - start
    elif valid_args == (True, False, True):
        end = start + delta
    elif valid_args == (True, True, False):
        delta = end - start
    elif valid_args == (True, True, True):
        # Override delta
        delta = end - start

    return start, end, delta


def message_card(msg, size):
    """Util to generate icon, title, subtitle, link
    and secondary_icon using fedmsg.meta modules.
    """
    # using fedmsg.meta modules
    config = fedmsg.config.load_config([], None)
    fedmsg.meta.make_processors(**config)

    msgDict = {}

    if size in ["extra-large"]:
        pass

    if size in ["extra-large", "large"]:
        # generate secondary icon associated with message
        secondary_icon = fedmsg.meta.msg2secondary_icon(msg, legacy=False, **config)
        msgDict["secondary_icon"] = secondary_icon

    if size in ["extra-large", "large", "medium"]:
        icon = fedmsg.meta.msg2icon(msg, legacy=False, **config)
        msgDict["icon"] = icon
        # generate subtitle associated with message
        subtitle = fedmsg.meta.msg2subtitle(msg, legacy=False, **config)
        msgDict["subtitle"] = subtitle

    if size in ["extra-large", "large", "medium", "small"]:
        # generate URL associated with message
        link = fedmsg.meta.msg2link(msg, legacy=False, **config)
        msgDict["link"] = link
        # generate title associated with message
        title = fedmsg.meta.msg2title(msg, legacy=False, **config)
        msgDict["title"] = title
        msgDict["topic_link"] = msg["topic"]

    # convert the timestamp in datetime object
    # we can lose the try except as soon as we remove the fedmsg code from datagrepper
    try:
        msgDict["date"] = arrow.get(msg["timestamp"])
    except KeyError:
        msgDict["date"] = arrow.get(msg["headers"]["sent-at"])

    return msgDict


def meta_argument(msg, meta):
    """Util to accept meta arguments for /raw and /id endpoint
    so that JSON include human-readable strings"""

    meta_expected = {
        "title",
        "subtitle",
        "icon",
        "secondary_icon",
        "link",
        "usernames",
        "packages",
        "objects",
        "date",
    }
    if len(set(meta).intersection(meta_expected)) != len(set(meta)):
        raise ValueError("meta must be in %s" % ",".join(list(meta_expected)))

    metas = {}
    config = fedmsg.config.load_config([], None)
    for metadata in meta:
        # This one is exceptional
        if metadata == "date":
            metas[metadata] = arrow.get(msg["timestamp"]).humanize()
            continue

        # All the other metas use fedmsg.meta.msg2*
        cmd = "msg2%s" % metadata
        metas[metadata] = getattr(fedmsg.meta, cmd)(msg, **config)

        # We have to do this because 'set' is not
        # JSON-serializable.  In the next version of fedmsg, this
        # will be handled automatically and we can just remove this
        # statement https://github.com/fedora-infra/fedmsg/pull/139
        if isinstance(metas[metadata], set):
            metas[metadata] = list(metas[metadata])

    msg["meta"] = metas

    return msg
