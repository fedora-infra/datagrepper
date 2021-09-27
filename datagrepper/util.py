import datetime
import json
import time

import arrow
import flask
from dateutil import tz
from dateutil.parser import parse
from fedora_messaging.message import get_class as get_fm_class


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
    return datetime_to_seconds(datetime.datetime.now(tz.tzutc()))


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


class DateAwareJSONEncoder(json.encoder.JSONEncoder):
    """Encoder with support for datetime objects"""

    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            # Convert to a UNIX timestamp. I would prefer isoformat but let's not
            # break compatibility.
            return time.mktime(obj.timetuple())
        return super().default(obj)


def get_fm_message(message_dict):
    """Build a ``fedora_messaging.message.Message`` instance from the message dictionary"""
    MessageClass = get_fm_class(message_dict["headers"]["fedora_messaging_schema"])
    message = MessageClass(
        body=message_dict["msg"],
        topic=message_dict["topic"],
        headers=message_dict["headers"],
        severity=message_dict["headers"].get("fedora_messaging_severity"),
    )
    message.id = message_dict["msg_id"]
    return message


def message_card(msg):
    """Generate a dict with the message's display information"""
    card = meta_argument(msg, ("date", "url", "summary", "app_icon", "agent_avatar"))
    card["timestamp"] = arrow.get(msg["timestamp"])
    # import some keys unchanged
    for key in ("topic", "msg_id"):
        card[key] = msg[key]
    return card


def meta_argument(msg, meta):
    """Util to accept meta arguments for /raw and /id endpoint
    so that JSON include human-readable strings"""

    meta_expected = {
        "summary",
        "text",
        "url",
        "app_icon",
        "agent_avatar",
        "usernames",
        "packages",
        "containers",
        "modules",
        "flatpaks",
        "date",
    }
    if len(set(meta).intersection(meta_expected)) != len(set(meta)):
        raise ValueError("meta must be in %s" % ",".join(list(meta_expected)))

    fm_msg = get_fm_message(msg)

    metas = {}
    for metadata in meta:
        # This one is exceptional
        if metadata == "date":
            metas[metadata] = arrow.get(msg["timestamp"]).humanize()
            continue
        # This one is exceptional too ;-)
        if metadata == "text":
            metas[metadata] = str(fm_msg)
            continue
        # All the other metas use the schema properties
        metas[metadata] = getattr(fm_msg, metadata)

        # We have to do this because 'set' is not JSON-serializable
        if isinstance(metas[metadata], set):
            metas[metadata] = list(metas[metadata])

    return metas
