import flask

import simplejson


# http://flask.pocoo.org/snippets/45/
def request_wants_json():
    best = flask.request.accept_mimetypes \
            .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
            flask.request.accept_mimetypes[best] > \
            flask.request.accept_mimetypes['text/html']


def json_return(data):
    return flask.Response(simplejson.dumps(data), mimetype='application/json')
