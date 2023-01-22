import flask
from flask import Flask
from markupsafe import escape

flask_app = Flask(__name__)


@flask_app.route('/')
def index():
    return 'Hello Flask app'


@flask_app.route('/site')
def show_user_profile():
    # show the user profile for that user
    # return 'Site %s' % escape(site_id)
    return flask.redirect('/app1/')
