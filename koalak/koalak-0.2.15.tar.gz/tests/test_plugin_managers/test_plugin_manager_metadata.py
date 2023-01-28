import koalak
import pytest


def test_metadata_working_normally():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        class Metadata:
            description = koalak.field()

    class APlugin(BasePlugin):
        name = "A"
        metadata = plugins.metadata(description="A plugin")

    assert APlugin.metadata.description == "A plugin"


def test_metadata_errors_metadata_attribute_not_present():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        class Metadata:
            description = koalak.field()

    with pytest.raises(AttributeError):

        class APlugin(BasePlugin):
            name = "A"
            # Don't have metadata field


def test_metadata_errors_field_in_metadata_not_present():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        class Metadata:
            description = koalak.field()

    with pytest.raises(TypeError):

        class BPlugin(BasePlugin):
            name = "B"
            # Don't have 'description' attribute
            metadata = plugins.metadata()


def test_metadata_errors_type_of_field():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        class Metadata:
            description: str = koalak.field()

    with pytest.raises(TypeError):

        class BPlugin(BasePlugin):
            name = "B"
            # Description present but int and not str
            metadata = plugins.metadata(description=12)


def test_metadata_errors_choices_in_field():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        class Metadata:
            x: int = koalak.field(choices=[1, 2, 3])

    with pytest.raises(ValueError):

        class BPlugin(BasePlugin):
            name = "B"
            # Description present but int and not str
            metadata = plugins.metadata(x=12)


def test_metadata_errors_metadata_function_with_unexpected_argument():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        class Metadata:
            x: int = koalak.field()

    with pytest.raises(TypeError):
        plugins.metadata(y=12)


def test_metadata_errors_metadata_created_with_function_not_dict():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        class Metadata:
            description = koalak.field()

    with pytest.raises(TypeError):

        class BPlugin(BasePlugin):
            name = "B"
            metadata = {"description": "B Plugin"}


def test_metadata_with_default_fields():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        class Metadata:
            description = koalak.field(default=None)

    class APlugin(BasePlugin):
        name = "A"


def test_metadata_with_factory_fields():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        class Metadata:
            description = koalak.field(factory=list)

    class APlugin(BasePlugin):
        name = "A"


def test_metadata_error_type_when_default_is_present():
    # Fixed error, when having default parameters only
    #  Didn't check that the metadata must be a dict
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        class Metadata:
            description = koalak.field(default="bla")

    with pytest.raises(TypeError):

        class APlugin(BasePlugin):
            metadata = {}


# TODO: implement filters on plugins bases on metadata
# TODO: implement default/required elements
# TODO: Check testing, with new changes
