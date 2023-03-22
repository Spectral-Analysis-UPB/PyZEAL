"""
This module contains a base class for argument estimators, which should
inherit from this class and supply a concrete implementation.

Authors:\n
- Philipp Schuette\n
"""

from abc import ABC, abstractmethod
from typing import List, Tuple

import numpy as np

from pyzeal.algorithms.estimators.estimator_cache import EstimatorCache
from pyzeal.pyzeal_logging.loggable import Loggable
from pyzeal.utils.root_context import RootContext


class ArgumentEstimator(ABC, Loggable):
    """
    Interface for argument estimators. `calcMoment` us implemented here,
    while the concrete method of evaluation is determined by overriding
    `calcMomentAlongLine`.
    """

    def calcMoment(
        self,
        order: int,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        context: RootContext,
    ) -> complex:
        """
        Calculate the `order`-th moment of the logarithmic derivative of the
        target function `context.f` along the boundary of the rectangle
        specified by `reRan` x `imRan`. The concrete method by which the
        integral of the logarithm derivative gets calculated is determined by
        overriding `calcMomentAlongLine`.

        :param order: Order of the moment to be calculated.
        :param reRan: Interval describing the real part of the rectangle
        :param imRan: Interval describing the imaginary part of the rectangle
        :param context: `RootContext` containing the necessary information.
        :return: `order`-th moment of the logarithmic derivative of 
            `context.f` along the boundary of the specified rectangle.
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
        phi: complex = 0

        # check if the requested complex line already resides in cache
        arguments: List[Tuple[complex, complex]] = [
            (x1 + y1 * 1j, x2 + y1 * 1j),
            (x2 + y1 * 1j, x2 + y2 * 1j),
            (x2 + y2 * 1j, x1 + y2 * 1j),
            (x1 + y2 * 1j, x1 + y1 * 1j),
        ]
        for zStart, zEnd in arguments:
            if entry := self.cache.retrieve(order, zStart, zEnd):
                phi += entry
            else:
                deltaPhi = self.calcMomentAlongLine(
                    order, zStart, zEnd, context
                )
                # store the missing entry in the cache
                self.cache.store(order, zStart, zEnd, deltaPhi)
                self.cache.store(order, zEnd, zStart, -deltaPhi)
                phi += deltaPhi

        self.logger.debug("estimated argument is %s", str(phi / (2.0 * np.pi)))
        return phi

    @abstractmethod
    def calcMomentAlongLine(
        self,
        order: int,
        zStart: complex,
        zEnd: complex,
        context: RootContext,
    ) -> complex:
        """Calculate the `order`-th moment of the logarithmic derivative of
        the target function `context.f` along the line given by `zStart` and
        `zEnd`. 

        :param order: Order of the moment to calculate
        :param zStart: Starting point of the line
        :param zEnd: End point of the line
        :param context: `RootContext` containing the necessary information.
        :return: The moment as calculated along the given line.
        """

    @property
    @abstractmethod
    def cache(self) -> EstimatorCache:
        """
        Returns the cache used by this argument estimator.

        :return: Cache used by this argument estimator.
        """
