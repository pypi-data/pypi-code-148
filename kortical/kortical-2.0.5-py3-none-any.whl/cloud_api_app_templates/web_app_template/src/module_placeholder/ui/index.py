import os
import flask
import logging
from kortical import app
from kortical import environment
from kortical.api.project import Project
from kortical.api.environment import Environment

from module_placeholder.ui import jinja
from module_placeholder.authentication import safe_api_call

logger = logging.getLogger(__name__)

app_config = app.get_config(format='yaml')
app_title = app_config['app_title']
logo_image_url = app_config['logo_image_url']

environment_config = environment.get_config(format='yaml')
if environment_config is None:
    environment_config = {}

app_title_extension = environment_config['app_title_extension'] if 'app_title_extension' in environment_config else ''
colour1 = environment_config['colour1'] if 'colour1' in environment_config else "#00cae5"
colour2 = environment_config['colour2'] if 'colour2' in environment_config else "#ef00ff"
background_colour = environment_config['background_colour'] if 'background_colour' in environment_config else "white"

project = Project.get_selected_project()
app_title_extension = app_title_extension.replace('<environment_name>', Environment.get_selected_environment(project).name)


# Adjust base name depending on environment
app_name = "" if os.environ.get('SERVER_RUNNING_LOCALLY', "FALSE") == "TRUE" else "module_placeholder"


def register_routes(app):

    @app.route('/', methods=['get'])
    @safe_api_call
    def get_index():
        template = jinja.get_template('index.html')
        return flask.Response(template.render(
            app_name=app_name,
            app_title=app_title,
            app_title_extension=app_title_extension,
            logo_image_url=logo_image_url,
            colour1=colour1,
            colour2=colour2,
            background_colour=background_colour))
