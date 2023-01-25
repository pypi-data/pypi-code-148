import pytest
from py_kaos_utils.pagination import paginate_generator


@pytest.fixture
def generator():
    return (i for i in range(5))


@pytest.mark.parametrize("limit", [10, 2, 0, -1])
def test_paginate_generator(generator, limit):
    pages = list(paginate_generator(generator, limit))
    assert len(pages) == 5 // limit + 1 if limit > 0 else 1
    l = list(range(5))
    assert pages[0] == l[:limit] if limit > 0 else l
