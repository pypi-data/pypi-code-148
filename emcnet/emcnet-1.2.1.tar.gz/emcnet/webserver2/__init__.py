"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    #app.config.from_object(".config.Config")
    app.config['FLASK_ENV'] = 'development'  # should not do this - figure out why the configurator is not working
    app.config['STATIC_FOLDER'] = "static"
    app.config['TEMPLATES_FOLDER'] = "templates"
    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes
        from .assets import compile_static_assets

        # Import Dash application
        from .plotlydash.dashboard_embedded import init_dashboard

        app = init_dashboard(app)

        # Compile static assets
        compile_static_assets(assets)

        return app
