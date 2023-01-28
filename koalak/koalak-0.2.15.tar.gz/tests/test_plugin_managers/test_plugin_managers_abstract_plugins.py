import koalak
import pytest


def test_simple_abstract_subplugin():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        # This plugin requires the description attribute
        description: str = plugins.field()

    # Plugin A must have the attribute "name"
    with pytest.raises(AttributeError):

        class APlugin(BasePlugin):
            name = "A"

    # Abstract class are not checked!
    class AbstractPlugin(BasePlugin):
        abstract = True

    # don't need description since abstract class have it
    # class BPlugin(AbstractPlugin):
    #    name = "B"


def test_abstract_subcplugin_with_other_fields():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        # This plugin requires the description attribute
        description: str = plugins.field()

    # Plugin A must have the attribute "name"
    with pytest.raises(AttributeError):

        class APlugin(BasePlugin):
            name = "A"

    # Abstract class are not checked!
    class AbstractPlugin(BasePlugin):
        abstract = True
        help: str = plugins.field()

    # Plugin must have help and description
    with pytest.raises(AttributeError):

        class BPlugin(AbstractPlugin):
            name = "B"
            help = "test"

    with pytest.raises(AttributeError):

        class CPlugin(AbstractPlugin):
            name = "C"
            description = "test"


def test_abstract_subcplugin_overwirting_field():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        # This plugin requires the description attribute
        description: str = plugins.field()

    # Plugin A must have the attribute "name"
    with pytest.raises(TypeError):

        class APlugin(BasePlugin):
            name = "A"
            description = 1  # description must be int

    # Abstract class are not checked!
    class AbstractPlugin(BasePlugin):
        abstract = True
        description: int = plugins.field()

    class BPlugin(AbstractPlugin):
        name = "B"
        description = 1  # now description can be int
