"""
TODO

Authors:\n
- Philipp Schuette\n
"""

from abc import ABC, abstractmethod
from typing import List, Tuple

import numpy as np

from pyzeal_algorithms.pyzeal_estimators.estimator_cache import EstimatorCache
from pyzeal_logging.loggable import Loggable
from pyzeal_utils.root_context import RootContext


class ArgumentEstimator(ABC, Loggable):
    """
    TODO
    """

    def calcMoment(
        self,
        order: int,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        context: RootContext,
    ) -> float:
        """
        Calculate the `order`-th moment of the logarithmic derivative of the
        target function `context.f` along the boundary of the rectangle
        specified by `reRan` x `imRan`. The concrete method by which the
        integral of the logarithm derivative gets calculated is determined by
        overriding `calcMomentAlongLine`.

        TODO
        """
        x1, x2 = reRan
        y1, y2 = imRan
        self.logger.debug(
            "estimating argument for rectangle [%f, %f] x [%f, %f]!",
            x1,
            x2,
            y1,
            y2,
        )
        phi: float = 0

        # check if the requested complex line already resides in cache
        arguments: List[Tuple[complex, complex]] = [
            (x1 + y1 * 1j, x2 + y1 * 1j),
            (x2 + y1 * 1j, x2 + y2 * 1j),
            (x2 + y2 * 1j, x1 + y2 * 1j),
            (x1 + y2 * 1j, x1 + y1 * 1j),
        ]
        for zStart, zEnd in arguments:
            if entry := self.cache.retrieve(zStart, zEnd):
                phi += entry
            else:
                deltaPhi = self.calcMomentAlongLine(
                    order, zStart, zEnd, context
                )
                # store the missing entry in the cache
                self.cache.store(zStart, zEnd, deltaPhi)
                phi += deltaPhi

        self.logger.debug("estimated argument is %f", phi / (2.0 * np.pi))
        return phi

    @abstractmethod
    def calcMomentAlongLine(
        self,
        order: int,
        zStart: complex,
        zEnd: complex,
        context: RootContext,
    ) -> float:
        """
        TODO
        """

    @property
    @abstractmethod
    def cache(self) -> EstimatorCache:
        """
        TODO
        """
