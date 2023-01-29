import pytest
from whatlies.language import BytePairLanguage
import numpy as np
from ....src.data_pipeline.feature_engineering.word_embedding import WordEmbedding


@pytest.mark.parametrize("lang, dimensions", [
    ("en", 25),
    ("es", 50),
    ("fr", 100)
])
def test_word_embedding_init(lang, dimensions):
    we = WordEmbedding(lang, dimensions)
    assert isinstance(we.bpl, BytePairLanguage)
    assert we.bpl.lang == lang
    assert we.bpl.dim == dimensions


@pytest.mark.parametrize("text, expected_shape", [
    ("This is a text", (50,)),
    ("Este es un texto", (50,)),
    ("C'est un texte", (50,)),
    ("&^%$#@", (50,))
])
def test_word_embedding_get_embedding(text, expected_shape):
    we = WordEmbedding("en", 50)
    embedding = we.get_embedding(text)
    assert isinstance(embedding, np.ndarray)
    assert embedding.shape == expected_shape
