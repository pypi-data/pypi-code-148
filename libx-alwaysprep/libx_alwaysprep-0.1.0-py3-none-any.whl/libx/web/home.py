import numpy

from flask import Blueprint

from src.core.time.utils import get_curent_time


home = Blueprint('home', __name__)

@home.route('/')
def print_hello():
    return {
        "time": get_curent_time(),
        "numpy array": (numpy.arange(10)**2).tolist()
    }
