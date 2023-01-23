from flask import Flask


def page_not_found(e):
    return "nope", 404

def create_app():
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    return app

