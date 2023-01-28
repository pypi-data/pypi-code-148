import koalak
import pytest


@pytest.mark.skip
def test_plugin_manager_run_simple():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        @koalak.abstract
        def append(self, l):
            pass

    class AppendOnePlugin(BasePlugin):
        name = "append_one"

        def append(self, l):
            return l.append(1)

    class AppendTwoPlugin(BasePlugin):
        name = "append_two"

        def append(self, l):
            return l.append(2)

    l_argument = []
    plugins.runner.append(l_argument).run()
