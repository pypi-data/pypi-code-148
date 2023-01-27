# encoding: utf-8

u"""
==================================================================================
Do not use. Incomplete
----------------------------------------------------------------------------------
Filter     : A string or regular expression to match in the request.
             Leave blank to modify for all requests.
Override   : N/A
Parameters : key:value pairs.
----------------------------------------------------------------------------------

"""

from fdutil.tree_search import TreeSearch
import logging_helper
from pyhttpintercept.intercept.handlers.support import (decorate_for_json_parameters,
                                                        decorate_for_json_modifier,
                                                        decorate_for_uri_filter)

logging = logging_helper.setup_logging()


def replace_json_fragment(object,
                          logs,
                          fragment,
                          position=None,
                          key=None,):
    pass


@decorate_for_json_modifier
@decorate_for_json_parameters
@decorate_for_uri_filter
def modify(request,
           response,
           modifier,
           **_):

    logs = logging_helper.LogLines()

    # TODO!

    response._content = modifier.params

    return response
