import pytest
from ....src.data_pipeline.feature_engineering.key_smash import KeySmash


@pytest.mark.parametrize("text, expected", [
    ("PUENTECILLA KM. 1.7", 1.121212121212121),
    ("ASDASD XXXX", 3.0)
])
def test_calculate_char_frequency_metric(text, expected):
    key_smash = KeySmash()
    assert key_smash.calculate_char_frequency_metric(text) == expected


@pytest.mark.parametrize("text, opt, expected", [
    ("PUENTECILLA KM. 1.7", "vowels", 0.21052631578947367),
    ("ASDASD XXXX", "consonants", 2.1818181818181817),
    ("!@#$% ASDFGHJKL", "special_characters", 1.6666666666666667)
])
def test_calculate_irregular_sequence_metric(text, opt, expected):
    key_smash = KeySmash()
    assert key_smash.calculate_irregular_sequence_metric(text, opt) == expected


@pytest.mark.parametrize("text, expected", [
    ("ABC 123 !@#", 0.0),
    ("ABC123 !@#", 0.9)
])
def test_calculate_number_count_metric(text, expected):
    key_smash = KeySmash()
    assert key_smash.calculate_number_count_metric(text) == expected
