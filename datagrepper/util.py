import flask

import arrow
from datetime import (
    datetime,
    timedelta,
    timezone,
)
import json
import fedmsg


# http://flask.pocoo.org/snippets/45/
# accept header returns json type content only
# However, if the accept header is */*, then return json.
def request_wants_html():
    best = flask.request.accept_mimetypes \
        .best_match(['application/json', 'text/html', 'text/plain'])
    return best == 'text/html'


def json_return(data):
    return flask.Response(json.dumps(data), mimetype='application/json')


def datetime_to_seconds(dt):
    """ Name this, just because its confusing. """
    return datetime.timestamp(dt)


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
    now = datetime_to_seconds(datetime.utcnow())

    if not delta and not start and not end:
        pass
    elif delta:
        if end is None:
            if start is None:
                end = float(now)
            else:
                start = float(start)
                end = start + float(delta)

        end = datetime.fromtimestamp(float(end), tz=timezone.utc)

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

        end = datetime.fromtimestamp(float(end), tz=timezone.utc)

        if start is None:
            delta = timedelta(seconds=600.0)
            start = datetime_to_seconds(end - delta)

        start = datetime.fromtimestamp(float(start), tz=timezone.utc)
        delta = end - start

        # Convert back to seconds for datanommer.models
        start = datetime_to_seconds(start)
        end = datetime_to_seconds(end)
        delta = timedelta_to_seconds(delta)

    return start, end, delta


def message_card(msg, size):
    """ Util to generate icon, title, subtitle, link
     and secondary_icon using fedmsg.meta modules.
    """
    # using fedmsg.meta modules
    config = fedmsg.config.load_config([], None)
    fedmsg.meta.make_processors(**config)

    msgDict = {}

    if (size in ['extra-large']):
        pass

    if (size in ['extra-large', 'large']):
        # generate secondary icon associated with message
        secondary_icon = fedmsg.meta.msg2secondary_icon(
            msg, legacy=False, **config)
        msgDict['secondary_icon'] = secondary_icon

    if (size in ['extra-large', 'large', 'medium']):
        icon = fedmsg.meta.msg2icon(msg, legacy=False, **config)
        msgDict['icon'] = icon
        # generate subtitle associated with message
        subtitle = fedmsg.meta.msg2subtitle(msg, legacy=False, **config)
        msgDict['subtitle'] = subtitle

    if (size in ['extra-large', 'large', 'medium', 'small']):
        # generate URL associated with message
        link = fedmsg.meta.msg2link(msg, legacy=False, **config)
        msgDict['link'] = link
        # generate title associated with message
        title = fedmsg.meta.msg2title(msg, legacy=False, **config)
        msgDict['title'] = title
        msgDict['topic_link'] = msg['topic']

    # convert the timestamp in datetime object
    msgDict['date'] = arrow.get(msg['timestamp'])

    return msgDict


def meta_argument(msg, meta):
    """ Util to accept meta arguments for /raw and /id endpoint
        so that JSON include human-readable strings"""

    meta_expected = set(['title', 'subtitle', 'icon', 'secondary_icon',
                         'link', 'usernames', 'packages', 'objects', 'date'])
    if len(set(meta).intersection(meta_expected)) != len(set(meta)):
        raise ValueError("meta must be in %s"
                         % ','.join(list(meta_expected)))

    metas = {}
    config = fedmsg.config.load_config([], None)
    for metadata in meta:
        # This one is exceptional
        if metadata == 'date':
            metas[metadata] = arrow.get(msg['timestamp']).humanize()
            continue

        # All the other metas use fedmsg.meta.msg2*
        cmd = 'msg2%s' % metadata
        metas[metadata] = getattr(
            fedmsg.meta, cmd)(msg, **config)

        # We have to do this because 'set' is not
        # JSON-serializable.  In the next version of fedmsg, this
        # will be handled automatically and we can just remove this
        # statement https://github.com/fedora-infra/fedmsg/pull/139
        if isinstance(metas[metadata], set):
            metas[metadata] = list(metas[metadata])

    msg['meta'] = metas

    return msg
