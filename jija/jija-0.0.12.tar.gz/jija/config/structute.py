from jija.config import base, fields

from pathlib import Path as Path
import sys


class StructureConfig(base.Config):
    PROJECT_PATH = None
    CORE_PATH = None
    APPS_PATH = None
    PYTHON_PATH = fields.CharField(default=sys.executable)

    def __init__(self, *, project_path=None, core_dir='core', apps_dir='apps', python_path=None):
        super().__init__(project_path=project_path, core_dir=core_dir, apps_dir=apps_dir, python_path=python_path)

    @classmethod
    async def validate(cls, values):
        project_path = cls.__get_project_path(values['project_path'])
        return {
            'PROJECT_PATH': project_path,
            'CORE_PATH': project_path.joinpath(values['core_dir']),
            'APPS_PATH': project_path.joinpath(values['apps_dir']),
            'PYTHON_PATH': await StructureConfig.PYTHON_PATH.validate(values['python_path'])
        }

    @staticmethod
    def __get_project_path(project_path):
        if isinstance(project_path, Path):
            if not project_path.is_absolute():
                return project_path.absolute()

            return project_path

        path = Path(project_path) if project_path else Path()
        return path.absolute()
