#  Copyright (c) 2019-2023 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Test for typing utils
"""
from typing import Callable, Union

import pytest

from hvl_ccb.utils.typing import check_generic_type, is_generic_type_hint


def test_is_generic_type_hint():
    for type_ in (1, "a", (), list, int, str, object):
        assert not is_generic_type_hint(type_)

    for type_ in (Union[None, list[int]], Union, Callable):
        assert is_generic_type_hint(type_)

    for type_ in (list[int],):  # PEP 585
        assert is_generic_type_hint(type_)


def test_check_generic_type():
    with pytest.raises(ValueError):
        check_generic_type([], list)

    with pytest.raises(TypeError):
        check_generic_type(["a"], list[int])

    assert check_generic_type([1, 2], list[int]) is None

    with pytest.raises(TypeError):
        check_generic_type([1, 1.0], list[int])

    assert check_generic_type([1, 1.0], list[Union[int, float]]) is None
    assert check_generic_type(None, Union[None, list[int]]) is None
    assert check_generic_type([1, 2], Union[None, list[int]]) is None
