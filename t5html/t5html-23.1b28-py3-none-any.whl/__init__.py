#!/usr/bin/python3
""""
t5html-lib contains the function to process a t5html formatted file.

the main-function is make_html.

Example:

    from htmllib import make_html

    t5html = open("example.t5h").read()
    html = make_html(t5html)

"""
from .treebuilder import HTML_from_t5html as make_html
