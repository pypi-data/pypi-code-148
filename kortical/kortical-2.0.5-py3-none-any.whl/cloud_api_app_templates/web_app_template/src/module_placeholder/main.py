import os
import logging
from pathlib import Path
from flask import Flask
from web_app_template.logging import logging_config
from web_app_template.api import endpoints
from web_app_template.ui import index

logging_config.init()

logger = logging.getLogger(__name__)


def create_app():
    current_dir = os.path.dirname(__file__)
    static_path = os.path.join(Path(current_dir), 'ui', 'static')
    flask_app = Flask(__name__, static_url_path='/static', static_folder=static_path)
    endpoints.register_routes(flask_app)
    index.register_routes(flask_app)
    return flask_app


app = create_app()
