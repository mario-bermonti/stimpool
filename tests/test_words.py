"""Tests for `words` module."""

import pytest

from stimpool.words import WordPoolCreator


def test_get_default_pool():
    """Test words._get_default_pool."""

    shape_exp = (55457,)
    word_pool_creator = WordPoolCreator()
    word_pool = word_pool_creator._get_default_pool()
    shape_obs = word_pool.shape

    assert shape_obs == shape_exp


@pytest.mark.parametrize(
    ("word_original", "word_expected"),
    [
        # none
        ("perro", "perro"),
        # upper
        ("PErrO", "perro"),
        # space
        ("   perro   ", "perro"),
        # mixed
        ("  PErrO", "perro"),
    ],
)
def test_normalize_word(word_original, word_expected):
    """Test the _normalize_word with different cases."""

    word_pool_creator = WordPoolCreator()
    word_observed = word_pool_creator._normalize_word(word_original)

    assert word_observed == word_expected
