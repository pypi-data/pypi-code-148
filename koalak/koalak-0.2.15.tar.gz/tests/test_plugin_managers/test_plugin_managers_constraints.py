from typing import List

import koalak
import pytest


def test_constraint_field_not_present():
    """Test that attribute "help" is required"""
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        help = plugins.field()  # help attribute is required

    class APlugin(BasePlugin):
        name = "A"
        help = "Something"

    class BPlugin(BasePlugin):
        name = "A"
        help = 12  # can be of any type

    with pytest.raises(AttributeError):
        # Must define help
        class CPlugin(BasePlugin):
            name = "B"


def test_constraint_field_with_its_type_through_argument():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        help = plugins.field(type=str)

    class APlugin(BasePlugin):
        name = "A"
        help = "Something"

    with pytest.raises(TypeError):
        # Help must be a string
        class BPlugin(BasePlugin):
            name = "B"
            help = 5


def test_constraint_field_with_its_type_through_annotation():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        help: str = plugins.field()

    class APlugin(BasePlugin):
        name = "A"
        help = "Something"

    with pytest.raises(TypeError):
        # Help must be a string
        class BPlugin(BasePlugin):
            name = "B"
            help = 5


def test_constraint_field_with_list_annotation():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        help: List[str] = plugins.field()

    class Plugin(BasePlugin):
        help = ["Something"]

    class Plugin(BasePlugin):
        help = []

    with pytest.raises(TypeError):
        # Help must be a string
        class Plugin(BasePlugin):
            help = 5

    with pytest.raises(TypeError):
        # Help must be a string
        class Plugin(BasePlugin):
            help = "test"

    with pytest.raises(TypeError):
        # Help must be a string
        class Plugin(BasePlugin):
            help = [1]

    with pytest.raises(TypeError):
        # Help must be a string
        class Plugin(BasePlugin):
            help = ["lol", 1]


def test_constraint_attr_choices():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        help = plugins.field(type=int, choices=[1, 2])

    class APlugin(BasePlugin):
        name = "A"
        help = 1

    with pytest.raises(ValueError):
        # Help must be 1 or 2
        class BPlugin(BasePlugin):
            name = "B"
            help = 3


def test_constraints_simple_abstract_method():
    plugins = koalak.mkpluginmanager()

    @plugins.mkbaseplugin
    class BasePlugin:
        @plugins.abstract
        def x(self):
            pass

    class XTest(BasePlugin):
        name = "x"

        def x(self):
            pass

    with pytest.raises(AttributeError):

        class YTest(BasePlugin):
            name = "y"
