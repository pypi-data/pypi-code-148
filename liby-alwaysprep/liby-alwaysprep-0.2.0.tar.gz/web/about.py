from flask import Blueprint

about = Blueprint('about', __name__)

@about.route('/')
def print_hello():
    return "This project is about versioning. (from version 0.2.0)"
