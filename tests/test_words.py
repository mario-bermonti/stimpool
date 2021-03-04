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
