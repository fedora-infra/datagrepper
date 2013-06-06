import flask

from datetime import (
    datetime,
    timedelta,
)
import hashlib
import random
import json
import time


# http://flask.pocoo.org/snippets/45/
def request_wants_json():
    best = flask.request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        flask.request.accept_mimetypes[best] > \
        flask.request.accept_mimetypes['text/html']


def json_return(data):
    return flask.Response(json.dumps(data), mimetype='application/json')


def generate_api_key():
    rand = str(random.getrandbits(256))
    timestamp = str(int(time.time() * 1000))
    return hashlib.sha224(rand + timestamp).hexdigest()


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
        return (
            (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) /
            1e6)


def assemble_timerange(start, end, delta):
    """ Util to handle our complicated datetime logic. """

    # Complicated combination of default start, end, delta arguments.
    now = datetime_to_seconds(datetime.now())

    if not delta and not start and not end:
        pass
    elif delta:
        if end is None:
            if start is None:
                end = float(now)
            else:
                end = float(start) + float(delta)

        end = datetime.fromtimestamp(float(end))

        if start is None:
            delta = timedelta(seconds=float(delta))
            then = datetime_to_seconds(end - delta)
            start = float(then)

        # Convert back to seconds for datanommer.models
        end = datetime_to_seconds(end)
        delta = end - start
    else:
        if end is None:
            end = float(now)

        end = datetime.fromtimestamp(float(end))

        if start is None:
            delta = timedelta(seconds=600.0)
            start = datetime_to_seconds(end - delta)

        start = datetime.fromtimestamp(float(start))
        delta = end - start

        # Convert back to seconds for datanommer.models
        start = datetime_to_seconds(start)
        end = datetime_to_seconds(end)
        delta = timedelta_to_seconds(delta)

    return start, end, delta
