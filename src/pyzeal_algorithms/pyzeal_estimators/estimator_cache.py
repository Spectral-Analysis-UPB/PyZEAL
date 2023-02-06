"""
TODO

Authors:\n
- Philipp Schuette
"""

from logging import DEBUG
from typing import Dict, Optional, Tuple

from pyzeal_logging.loggable import Loggable


class EstimatorCache(Loggable):
    """
    A simple in-memory cache that can store and retrieve total argument changes
    along horizontal and vertical lines in the complex plane.
    """

    __slots__ = ("_cache", "cacheHits", "cacheMisses")

    def __init__(self) -> None:
        """
        TODO
        """
        self._cache: Dict[Tuple[complex, complex], float] = {}
        self.logger.info("initialized a new argument estimator cache...")
        # cache hits and misses are only recorded if logging is set to DEBUG
        self.cacheHits = 0
        self.cacheMisses = 0

    def store(
        self,
        zStart: complex,
        zEnd: complex,
        argument: float,
    ) -> None:
        """
        Store the total argument change associated with a horizontally or
        vertically oriented range of complex numbers.

        TODO
        """
        self._cache[(zStart, zEnd)] = argument
        self.logger.debug(
            "stored value %f under key %s in estimator cache!",
            argument,
            str((zStart, zEnd)),
        )

    def retrieve(
        self,
        zStart: complex,
        zEnd: complex,
    ) -> Optional[float]:
        """
        Retrieve the total argument change associated with a horizontally or
        vertically oriented range of complex numbers. Returns `None` if the
        requested entry is not present.

        TODO
        """
        value = self._cache.get((zStart, zEnd), None)
        self.logger.debug(
            "retrieved value %s under key %s from estimator cache!",
            str(value),
            str((zStart, zEnd)),
        )
        if self.logger.isEnabledFor(DEBUG):
            self.cacheHits += 1 if value else 0
            self.cacheMisses += 1 if not value else 0
        return value

    def remove(
        self,
        zStart: complex,
        zEnd: complex,
    ) -> None:
        """
        Remove the total argument change associated with a horizontally or
        vertically oriented range of complex numbers.

        TODO
        """
        value = self._cache.pop((zStart, zEnd), None)
        self.logger.debug(
            "removed value %s under key %s from estimator cache!",
            str(value),
            str((zStart, zEnd)),
        )

    def reset(self) -> None:
        """
        TODO
        """
        self._cache.clear()
        self.cacheHits = 0
        self.cacheMisses = 0
