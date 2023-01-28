import inspect
import os


class StackInspector:
    """
    Inspect the current stack to alter internal application behaviour based on the application stack
    """

    def __init__(self):
        self.stack = inspect.stack()
        self.stack_list = [f"{s.filename}:{s.function}:{s.lineno}" for s in self.stack]

    def is_app_startup(self):
        """
        Return if the app is starting up
        Detects management commands (including auto-reload debug server), Celery startup, PyCharm debugger and PyTest
        test suite startup or test startup.
        """
        is_management_command = self._is_startup_command(
            "manage.py"
        ) and not self._is_command_in_stack("django/core/management/commands/shell")
        is_celery_starting = self._are_all_commands_in_stack(
            {
                "celery/__main__.py",
                "celery/loaders/base",
                "on_import_modules",
            }
        )
        is_autoreload = self._is_command_in_stack("django/utils/autoreload")
        is_pycharm_debugger = self._are_all_commands_in_stack(
            {
                "pycharm_helpers/pydev/pydevd",
                "manage.py",
            }
        )
        is_pytest = self._is_env_var_set("PYTEST_ADDOPTS")
        is_pytest_run = self._is_value_in_env_var("PYTEST_CURRENT_TEST", "(call)")
        is_pytest_setup = is_pytest and not is_pytest_run
        return any(
            [
                is_management_command,
                is_autoreload,
                is_celery_starting,
                is_pytest_setup,
                is_pycharm_debugger,
            ]
        )

    def _is_startup_command(self, cmd):
        return cmd in self.stack_list[-1]

    def _is_command_in_stack(self, cmd):
        return any(cmd in frame for frame in self.stack_list)

    def _are_all_commands_in_stack(self, commands):
        return all([self._is_command_in_stack(cmd) for cmd in commands])

    def _is_env_var_set(self, var):
        return bool(var in os.environ)

    def _is_value_in_env_var(self, var, value):
        return bool(value in os.environ.get(var, ""))

    def print(self):
        """Print the current stack list to be used for debug purposes"""
        print("\n".join(self.stack_list))
