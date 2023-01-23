# utils
from werkzeug.utils import cached_property
from QueryStringManager import QueryStringManager

# typing
from flask import Request
import typing as t

class NormalizedRequest(Request):
    """Works like the usual flask.Request with some added twists:
        1. flask.Request.args - Base64 encoded query string parsing is supported via [QueryStringManager](https://github.com/Topazoo/Query-String-Manager)
        2. flask.Request.get_json - If the mimetype does not indicate JSON (:mimetype:`application/json`, see :attr:`is_json`), 
        this is will still attempt to parse JSON unless `force` is False
        3. flask.Request.get_json - Query parameters (`Request.args`), Form parameters (`Request.form`) and Body parameters are all returned.
        In vanilla Flask, this only returns Body parameters. The Body parameters take precedence if overlap occurs in keys.
    """
    
    @cached_property
    def args(self) -> dict:
        """The parsed Query parameters (the part in the URL after the question
        mark) or None if no query parameters passed.

        Uses a [QueryStringManager](https://github.com/Topazoo/Query-String-Manager) to parse
        the query parameters including Base64 encoded query strings
        """

        if not self.query_string:
            return None

        return QueryStringManager.parse(self.query_string.decode())


    def get_json(self, force: bool = True, silent: bool = True, cache: bool = True) -> t.Optional[dict]:
        """Works like the usual get_json() with some added twists:
           1. Query parameters (`Request.args`), Form parameters (`Request.form`) and Body parameters are all present.
           In vanilla Flask, this only returns Body parameters. The Body parameters take precedence if overlap occurs in keys.
           2. Base64 encoded query string parsing is supported
           3. If the mimetype does not indicate JSON (:mimetype:`application/json`, see :attr:`is_json`), 
           this is will still attempt to parse JSON unless `force` is False

        If no data is present in the Query String, Form or Body, return None

        :param force: Ignore the mimetype and always try to parse JSON. (default: True)
        :param silent: Silence parsing errors and return None instead.
        :param cache: Store the parsed JSON to return for subsequent calls.
        """

        # Parse body data like usual
        body_data = super().get_json(force=force, silent=silent, cache=cache)

        # Parse query parameter data
        query_param_and_form_data = self.values.to_dict()

        # If no body data, no form data and no query params
        if not body_data and not query_param_and_form_data:
            return None
        
        return self.merge_request_data_dictionaries(query_param_and_form_data, body_data)
    

    def merge_request_data_dictionaries(self, dictionary1:dict, dictionary2:dict):
        """ Merge two dictionaries recursively. The value of the second
            dictionary will overwrite the first.
        """

        # Check "no-op" conditions
        if not dictionary1:
            return dictionary2
        if not dictionary2: 
            return dictionary1
        
        # For all keys and value in the second dictionary starting at top-level
        for key, value in dictionary2.items():
            # If the key is not on this level of the first dictionary, copy it over
            if key not in dictionary1:
                dictionary1[key] = value
            
            # Otherwise, if the key is in dictionary 1 on this level:
            else:
                # If the datatype of the value mismatches, default to the value of dict 2
                if type(value) != type(dictionary1[key]):
                    dictionary1[key] = value

                # If the datatype matches and is a dictionary, recurse
                elif isinstance(value, dict):
                    dictionary1[key] = self.merge_request_data_dictionaries(value, dictionary1[key])

                # If the datatype matches and is a list or something else, default to the value of dict 2
                else:
                    dictionary1[key] = value

        return dictionary1
