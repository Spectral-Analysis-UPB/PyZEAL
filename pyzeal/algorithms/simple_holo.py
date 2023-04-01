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

from typing import Tuple

import numpy as np

from pyzeal.algorithms.constants import (
    DEFAULT_DELTA_PHI,
    DEFAULT_MAX_PRECISION,
    DEFAULT_NUM_PTS,
    TWO_PI,
)
from pyzeal.algorithms.estimators import EstimatorCache
from pyzeal.algorithms.estimators.argument_estimator import ArgumentEstimator
from pyzeal.algorithms.finder_algorithm import FinderAlgorithm
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.utils.root_context import RootContext
from pyzeal.utils.service_locator import ServiceLocator


class SimpleArgumentAlgorithm(FinderAlgorithm):
    """
    Class representation of a simple root finding algorithm for holomorphic
    functions based on the argument principle and the approximation of
    integrals over logarithmic derivatives via the summation of phase
    differences.
    """

    __slots__ = ("cache", "estimator")

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
        simple adaptation of the argument principle by refining an initial
        bounding rectangle until it either contains no further roots or it is
        smaller in size than the requested accuracy.

        :param numPts: the default number of support points on rectangle edges
            at the start of dynamic refinement
        :param deltaPhi: the maximal phase shift between neighboring points on
            rectangle edges before dynamic refinement starts
        :param maxPrecision: the minimal distance between neighboring points on
            rectangle edges during dynamic refinement
        """
        self.cache = EstimatorCache()
        self.estimator = ServiceLocator.tryResolve(
            ArgumentEstimator,
            estimatorType=estimatorType,
            numPts=numPts,
            deltaPhi=deltaPhi,
            maxPrecision=maxPrecision,
            cache=self.cache,
        )
        self.logger.debug(
            "initialized a new subclass of SimpleArgumentAlgorithm!"
        )

    def calcRoots(self, context: RootContext) -> None:
        """
        Start a root calculation using a straightforward argument principle
        based refinement strategy.

        This routine calculates the initially expected number of roots by
        delegating the argument calculation to its `ArgumentEstimator`
        instance. Then it delegates the actual work of recursive refinement to
        the routines `decideRefinement` and `calcRootsRecursion`.

        :param context: context in which the algorithm operates
        """
        self.logger.info(
            "starting simple argument search for %s",
            context.functionDataToString(),
        )
        # reset cache
        if self.cache.dirty():
            self.logger.info("resetting argument estimator cache...")
            self.cache.reset()

        phi = self.estimator.calcMoment(
            0, context.reRan, context.imRan, context
        ).real  # if order=0 then the result is (theoretically) an int
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
        Decide which way the current search area should be subdivided and
        calculate roots in the subdivided areas. The simple strategy consists
        of the choices (1) return, if argument indicates no roots, (2) place
        root in `context.container` if roots present and accuracy attained, or
        (3) subdivide further if roots present but accuracy not yet attained.

        :param reRan: Real part of current search Range
        :param imRan: Imaginary part of current search range
        :param phi: Change in argument along the boundary of the current range
        :param context: `RootContext` in which the algorithm operates
        """
        # calculate difference between right/left and top/bottom
        x1, x2 = reRan
        y1, y2 = imRan
        deltaRe = x2 - x1
        deltaIm = y2 - y1

        # check if current rectangle contains zeros
        if phi < TWO_PI:
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
            phi = self.calculateRefinedMoment(
                (x1, midPoint), (y1, y2), context
            )
            self.decideRefinement((x1, midPoint), (y1, y2), phi, context)
            self.cache.remove(0, x1 + y2 * 1j, x1 + y1 * 1j)
            phi = self.calculateRefinedMoment(
                (midPoint, x2), (y1, y2), context
            )
            self.decideRefinement((midPoint, x2), (y1, y2), phi, context)
            self.cache.remove(0, x2 + y1 * 1j, x2 + y2 * 1j)
        else:
            midPoint = (y1 + y2) / 2
            phi = self.calculateRefinedMoment(
                (x1, x2), (y1, midPoint), context
            )
            self.decideRefinement((x1, x2), (y1, midPoint), phi, context)
            self.cache.remove(0, x1 + y1 * 1j, x2 + y1 * 1j)
            phi = self.calculateRefinedMoment(
                (x1, x2), (midPoint, y2), context
            )
            self.decideRefinement((x1, x2), (midPoint, y2), phi, context)
            self.cache.remove(0, x2 + y2 * 1j, x1 + y2 * 1j)

    def calculateRefinedMoment(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        context: RootContext,
    ) -> float:
        """
        Recursively calculate roots in the given search range according to
        `context`.

        :param reRan: Real part of current search range
        :param imRan: Imaginary part of current search range
        :param context: `RootContext` in which the algorithm operates
        """
        # check if the given rectangle contains at least one zero
        phi: float = self.estimator.calcMoment(
            0, reRan=reRan, imRan=imRan, context=context
        ).real
        self.logger.debug(
            "simple argument recursively refined with total phase=%f",
            phi / (2.0 * np.pi),
        )

        return phi

    @staticmethod
    def getRootFromRectangle(
        right: float,
        left: float,
        top: float,
        bottom: float,
        phi: float,
        context: RootContext,
    ) -> None:
        """
        Compute the location of a root in a sufficiently small rectangle and
        update the progress bar accordingly.

        :param right: right boundary of the rectangle
        :param left: left boundary of the rectangle
        :param top: top boundary of the rectangle
        :param bottom: bottom boundary of the rectangle
        :param phi: the total argument within the rectangle
        :param context: overall context of the current calculation
        """
        newZero = (left + right + 1j * (bottom + top)) / 2.0
        zOrder = int(np.round(phi / (2 * np.pi)))
        context.container.addRoot((newZero, zOrder), context.toFilterContext())
        if context.progress is not None and context.task is not None:
            context.progress.update(
                context.task,
                advance=(right.real - left.real) * (top.imag - bottom.imag),
            )
