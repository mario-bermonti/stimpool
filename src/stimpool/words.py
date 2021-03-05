"""Create word pools."""

from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

ROOT_DIR = Path().resolve()


class WordPoolCreator(object):
    """Create word pools."""

    def __init__(self, pool: Optional[Iterable] = None) -> None:
        """Create a word pool.

        Parameters
        -----------
        pool : Iterable
            Word pool that will be used to create subpool (the default
            is None, use default word pool)
        """

        if pool is None:
            pool = self._get_default_pool()

        self.pool_original: pd.Series = pool

    def _get_default_pool(self) -> Iterable:
        """Get the default word pool."""

        path = ROOT_DIR / "src" / "stimpool" / "words" / "es_PR.dic"
        pool = pd.read_csv(path, squeeze=True)
        pool.name = "original pool"

        return pool

    def _format_pool(self, pool):
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

    def _normalize_word(self, word):
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

    def remove_words_accented_characters(self) -> None:
        """Remove words with accented characters.

        Accented characters:: á, é, í, ó, ú, ñ, ü
        """

        pool_cleaned = self._pool_original.mask(self._check_accented_characters)
        self._pool_cleaned = pool_cleaned.dropna()

    def _check_accented_characters(self, word):
        """Checks if the word contains accented characters.

        Parameters
        ----------
        word : str
            word to be analyzed

        Returns
        -------
        Bool
            True if the word contains accented characters; False otherwise
        """

        accented_characters = "áéíóúñü"
        for char in word:
            if char in accented_characters:
                return True
        return False
