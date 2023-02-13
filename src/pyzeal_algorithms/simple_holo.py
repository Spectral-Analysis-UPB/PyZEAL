"""
Class SimpleHoloAlgorithm from the package pyzeal_algorithms.
This module defines a root finding algorithm based on a simple, straight
forward approach to the argument principle. The simplicity comes from the fact
that we avoid numeric quadrature by approximating integration of the
logarithmic derivative via changes in the complex argument of the target
function. Due to the possibility of overlooking large changes in the complex
argument this algorithm is not completely reliable, see [Henrici].

Authors:\n
- Philipp Schuette\n
"""

from typing import Final, Tuple

import numpy as np

from pyzeal_algorithms.finder_algorithm import FinderAlgorithm
from pyzeal_algorithms.pyzeal_estimators import EstimatorCache
from pyzeal_logging.loggable import Loggable
from pyzeal_types.estimator_types import EstimatorTypes
from pyzeal_utils.pyzeal_factories.estimator_factory import EstimatorFactory
from pyzeal_utils.root_context import RootContext

####################
# Global Constants #
####################

# constants determining the numerical cutoff between 0 and 2*pi
TWO_PI: Final[float] = 5.0
FOUR_PI: Final[float] = 8.0
# default values for the argument estimator
DEFAULT_NUM_PTS = 6500
DEFAULT_DELTA_PHI = 0.01
DEFAULT_MAX_PRECISION = 1e-10


class SimpleArgumentAlgorithm(FinderAlgorithm, Loggable):
    """
    Class representation of a simple root finding algorithm for holomorphic
    functions based on the argument principle and the approximation of
    integrals over logarithmic derivatives via the summation of phase
    differences.
    """

    __slots__ = ("numPts", "deltaPhi", "maxPrecision")

    def __init__(
        self,
        estimatorType: EstimatorTypes,
        *,
        numPts: int = DEFAULT_NUM_PTS,
        deltaPhi: float = DEFAULT_DELTA_PHI,
        maxPrecision: float = DEFAULT_MAX_PRECISION,
    ) -> None:
        """
        Initialize a root finding algorithm that employs a straightforward,
        simple adaptation of the argument principle which does not require
        numerical quadrature.

        :param numPts:
        :type numPts: int
        :param deltaPhi:
        :type deltaPhi: float
        :param maxPrecision:
        :type maxPrecision: float
        """
        self.cache = EstimatorCache()
        self.estimator = EstimatorFactory.getConcreteEstimator(
            estimatorType=estimatorType,
            numPts=numPts,
            deltaPhi=deltaPhi,
            maxPrecision=maxPrecision,
            cache=self.cache,
        )
        self.logger.debug("initialized a new SimpleArgumentAlgorithm!")

    def calcRoots(self, context: RootContext) -> None:
        """
        Start a root calculation using a straightforward argument principle
        based refinement strategy. This routine calculates the initially
        expected number of roots by delegating the argument calculation to its
        `ArgumentEstimator` instance. Then it delegates the actual
        work of recursive refinement to the routines `decideRefinement` and
        `calcRootsRecursion`.

        :param context: context in which the algorithm operates
        :type context: RootContext
        """
        self.logger.info(
            "starting simple argument search for %s",
            context.functionDataToString(),
        )
        # reset cache
        self.logger.info("resetting argument estimator cache...")
        self.cache.reset()

        phi = self.estimator.calcMoment(
            0, context.reRan, context.imRan, context
        )
        self.decideRefinement(context.reRan, context.imRan, phi, context)
        self.logger.debug(
            "cache hits/misses: %d/%d (= %.03f)",
            self.cache.cacheHits,
            self.cache.cacheMisses + self.cache.cacheHits,
            round(
                self.cache.cacheHits
                / (self.cache.cacheMisses + self.cache.cacheMisses or 1),
                3,
            ),
        )

    def decideRefinement(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        phi: float,
        context: RootContext,
    ) -> None:
        """
        TODO
        """
        # calculate difference between right/left and top/bottom
        x1, x2 = reRan
        y1, y2 = imRan
        deltaRe = x2 - x1
        deltaIm = y2 - y1

        # check if current rectangle contains zeros
        if phi <= TWO_PI:
            if context.progress is not None and context.task is not None:
                context.progress.update(
                    context.task, advance=deltaRe * deltaIm
                )
            return

        # the current rectangle does contain (at least one) zero(s)
        self.logger.debug(
            "Rectangle [%s, %s] x [%s, %s] contains zeros!",
            str(x1),
            str(x2),
            str(y1),
            str(y2),
        )
        self.logger.debug("Rectangle diameters are %f x %f", deltaRe, deltaIm)

        # check if desired accuracy is aquired
        epsReal = 10 ** (-context.precision[0])
        epsImag = 10 ** (-context.precision[1])
        if deltaRe < epsReal and deltaIm < epsImag:
            SimpleArgumentAlgorithm.getRootFromRectangle(
                x2, x1, y2, y1, phi, context
            )
            return

        # the current box contains a root and must be refined further
        if deltaRe / epsReal > deltaIm / epsImag:
            midPoint = (x1 + x2) / 2
            self.calcRootsRecursion((x1, midPoint), (y1, y2), context)
            self.cache.remove(x1 + y2 * 1j, x1 + y1 * 1j)
            self.calcRootsRecursion((midPoint, x2), (y1, y2), context)
            self.cache.remove(x2 + y1 * 1j, x2 + y2 * 1j)
        else:
            midPoint = (y1 + y2) / 2
            self.calcRootsRecursion((x1, x2), (y1, midPoint), context)
            self.cache.remove(x1 + y1 * 1j, x2 + y1 * 1j)
            self.calcRootsRecursion((x1, x2), (midPoint, y2), context)
            self.cache.remove(x2 + y2 * 1j, x1 + y2 * 1j)

    def calcRootsRecursion(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        context: RootContext,
    ) -> None:
        """
        TODO
        """
        # check if the given rectangle contains at least one zero
        phi = self.estimator.calcMoment(
            0, reRan=reRan, imRan=imRan, context=context
        )
        self.logger.debug(
            "simple argument recursively refined with total phase=%f",
            phi / (2.0 * np.pi),
        )

        self.decideRefinement(reRan, imRan, phi, context)

    @staticmethod
    def getRootFromRectangle(
        right: float,
        left: float,
        top: float,
        bottom: float,
        phi: float,
        context: RootContext,
    ) -> None:
        """Compute the location of a root in a sufficiently small rectangle
        and update the progress bar

        :param right: _description_
        :type right: complex
        :param left: _description_
        :type left: complex
        :param top: _description_
        :type top: complex
        :param bottom: _description_
        :type bottom: complex
        :param phi: _description_
        :type phi: float
        :param context: _description_
        :type context: RootContext
        """
        newZero = (left + right + 1j * (bottom + top)) / 2.0
        zOrder = int(np.round(phi / (2 * np.pi)))
        context.container.addRoot((newZero, zOrder), context.toFilterContext())
        if context.progress is not None and context.task is not None:
            context.progress.update(
                context.task,
                advance=(right.real - left.real) * (top.imag - bottom.imag),
            )
