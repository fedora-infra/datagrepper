import flask
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy

import datagrepper

# Set up OpenID
oid = OpenID(datagrepper.app, datagrepper.app.config['OPENID_STORE'])

# set up SQLAlchemy
db = SQLAlchemy(datagrepper.app)

from datagrepper import forms, util
from datagrepper.models import User, Job


# Verify that the user is logged in. We check for an API key first, then for an
# 'openid' key in the session cookie.
#
# If a user submits both an apikey and an openid (which is unsupported), a
# valid openid will override a valid apikey.
@datagrepper.app.before_request
def lookup_current_user():
    flask.g.user = None
    # Look for 'apikey' in POST or GET
    if flask.request.method == 'POST':
        if 'apikey' in flask.request.form:
            apikey = flask.request.form['apikey']
            flask.g.user = User.query.filter_by(apikey=apikey).first()
    if 'apikey' in flask.request.args:
        apikey = flask.request.args['apikey']
        flask.g.user = User.query.filter_by(apikey=apikey).first()
    # Look for 'openid' in encrypted session cookie
    if 'openid' in flask.session:
        flask.g.user = User.query.\
            filter_by(openid=flask.session['openid']).first()


@oid.after_login
def create_or_login(resp):
    flask.session['openid'] = resp.identity_url
    user = User.query.filter_by(openid=resp.identity_url).first()
    if user is None:
        # create new user object
        user = User(openid=resp.identity_url, email=resp.email)
        # generate API key
        while True:
            apikey = util.generate_api_key()
            if User.query.filter_by(apikey=apikey).first() is None:
                break
        user.apikey = apikey
        # commit user to database
        db.session.add(user)
        db.session.commit()
    if user is not None:
        flask.flash(u'You are now logged in')
        flask.g.user = user
    return flask.redirect(oid.get_next_url())


def start_resp_object():
    resp = {'user': None}
    if flask.g.user:
        resp['user'] = flask.g.user.openid
    return resp


# Provide documentation of all topics from fedmsg.meta.
# Also provide a list of current tasks owned by the user if logged in.
@datagrepper.app.route('/')
@datagrepper.app.route('/page/<int:page>')
def index(page=1):
    # TODO: integrate fedmsg.meta for automated documentation
    resp = start_resp_object()
    # show jobs
    if flask.g.user:
        jobs = flask.g.user.jobs
        start = (page - 1) * 20
        if start > jobs.count():
            return flask.redirect(flask.url_for('index', page=1))
        resp['jobs'] = flask.g.user.jobs.slice(start, start+20).all()
        resp['jobs_count'] = jobs.count()
        if start + 20 < jobs.count():
            resp['jobs_continue'] = {'page': page + 1}
    if util.request_wants_json():
        return util.json_return(resp)
    else:
        return flask.render_template('index.html', resp=resp)


# Log the user in + woo cookies
# This is *not* called via the API
@datagrepper.app.route('/login', methods=('GET', 'POST'))
@oid.loginhandler
def login():
    if flask.g.user is not None:
        return flask.redirect(oid.get_next_url())
    if flask.request.method == 'POST':
        openid = flask.request.form.get('openid')
        if openid:
            return oid.try_login(openid, ask_for=['email'])
    return flask.render_template('login.html', next=oid.get_next_url(),
                                 error=oid.fetch_error(),
                                 resp=start_resp_object())


# Log the user out
@datagrepper.app.route('/logout')
def logout():
    flask.session.pop('openid', None)
    flask.flash(u'You are now logged out')
    return flask.redirect(oid.get_next_url())


# Edit user information (reset API key, change email)
@datagrepper.app.route('/user', methods=('GET', 'POST'))
def user():
    infoform = forms.InformationForm(email=flask.g.user.email)
    apiform = forms.NullForm()
    form = None

    if flask.request.method == 'POST':
        if 'formname' in flask.request.form:
            if flask.request.form['formname'] == 'infoform':
                form = infoform
            elif flask.request.form['formname'] == 'apiform':
                form = apiform

    if form:
        if form.validate_on_submit():
            if form == infoform:
                flask.g.user.email = form.email.data
                db.session.add(flask.g.user)
                db.session.commit()
                flask.flash(u'Your information was successfully changed')
            elif form == apiform:
                # generate API key
                while True:
                    apikey = util.generate_api_key()
                    if User.query.filter_by(apikey=apikey).first() is None:
                        break
                flask.g.user.apikey = apikey
                db.session.add(flask.g.user)
                db.session.commit()
                flask.flash(u'Your API key was successfully reset')

    return flask.render_template('user.html', resp=start_resp_object(),
                                 infoform=infoform, apiform=apiform)


def datetime_to_seconds(dt):
    """ Name this, just because its confusing. """
    return time.mktime(dt.timetuple())


# Add a request job to the queue
@datagrepper.app.route('/submit')
def submit():
    pass
