from werkzeug.middleware.dispatcher import DispatcherMiddleware
from .flask_app import flask_app

from .app1 import app as app1
# from app2 import app as app2

application = DispatcherMiddleware(flask_app, {
    '/app1': app1.server,
    # '/app2': app2.server,
})

