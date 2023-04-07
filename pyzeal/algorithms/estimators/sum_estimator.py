"""
This module provides a simple argument estimator based on summation of
incremental changes in the phase of the argument.

Authors:\n
- Philipp Schuette\n
"""

from typing import Dict, Literal, Tuple, Union, cast

import numpy as np

from pyzeal.algorithms.estimators.argument_estimator import ArgumentEstimator
from pyzeal.algorithms.estimators.constants import MAX_Z_LENGTH, Z_REFINE
from pyzeal.algorithms.estimators.estimator_cache import EstimatorCache
from pyzeal.pyzeal_types.root_types import tVec
from pyzeal.utils.root_context import RootContext

# type alias for internal caches
tCache = Dict[
    Tuple[float, int],
    Dict[
        Tuple[float, Union[Literal["start"], Literal["end"]]],
        Tuple[tVec, tVec],
    ],
]


class SummationEstimator(ArgumentEstimator):
    """
    Class implementation of a simple argument estimator.

    It is based on discretizing the path of integration and summing the change
    of argument between these points to compute the integral of the logarithmic
    derivative.
    """

    __slots__ = (
        "numPts",
        "deltaPhi",
        "maxPrecision",
        "_cache",
        "cacheHorizontal",
        "cacheVertical",
    )

    def __init__(
        self,
        *,
        numPts: int,
        deltaPhi: float,
        maxPrecision: float,
        cache: EstimatorCache,
    ) -> None:
        """
        Initialize a `SummationEstimator` with given settings.

        :param numPts: Number of points used for estimation.
        :param deltaPhi: Threshold for argument change. When the change in
            argument between two points exceeds this, it will be further
            refined.
        :param maxPrecision: Maximum precision for refinement
        :param cache: Cache to store intermediate computation results.
        """
        self.numPts = numPts
        self.deltaPhi = deltaPhi
        self.maxPrecision = maxPrecision
        self._cache = cache
        # initialize additional internal caches to avoid function re-evals
        self.cacheHorizontal: tCache = {}
        self.cacheVertical: tCache = {}

        self.logger.info("initialized new phase summation based estimator...")

    # docstr-coverage:inherited
    @property
    def cache(self) -> EstimatorCache:
        return self._cache

    def calcMomentAlongLine(
        self,
        order: int,
        zStart: complex,
        zEnd: complex,
        context: RootContext,
    ) -> complex:
        r"""
        The result of this method coincides exactly with the integral of the
        logarithmic derivative as long as the increments remain below the
        threshold of :math:`\pi`. It can be proven that local function
        information is not sufficient to verify this condition in general.

        :param order: Moment to calculate
        :param zStart: Starting point of the line
        :param zEnd: End point of the line
        :param context: `RootContext` containing the necessary information
        :raises ValueError: An error is raised if the line is not
            parallel to either the real or imaginary axis.
        :return: The moment as calculated along the given line.
        """
        # look for required function values in the internal caches
        x1, y1 = zStart.real, zStart.imag
        x2, y2 = zEnd.real, zEnd.imag
        phi: complex
        # handle the case of horizontal line first
        if y1 == y2:
            phi = self.retrieveCachedHorizontal(order, x1, x2, y1, context)
        elif x1 == x2:
            phi = self.retrieveCachedVertical(order, y1, y2, x1, context)
        else:
            raise ValueError(
                f"{zStart} and {zEnd} must define an axis-parallel line!"
            )

        return phi

    def retrieveCachedHorizontal(
        self, order: int, x1: float, x2: float, y: float, context: RootContext
    ) -> complex:
        """
        Try to retrieve the moment along a horizontal line from cache,
        calculating it if necessary.

        :param order: Moment to retrieve
        :param x1: Starting point x-value
        :param x2: End point x-value
        :param y: y-value of the line
        :param context: `RootContext` containing the necessary information
        :return: The moment as calculated along the given line.
        """
        cache = self.cacheHorizontal
        # the internal caches only contain positively oriented lines
        sign = 1 if x1 < x2 else -1
        x1, x2 = sorted((x1, x2))
        if (y, order) in cache:
            if (x1, "start") in cache[(y, order)]:
                self.logger.debug(
                    "horizontal line start in internal cache found - dividing!"
                )
                value = cache[(y, order)][(x1, "start")]
                if len((indices := np.where(np.real(value[0]) <= x2)[0])) < 3:
                    self.logger.warning("must regenerate support points!")
                    newValue = self.genPhiArr(
                        order, x1 + 1j * y, x2 + 1j * y, context
                    )
                else:
                    middleIdx = indices[-1]
                    newValue = (
                        value[0][: middleIdx + 1],
                        value[1][: middleIdx + 1],
                    )
                self.storeCache(y, order, x1, x2, cache, newValue)
                return cast(float, sign * newValue[1].sum())
            if (x2, "end") in cache[(y, order)]:
                self.logger.debug(
                    "horizontal line end in internal cache found - dividing!"
                )
                value = cache[(y, order)][(x2, "end")]

                if len((indices := np.where(x1 <= np.real(value[0]))[0])) < 3:
                    self.logger.warning("must regenerate support points!")
                    newValue = self.genPhiArr(
                        order, x1 + 1j * y, x2 + 1j * y, context
                    )
                else:
                    middleIdx = indices[0]
                    newValue = (
                        value[0][middleIdx:],
                        value[1][middleIdx:],
                    )
                self.storeCache(y, order, x1, x2, cache, newValue)
                return cast(float, sign * newValue[1].sum())

        self.logger.debug("internal cache miss on horizontal line!")
        newValue = self.genPhiArr(order, x1 + 1j * y, x2 + 1j * y, context)

        if (y, order) not in cache:
            cache[(y, order)] = {}
        self.storeCache(y, order, x1, x2, cache, newValue)
        return cast(float, sign * newValue[1].sum())

    def retrieveCachedVertical(
        self, order: int, y1: float, y2: float, x: float, context: RootContext
    ) -> complex:
        """
        Try to retrieve the moment along a vertical line from cache,
        calculating it if necessary.

        :param order: Moment to retrieve
        :param y1: Starting point y-value
        :param y2: End point y-value
        :param x: x-value of the line
        :param context: `RootContext` containing the necessary information.
        :return: The moment as calculated along the given line.
        """
        cache = self.cacheVertical
        sign = 1 if y1 < y2 else -1
        y1, y2 = sorted((y1, y2))
        if (x, order) in cache:
            if (y1, "start") in cache[(x, order)]:
                self.logger.debug(
                    "vertical line start in internal cache found - dividing!"
                )
                value = cache[(x, order)][(y1, "start")]
                if len((indices := np.where(np.imag(value[0]) <= y2)[0])) < 3:
                    self.logger.warning("must regenerate support points!")
                    newValue = self.genPhiArr(
                        order, x + 1j * y1, x + 1j * y2, context
                    )
                else:
                    middleIdx = indices[-1]
                    newValue = (
                        value[0][: middleIdx + 1],
                        value[1][: middleIdx + 1],
                    )
                self.storeCache(x, order, y1, y2, cache, newValue)
                return cast(float, sign * newValue[1].sum())
            if (y2, "end") in cache[(x, order)]:
                self.logger.debug(
                    "vertical line end in internal cache found - dividing!"
                )
                value = cache[(x, order)][(y2, "end")]
                if len((indices := np.where(np.imag(value[0]) <= y2)[0])) < 3:
                    self.logger.warning("must regenerate support points!")
                    newValue = self.genPhiArr(
                        order, x + 1j * y1, x + 1j * y2, context
                    )
                else:
                    middleIdx = np.where(y1 <= np.imag(value[0]))[0][0]
                    newValue = (
                        value[0][middleIdx:],
                        value[1][middleIdx:],
                    )
                self.storeCache(x, order, y1, y2, cache, newValue)
                return cast(float, sign * newValue[1].sum())

        self.logger.debug("internal cache miss on vertical line!")
        newValue = self.genPhiArr(order, x + 1j * y1, x + 1j * y2, context)

        if (x, order) not in cache:
            cache[(x, order)] = {}
        self.storeCache(x, order, y1, y2, cache, newValue)
        return cast(float, sign * newValue[1].sum())

    def genPhiArr(
        self,
        order: int,
        zStart: complex,
        zEnd: complex,
        context: RootContext,
    ) -> Tuple[tVec, tVec]:
        """
        Calculate an array of complex argument values from the function values
        of the target function `context.f` on the complex line
        `[zStart, zEnd]`. Zeros of the target function found during this
        procedure are put into `context.container` immediately and the complex
        line is adjusted by translating into direction `pos` by a small offset.
        The number of support points on the line is adjusted dynamically.

        :param order: The moment which is to be calculated.
        :param zStart: Starting point of the line segment.
        :param zEnd: End point of the line segment.
        :param context: Context of the current calculation.
        :return: Points along with estimated change of argument between them.
        """
        if order != 0:
            raise NotImplementedError(
                f"summation estimator is not implemented for order={order}>0!"
            )

        # build the array f(z_{k+1})/f(z_k) of quotients of successive values
        zArr, funcArr = self.genFuncArr(zStart, zEnd, context, self.numPts)
        funcArr = funcArr[1:] / funcArr[:-1]
        # compute change in argument between two points on the line
        phiArr = np.arctan2(funcArr.imag, funcArr.real)

        # loop over entries in phiArr larger than deltaPhi with dynamically
        # increasing refinement size
        idxPhi = np.where(abs(phiArr) >= self.deltaPhi)[0]
        idx = 0
        while idxPhi.size > 0:
            idx += 1
            # refine grid between z values at large phi values
            k = idxPhi[0]
            self.logger.debug(
                "Refining the line between [%s, %s] because phase change=%s",
                str(zArr[k]),
                str(zArr[k + 1]),
                str(phiArr[k]),
            )
            if abs(zArr[k] - zArr[k + 1]) < self.maxPrecision:
                self.logger.warning("maximum z-refinement depth reached!")
                break
            if len(zArr) > MAX_Z_LENGTH * self.numPts:
                self.logger.warning("maximum z-length reached!")
                break
            refinementFactor = int(
                idx * Z_REFINE * abs(phiArr[k]) / self.deltaPhi
            )
            zArrRefinement, funcArr = self.genFuncArr(
                cast(complex, zArr[k]),
                cast(complex, zArr[k + 1]),
                context,
                refinementFactor,
            )
            funcArr = funcArr[1:] / funcArr[:-1]
            phiArrRefinement = np.arctan2(funcArr.imag, funcArr.real)

            # concatenate old and new arrays
            zArr = np.concatenate(
                (zArr[: k + 1], zArrRefinement[1:-1], zArr[k + 1 :])
            )

            phiArr = np.concatenate(
                (phiArr[:k], phiArrRefinement, phiArr[k + 1 :])
            )
            idxPhi = np.where(abs(phiArr) >= self.deltaPhi)[0]

        return zArr, phiArr

    def storeCache(
        self,
        z: float,
        order: int,
        start: float,
        end: float,
        cache: tCache,
        newValue: Tuple[tVec, tVec],
    ) -> None:
        """
        Store a new value in cache.

        :param z: Real or imaginary part of the line, depending on if the line
            is horizontal or vertical.
        :param order: Order of the moment to be calculated
        :param start: Real or imaginary part of the starting point, depending
            on line orientation
        :param end: Real or imaginary part of the starting point, depending
            on line orientation
        :param cache: Cache to store the new value in.
        :param newValue: New value to store.
        """
        cache[(z, order)][(start, "start")] = newValue
        cache[(z, order)][(end, "end")] = newValue
