import json
from pathlib import Path

import pytest
from pymultirole_plugins.v1.schema import Document

from pyprocessors_afp_sports.afp_sports import (
    AFPSportsProcessor,
    AFPSportsParameters
)


def test_model():
    model = AFPSportsProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == AFPSportsParameters


# Arrange
@pytest.fixture
def original_docs():
    original_docs = []
    testdir = Path(__file__).parent
    for f in (testdir / "data").glob('*.json'):
        with f.open("r") as fin:
            doc = json.load(fin)
            original_doc = Document(**doc)
            original_docs.append(original_doc)
    return original_docs


def test_afp_sports(original_docs):
    # linker
    processor = AFPSportsProcessor()
    parameters = AFPSportsParameters()
    docs = processor.process(original_docs, parameters)
    for doc in docs:
        fired_by_rule = [c.properties['firedBy'] for c in doc.categories if c.properties]
        assert len(fired_by_rule) > 0
