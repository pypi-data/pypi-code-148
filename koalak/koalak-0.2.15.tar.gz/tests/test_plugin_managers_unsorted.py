import os
import sys
import tempfile

import koalak
import pytest
from koalak.utils import temp_pathname, tmp_module


def test_load_plugins():
    # TODO: check if this test is correct
    # TODO: Test with existing directory and without
    with tempfile.TemporaryDirectory() as plugin_path:
        plugins = koalak.mkpluginmanager(homepath=plugin_path)

        @plugins.mkbaseplugin
        class BasePlugin:
            pass

        class APlugin:
            name = "A"

        # Temporally create a module so it can be importable by the plugin
        with tmp_module(context={"BasePlugin": BasePlugin}) as module:
            name_module = module.__name__
            # print(name_module, name_module in sys.modules)
            data_file = f"""from {name_module} import BasePlugin
class BPlugin(BasePlugin):
    name = 'B'
    """
            with open(os.path.join(plugin_path, "plugin.py"), "w") as f:
                # print("in path", os.path.join(plugin_path, "plugin.py"))
                # print("data_file", data_file)
                f.write(data_file)

            # Init folder and plugins
            plugins.init()
            assert plugins["B"].name == "B"  # Just check that "B" is loaded in plugnis


def test_init_without_homepath():
    """We can not initiate a plugin manager without homepath"""
    plugins = koalak.mkpluginmanager()
    with pytest.raises(TypeError):
        plugins.init()  # No error should be raised


def test_double_init():
    """We can init twice"""
    with temp_pathname() as pathname:
        plugins = koalak.mkpluginmanager(homepath=pathname)
        plugins.init()
        with pytest.raises(TypeError):
            plugins.init()


def test_init_with_homepath():
    """Homepath is correctly created"""
    with temp_pathname() as pathname:
        plugins = koalak.mkpluginmanager(homepath=pathname)
        plugins.init()
        assert os.path.isdir(plugins.homepath)


# =========== #
# CONSTRAINTS #
# =========== #
# TODO: are inheritibale needed?
@pytest.mark.skip
def test_constraint_attr_inheritable_true():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        x = plugins.field()  # By default inheritable is True

    class APlugin(BasePlugin):
        name = "A"
        x = 1

    class BPlugin(APlugin):
        name = "B"


@pytest.mark.skip
def test_constraint_attr_inheritable_false():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        x = plugins.field(inheritable=False)

    class APlugin(BasePlugin):
        name = "A"
        x = 1

    with pytest.raises(TypeError):

        class BPlugin(APlugin):
            name = "B"
