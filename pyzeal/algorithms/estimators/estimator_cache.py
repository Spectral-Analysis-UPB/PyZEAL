"""
This module provides a simple cache to store and retrieve intermediate
results during computation.

Authors:\n
- Philipp Schuette
"""

from logging import DEBUG
from typing import Dict, Optional, Tuple

from pyzeal.pyzeal_logging.loggable import Loggable


class EstimatorCache(Loggable):
    """
    A simple in-memory cache that can store and retrieve total argument changes
    along horizontal and vertical lines in the complex plane.
    """

    __slots__ = ("_cache", "cacheHits", "cacheMisses")

    def __init__(self) -> None:
        """
        Initializes a new `EstimatorCache`.
        """
        self._cache: Dict[int, Dict[Tuple[complex, complex], complex]] = {}
        self.logger.info("initialized a new argument estimator cache...")
        # cache hits and misses are only recorded if logging is set to DEBUG
        self.cacheHits = 0
        self.cacheMisses = 0

    def store(
        self,
        order: int,
        zStart: complex,
        zEnd: complex,
        argument: complex,
    ) -> None:
        """
        Store the total argument change associated with a horizontally or
        vertically oriented range of complex numbers.

        :param order: Order of the moment to be stored
        :param zStart: Starting point of the line
        :param zEnd: End point of the line
        :param argument: Total argument change
        """
        if (orderCache := self._cache.get(order, None)) is None:
            self._cache[order] = {(zStart, zEnd): argument}
        else:
            orderCache[(zStart, zEnd)] = argument
        self.logger.debug(
            "stored value %s under key (%s, %d) in estimator cache!",
            str(argument),
            str((order, (zStart, zEnd))),
            order,
        )

    def retrieve(
        self,
        order: int,
        zStart: complex,
        zEnd: complex,
    ) -> Optional[complex]:
        """
        Retrieve the total argument change associated with a horizontally or
        vertically oriented range of complex numbers. Returns `None` if the
        requested entry is not present.

        :param order: Order of the moment to be retrieved
        :param zStart: Starting point of the line
        :param zEnd: End point of the line
        :return: Total argument change if the cache contains a value, else
            None is returned.
        """
        if (orderCache := self._cache.get(order, None)) is None:
            value = None
        else:
            value = orderCache.get((zStart, zEnd), None)
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
        order: int,
        zStart: complex,
        zEnd: complex,
    ) -> None:
        """
        Remove the total argument change associated with a horizontally or
        vertically oriented range of complex numbers.

        :param order: Order of the moment to remove
        :param zStart: Starting point of the line
        :param zEnd: End point of the line
        """
        if order in self._cache:
            value = self._cache[order].pop((zStart, zEnd), None)
            self.logger.debug(
                "removed value %s under key %s from estimator cache!",
                str(value),
                str((zStart, zEnd)),
            )

    def dirty(self) -> bool:
        """
        Returns `True` if the cache contains anything.

        :return: `True` if the cache contains anything.
        """
        return len(self._cache) > 0

    def reset(self) -> None:
        """
        Resets the cache by clearing all stored values and resetting
        the hit and miss counters.
        """
        self._cache.clear()
        self.cacheHits = 0
        self.cacheMisses = 0
