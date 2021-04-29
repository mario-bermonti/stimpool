"""Create word pools."""

import re
from pathlib import Path
from typing import Any, Callable, Iterable, Optional, Tuple

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent


class WordPool(object):
    """Create word pools."""

    def __init__(
        self, pool: Optional[Iterable] = None, clean_conjugation_suffix: bool = True
    ) -> None:
        """Create a word pool.

        Parameters
        -----------
        pool : Iterable
            Word pool that will be used to create subpool (the default
            is None, use default word pool)
        clean_conjugation_suffix : bool
            Specifies if suffixes that are used to identify word conjugations
            should be removed from the pool (Default=True)
        """

        self._pool_original, self._pool_cleaned = self._prepare_pool(
            pool, clean_conjugation_suffix
        )

    def _prepare_pool(
        self, pool: Optional[Iterable[str]], clean_conjugation_suffix: bool
    ) -> Tuple[pd.Series, pd.Series]:
        """Prepare word pool to be used.

        Parameters
        ----------
        pool : Iterable
            Word pool that will be used to create subpool.
        clean_conjugation_suffix : bool
            Specifies if suffixes that are used to identify word conjugations
            should be removed from the pool (Default=True)

        Returns
        -------
        word_pools
            Original word pool and its formatted word version, which will be
            used to create the subpool.
        """

        if pool is None:
            pool_current: pd.Series = self._get_default_pool()
        else:
            # redefining makes sense; see mypy issue #6233
            pool_current: Iterable = pool  # type: ignore

        pool_formatted: pd.Series = self._format_pool(pool_current)
        pool_original: pd.Series[str] = pool_formatted.copy()
        pool_cleaned: pd.Series[str] = pool_formatted.copy()

        if clean_conjugation_suffix:
            pool_cleaned: pd.Series = self._clean_conjugation_suffixes(  # type: ignore
                pool_cleaned
            )

        pool_original.name = "words_original"
        pool_cleaned.name = "words"

        return pool_original, pool_cleaned

    def _get_default_pool(self) -> pd.Series:
        """Get the default word pool."""

        path = ROOT_DIR / "words" / "es_PR.dic"
        pool = pd.read_csv(path, squeeze=True)

        return pool

    def _format_pool(self, pool: Iterable) -> pd.Series:
        """Format word pool.

        The pool is formatted by converting it in into a pd.Series if
        necessary and formatting its words.

        Parameters
        ----------
        pool : Iterable
            word pool

        Returns
        -------
        pool_formatted : pd.Series
        """

        if not isinstance(pool, pd.Series):
            pool = pd.Series(pool)

        pool_formatted: pd.Series = pool.apply(self._normalize_word)

        return pool_formatted

    def _normalize_word(self, word: str) -> str:
        """Normalize the word.

        Parameters
        ----------
        word : str
            word to be normalized

        Returns
        -------
        word_normalized : str
        """

        word_normalized = word.strip().lower()

        return word_normalized

    def select_words_without_accented_characters(self) -> None:
        """Get words without accented characters.

        Accented characters:: á, é, í, ó, ú, ñ, ü
        """

        pool_cleaned = self._get_words_meeting_criteria(
            func_checks_criteria=self._check_accented_characters,
            how="remove",
        )

        self._pool_cleaned = pool_cleaned

    def _check_accented_characters(self, word: str) -> bool:
        """Check if the word contains accented characters.

        Parameters
        ----------
        word : str
            word to be analyzed

        Returns
        -------
        bool
            True if the word contains accented characters; False otherwise
        """

        pattern_accented_characters = re.compile("[áéíóúñü]")
        matches = pattern_accented_characters.findall(word)
        if len(matches) > 0:
            return True
        else:
            return False

    def select_words_of_length(self, min_len: int = None, max_len: int = None) -> None:
        """Get words of the length specified.

        Parameters
        ----------
        min_len : int
            Minimum word length (defaults to None; no min length). If a min length is
            not specified, a max length has to be specified.
        max_len : int
            Maximum word length (defaults to None; no max length). If a max length is
            not specified, a min length has to be specified.

        Raises
        ------
        ValueError
            If neither min_len nor max_len are specified.
        """

        if min_len is None and max_len is None:
            raise ValueError("Either min_len or a max_len have to be specified")

        pool_cleaned = self._get_words_meeting_criteria(
            func_checks_criteria=self._check_word_length,
            how="keep",
            min_len=min_len,
            max_len=max_len,
        )

        self._pool_cleaned = pool_cleaned

    def _check_word_length(
        self, word: str, min_len: int = None, max_len: int = None
    ) -> bool:
        """Check that the length of the word meets the established limits.

        Parameters
        ----------
        word : str
            word to be analyzed
        min_len : int
            Minimum word length (defaults to None; no min length).
        max_len : int
            Maximum word length (defaults to None; no max length).

        Returns
        -------
        bool
            True if the word is within the specified length; False otherwise.
        """

        word_length = len(word)

        if min_len is None:
            min_len = 0
        if max_len is None:
            max_len = word_length

        if word_length >= min_len and word_length <= max_len:
            return True
        else:
            return False

    def _clean_conjugation_suffixes(self, pool: pd.Series) -> pd.Series:
        """Clean suffix that indicates how to conjugate the words."""

        pool_clean: pd.Series = pool.apply(self._remove_conjugation_suffix_from_word)

        return pool_clean

    def _remove_conjugation_suffix_from_word(self, word: str) -> str:
        """Remove suffix that indicates how to conjugate the word."""

        if "/" in word:
            word_elements = word.split("/")
            word = word_elements[0]

        return word

    def _get_words_meeting_criteria(
        self, func_checks_criteria: Callable, how: str = "keep", **kwargs: Optional[Any]
    ) -> pd.Series:
        """Run specified analysis on words (helper function).

        Parameters
        ----------
        func_checks_criteria : Callable
            Function that analyzes the words to determine which met the
            criteria.
        how : {"keep", "remove"}, str  # noqa: DAR103 (numpy style)
            Determines if words meeting the criteria should be kept or removed.
        **kwargs : Any
            Key-word args to pass to func_checks_criteria

        Returns
        -------
        pool_cleaned : pd.Series
            Words that met the criteria.
        """

        pool_meeting_criteria_flags = self._pool_cleaned.apply(
            func_checks_criteria, **kwargs
        )
        if how == "keep":
            pool_meeting_criteria = self._pool_cleaned.where(
                pool_meeting_criteria_flags
            )
        elif how == "remove":
            pool_meeting_criteria = self._pool_cleaned.mask(pool_meeting_criteria_flags)

        pool_cleaned = pool_meeting_criteria.dropna()

        return pool_cleaned

    def sample_pool(self, n: int, reproducible: bool = True) -> pd.Series:
        """Return a sample from the word pool.

        This is just a helper function that uses pandas.Series.sample.
        You can read its [complete documentation]
        (https://pandas.pydata.org/docs/reference/api/pandas.Series.sample.html)

        Parameters
        ----------
        n : int
            sample size

        reproducible : bool
            Specifies whether the sample obtained should be reproducible.
            This is important to guarantee the reproducibility of
            research (Default=True)

        Returns
        -------
        pd.Series
            pool sample of specified size
        """

        reproducible_coded: Optional[int] = 1 if True else None

        sample = self._pool_cleaned.sample(n=n, random_state=reproducible_coded)

        return sample

    def save_pool(self, filename: str = "word pool") -> None:
        """Save the word pool to a csv file.

        This is just a helper function that uses pandas.Series.to_csv.
        You can read its [complete documentation]
        (https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.Series.to_csv.html)

        Parameters
        ----------
        filename : str
            Name of the file without the extension (i.e., csv). (Default=word pool)
        """

        path = f"{filename}.csv"
        self._pool_cleaned.name = "words"

        self._pool_cleaned.to_csv(path, index=False)

    @property
    def words(self) -> pd.Series:
        """Return the clean word pool."""

        return self._pool_cleaned
