"""Tests for `words` module."""

from typing import List, Optional

import pandas as pd
import pytest

from stimpool.words import WordPool


def test_get_default_pool() -> None:
    """Test words._get_default_pool."""

    shape_exp = (55457,)
    word_pool = WordPool()
    word_pool_default = word_pool._get_default_pool()
    shape_obs = word_pool_default.shape

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

    word_pool = WordPool()
    word_observed = word_pool._normalize_word(word_original)

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

    word_pool = WordPool()
    obs = word_pool._check_accented_characters(word)

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
    word_pool = WordPool(words)
    obs: pd.Series = word_pool._get_words_meeting_criteria(
        func_checks_criteria=lambda x: "yes" == x,
        how=how,
    )

    obs = obs.reset_index(drop=True)
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

    word_pool = WordPool()
    obs = word_pool._check_word_length(word, min_len, max_len)

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
def test_select_words_of_length(
    words: List[str], min_len: Optional[int], max_len: Optional[int], exp: pd.Series
) -> None:
    """Test the _select_words_of_length with different cases."""

    word_pool = WordPool(words)
    word_pool.select_words_of_length(min_len, max_len)
    obs: pd.Series = word_pool._pool_cleaned

    obs = obs.reset_index(drop=True)
    exp = exp.reset_index(drop=True)
    obs.equals(exp)


def test_select_words_of_length_exception() -> None:
    """Test that _select_words_of_length raises exception if no min or max length is specified."""

    word_pool = WordPool()
    with pytest.raises(ValueError):
        word_pool.select_words_of_length()


@pytest.mark.parametrize(
    ("word", "exp"),
    [
        # with
        ("acantio/S", "acantio"),
        ("acantonamiento/hS", "acantonamiento"),
        ("acantarar/RED", "acantarar"),
        # without
        ("acaso", "acaso"),
        ("accidentalmente", "accidentalmente"),
    ],
)
def test_remove_conjugation_suffix_from_word(word: str, exp: str) -> None:
    """Test the _remove_conjugation_suffix_from_word with different cases."""

    word_pool = WordPool(word)
    obs = word_pool._remove_conjugation_suffix_from_word(word)

    assert obs == exp


@pytest.mark.parametrize(
    ("words", "exp"),
    [
        # none
        (["accidentalmente", "úsenos", "óigame"], ["accidentalmente", "úsenos", "óigame"]),
        # all
        (
            ["accidentar/RED", "accidentario/GS", "accidente/S"],
            ["accidentar", "accidentario", "accidente"],
        ),
        # mixed
        (
            [
                "accidentalmente",
                "úsenos",
                "óigame",
                "accidentar/RED",
                "accidentario/GS",
                "accidente/S",
            ],
            ["accidentalmente", "úsenos", "óigame", "accidentar", "accidentario", "accidente"],
        ),
    ],
)
def test_clean_conjugation_suffixes(words: List[str], exp: List[Optional[str]]) -> None:
    """Test the _clean_conjugation_suffixes with different cases."""

    exp: pd.Series = pd.Series(exp)  # type: ignore
    exp = exp.reset_index(drop=True)  # type: ignore
    word_pool = WordPool(words)
    words = pd.Series(words)
    obs = word_pool._clean_conjugation_suffixes(words)
    obs = obs.reset_index(drop=True)

    assert obs.equals(exp)


@pytest.mark.parametrize("words", [["al", "gato", "cabeza", "periódico", "ratón"]])
def test_sample_pool_is_reproducible(words: List[str]) -> None:
    """Test that sample_pool is reproducible."""

    word_pool = WordPool(words)
    obs1 = word_pool.sample_pool(n=3)
    obs2 = word_pool.sample_pool(n=3)

    obs1.equals(obs2)
