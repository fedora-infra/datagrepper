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


def json_return(data, status=200, callback=None):
    try:
        output = json.dumps(data, cls=DateAwareJSONEncoder)
    except TypeError:
        flask.current_app.logger.exception(f"Could not encode to JSON: {data!r}")
        raise
    mimetype = flask.request.headers.get("Accept")
    # Our default - http://da.gd/vIIV
    if mimetype == "*/*":
        mimetype = "application/json"

    if callback:
        mimetype = "application/javascript"
        output = f"{callback}({output});"

    return flask.Response(
        response=output,
        status=status,
        mimetype=mimetype,
    )


def datetime_to_seconds(dt):
    """Name this, just because its confusing."""
    return dt.timestamp()


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


def as_bool(value):
    if isinstance(value, str):
        value = value.strip().lower()
        if value in ["true", "yes", "on", "y", "t", "1"]:
            return True
        elif value in ["false", "no", "off", "n", "f", "0"]:
            return False
        else:
            raise ValueError(f"value is not true or false: {value}")
    return bool(value)


def get_message_dict(msg, meta):
    # we can drop this if statement once we remove fedmsg
    if flask.request.url_rule.rule.startswith("/v2/"):
        msg_dict = msg.as_fedora_message_dict()
    else:
        msg_dict = msg.as_dict()
    if meta:
        msg_dict["meta"] = meta_argument(msg, meta)
    return msg_dict


def get_fm_message(message):
    """Build a ``fedora_messaging.message.Message`` instance from the DB message instance"""
    headers = message.headers
    if not headers:
        headers = {}
    if "sent-at" not in headers:
        headers["sent-at"] = message.timestamp.isoformat()

    MessageClass = get_fm_class(headers.get("fedora_messaging_schema"))
    fm_message = MessageClass(
        body=message.msg,
        topic=message.topic,
        headers=headers,
        severity=headers.get("fedora_messaging_severity"),
    )
    fm_message.id = message.msg_id
    return fm_message


def message_card(msg):
    """Generate a dict with the message's display information"""
    card = meta_argument(msg, ("date", "url", "summary", "app_icon", "agent_avatar"))
    card["timestamp"] = arrow.get(msg.timestamp)
    # import some keys unchanged
    for key in ("topic", "msg_id"):
        card[key] = getattr(msg, key)
    return card


def meta_argument(msg, meta):
    """Return meta argument values for search and id endpoints
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
    meta_legacy = {
        "subtitle": "summary",
        "link": "url",
        "icon": "app_icon",
    }
    meta_allowed = meta_expected | set(meta_legacy.keys())
    if len(set(meta).intersection(meta_allowed)) != len(set(meta)):
        raise ValueError(
            "meta must be in {}. Got {}".format(
                ",".join(list(meta_allowed)), list(meta)
            )
        )

    fm_msg = get_fm_message(msg)

    metas = {}
    for metadata in meta:
        # This one is exceptional
        if metadata == "date":
            metas[metadata] = arrow.get(msg.timestamp).humanize()
            continue
        # This one is exceptional too ;-)
        if metadata == "text":
            metas[metadata] = str(fm_msg)
            continue
        # Handle legacy (fedmsg) meta
        if metadata in meta_legacy:
            metas[metadata] = getattr(fm_msg, meta_legacy[metadata])
            metas.setdefault("WARNING", []).append(
                f"Meta {metadata} is deprecated and has been replaced by {meta_legacy[metadata]}"
            )
            continue
        # All the other metas use the schema properties
        try:
            metas[metadata] = getattr(fm_msg, metadata)
        except Exception:
            flask.current_app.logger.exception(
                f"Could not get metadata {metadata} for message {msg.id}"
            )
            continue

        # We have to do this because 'set' is not JSON-serializable
        if isinstance(metas[metadata], set):
            metas[metadata] = list(metas[metadata])

    return metas
