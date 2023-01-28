import attrs
import koalak
import pytest


def test_default_values():
    field = koalak.field()

    assert field.name is None

    # attributes related to arguments/parameters
    assert field.kw_only is False
    assert field.default is attrs.NOTHING
    assert field.required is True
    assert field.annotation is None

    # attributes related to type checking
    assert field.type is None
    assert field.choices is None  # FIXME: None or list?

    # attributes related to documentation
    assert field.description is None
    assert field.examples is None

    # attributes related to database
    assert field.unique is False
    assert field.indexed is False


def test_generic_field_if_default_required_is_false():
    field = koalak.field(default=10)
    assert field.default == 10
    assert field.required is False


def test_generic_field_error_when_default_and_factory_are_set():
    with pytest.raises(ValueError):
        koalak.field(default=10, factory=list)


def test_method_get_default():
    field = koalak.field()
    assert field.get_default() is attrs.NOTHING

    field = koalak.field(default=10)
    assert field.default == 10

    field = koalak.field(factory=list)
    l1 = field.get_default()
    assert l1 == []

    l2 = field.get_default()
    assert l2 == []

    assert l1 is not l2


def test_required_property():
    field = koalak.field()
    assert field.required is True

    field = koalak.field(default=10)
    assert field.required is False

    field = koalak.field(factory=list)
    assert field.required is False
