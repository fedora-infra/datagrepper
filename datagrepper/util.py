import flask

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
