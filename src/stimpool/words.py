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
