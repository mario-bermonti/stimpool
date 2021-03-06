"""Tests for `words` module."""

from typing import List, Optional

import pandas as pd
import pytest
from pandas.testing import assert_series_equal

from stimpool.words import WordPoolCreator


def test_get_default_pool() -> None:
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
def test_normalize_word(word_original: str, word_expected: str) -> None:
    """Test the _normalize_word with different cases."""

    word_pool_creator = WordPoolCreator()
    word_observed = word_pool_creator._normalize_word(word_original)

    assert word_observed == word_expected


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        # valid
        ("perro", False),
        # edge case; this is the expected behavior
        # blank spaces are handled by other methods
        ("carro ", False),
        # invalid
        ("canción", True),
        ("así", True),
        ("güiro", True),
        ("ñame", True),
    ],
)
def test_check_accented_characters(word: str, expected: bool) -> None:
    """Test the _check_accented_characters with different cases."""

    word_pool_creator = WordPoolCreator()
    obs = word_pool_creator._check_accented_characters(word)

    assert obs == expected


@pytest.mark.parametrize(
    ("words", "exp", "how"),
    [
        (["yes", "no", "yes", "no"], pd.Series(["yes", "yes"]), "keep"),
        (["yes", "no", "yes", "no"], pd.Series(["no", "no"]), "remove"),
    ],
)
def test_get_words_meeting_criteria(words: List[str], exp: pd.Series, how: str) -> None:
    """Test _get_words_meeting_criteria with different cases."""
    word_pool_creator = WordPoolCreator(words)
    obs: pd.Series = word_pool_creator._get_words_meeting_criteria(
        func_checks_criteria=lambda x: "yes" == x,
        how=how,
    )

    obs = obs.reset_index(drop=True)
    exp = exp.reset_index(drop=True)
    assert_series_equal(obs, exp, check_dtype=False, check_index_type=False)
    assert obs.equals(exp)


@pytest.mark.parametrize(
    ("word", "min_len", "max_len", "exp"),
    [
        # only min
        ("perro", 1, None, True),
        ("perro", 6, None, False),
        # only max
        ("perro", None, 6, True),
        ("perro", None, 1, False),
        # None; special case
        ("perro", None, None, True),
        ("perro", None, None, True),
        # both
        ("perro", 1, 5, True),
        ("perro", 1, 4, False),
    ],
)
def test_check_word_length(word: str, min_len: int, max_len: int, exp: bool) -> None:
    """Test the _check_word_length with different cases."""

    word_pool_creator = WordPoolCreator()
    obs = word_pool_creator._check_word_length(word, min_len, max_len)

    assert obs == exp


@pytest.mark.parametrize(
    ("words", "min_len", "max_len", "exp"),
    [
        # only min
        # all meet criteria
        (
            ["al", "gato", "cabeza", "periódico"],
            1,
            None,
            pd.Series(["al", "gato", "cabeza", "periódico"]),
        ),
        # only min
        # some meet criteria
        (["al", "gato", "cabeza", "periódico"], 6, None, pd.Series(["cabeza", "periódico"])),
        # only min
        # none meet criteria
        (["al", "gato", "cabeza", "periódico"], 15, None, pd.Series([])),
        # only max
        # all meet criteria
        (
            ["al", "gato", "cabeza", "periódico"],
            None,
            15,
            pd.Series(["al", "gato", "cabeza", "periódico"]),
        ),
        # only max
        # some meet criteria
        (["al", "gato", "cabeza", "periódico"], None, 5, pd.Series(["al", "gato"])),
        # only max
        # none meet criteria
        (["al", "gato", "cabeza", "periódico"], None, 1, pd.Series([])),
        # only min y max
        # all meet criteria
        (
            ["al", "gato", "cabeza", "periódico"],
            0,
            15,
            pd.Series(["al", "gato", "cabeza", "periódico"]),
        ),
        # only min y max
        # some meet criteria
        (["al", "gato", "cabeza", "periódico"], 2, 5, pd.Series(["al", "gato"])),
        # only min y max
        # none meet criteria
        (["al", "gato", "cabeza", "periódico"], 3, 1, pd.Series([])),
    ],
)
def test_get_words_of_length(
    words: List[str], min_len: Optional[int], max_len: Optional[int], exp: pd.Series
) -> None:
    """Test the _get_words_of_length with different cases."""

    word_pool_creator = WordPoolCreator(words)
    word_pool_creator.get_words_of_length(min_len, max_len)
    obs: pd.Series = word_pool_creator._pool_cleaned

    obs = obs.reset_index(drop=True)
    exp = exp.reset_index(drop=True)
    assert_series_equal(obs, exp, check_dtype=False, check_index_type=False)


def test_get_words_of_length_exception() -> None:
    """Test that _get_words_of_length raises exception if no min or max length is specified."""

    word_pool_creator = WordPoolCreator()
    with pytest.raises(ValueError):
        word_pool_creator.get_words_of_length()
