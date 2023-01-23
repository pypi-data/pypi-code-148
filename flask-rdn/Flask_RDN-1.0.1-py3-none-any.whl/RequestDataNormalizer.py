# typing
from .NormalizedRequest import NormalizedRequest

class RequestDataNormalizer:
    """ [Request Data Normalizer Flask Extension](https://github.com/Topazoo/Flask-Request-Data-Normalizer)
    
        To Use:
        ```
        app = Flask(__name__)
        RequestDataNormalizer(app)
        ```

        Overrides the functionality of a `flask.Request`:
        1. flask.Request.args - Base64 encoded query string parsing is supported via [QueryStringManager](https://github.com/Topazoo/Query-String-Manager)
        2. flask.Request.get_json - If the mimetype does not indicate JSON (:mimetype:`application/json`, see :attr:`is_json`), 
        this is will still attempt to parse JSON unless `force` is False
        3. flask.Request.get_json - Query parameters (`Request.args`), Form parameters (`Request.form`) and Body parameters are all returned.
        In vanilla Flask, this only returns Body parameters. The Body parameters take precedence if overlap occurs in keys.
    """

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.request_class = NormalizedRequest
