from jinja2 import Environment, FileSystemLoader
from .templates import return_function 
import os


def generate_script(node):
    """
    Generate script for training data.
    """
    output =  return_function(node)
    return output
