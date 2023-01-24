"""
Some template functions.

For usage examples, see ``./tests/test_template_funcs.py``.
"""

from os import (
    getcwd,
    path,
)

from logging import Logger

from jinja2.environment import (
    Template,
    Environment,
)

from bh_utils import BH_TEMPLATE_FILE_NOT_FOUND_MSG

def template_root_path(source_dir="src") -> str:
    """Get a project template root path.

    This method assumes the project has the following layout.

    .. code-block:: text

            f:\\project_name\\
            |
            |-- ...
            |
            |-- src\\
            |   |
            |   |-- project_name\\
            |       |
            |       |-- ...
            |       |
            |       |-- templates\\
            |       |   |
            |       |   |-- base_template.html
            |       |   |
            |       |   |-- auth\\
            |       |   |-- report\\
            |       |
            |       |-- static\\

    The only possible variation is ``src\``.

    :param str source_dir: the project source directory.

    :return: project template root path.
    :rtype: str.

    :Return examples:

        * Windows: ``f:\\project_name\\{source_dir}\\project_name\\templates``
        * Linux: ``/volume1/web/project_name/{source_dir}/project_name/templates``
    """

    base_dir = getcwd()

    drive, root_path = path.splitdrive(base_dir)

    paths = root_path.split("/")
    project_path = paths[len(paths)-1][1:] if len(drive) > 0 else paths[len(paths)-1]

    return path.join(base_dir, source_dir, project_path, "templates")

def template_path(template_dir: str, source_dir="src"):
    """Get a project template sub-path under the template root path.

    Call to :py:meth:`template_root_path` to get the project template root path, then append
    a sub-path to this root path.

    :param str template_dir: template sub-path.

    :param source_dir: the project source directory.

    :return: a project template sub-path.
    :rtype: str.

    :Return examples:
        * Windows: ``f:\\project_name\\{source_dir}\\project_name\\templates\\{template_dir}``
        * Linux: ``/volume1/web/project_name/{source_dir}/project_name/templates/{template_dir}``
    """

    return path.join(template_root_path(source_dir), template_dir)

def get_template(template_env: Environment, file_name: str, logger: Logger) -> Template:
    """Attempt to load a template.

    :param template_env: an already prepared valid Jinja Environment class.
    :type template_env: `jinja2.Environment <https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.Environment>`_

    :param str file_name: a template file name to load.

    :param logger: where to log possible exception to.
    :type logger: `logging.Logger <https://docs.python.org/3/library/logging.html#logger-objects>`_

    :return: `jinja2.Template <https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.Template>`_.
    """

    try:
        template = template_env.get_template(file_name)
        return template
        
    except Exception as e:
        msg = BH_TEMPLATE_FILE_NOT_FOUND_MSG.format(path.join(template_env.loader.searchpath[0], file_name))
        logger.exception(msg)
        raise Exception(msg)