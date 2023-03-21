"""
A concrete argument estimator using simple summation of phase changes.

Authors:\n
- Philipp Schuette\n
"""

from typing import Dict, Final, Literal, Tuple, Union, cast

import numpy as np

from pyzeal.algorithms.estimators.argument_estimator import ArgumentEstimator
from pyzeal.algorithms.estimators.estimator_cache import EstimatorCache
from pyzeal.pyzeal_logging.loggable import Loggable
from pyzeal.pyzeal_types.root_types import tVec
from pyzeal.utils.root_context import RootContext

####################
# Global Constants #
####################

# constant determining the refinement of complex arrays for large phi values
Z_REFINE: Final[int] = 100
# constant determining the maximal length of z-arrays
MAX_Z_LENGTH: Final[int] = 100
# type alias for internal caches
tCache = Dict[
    Tuple[float, int],
    Dict[
        Tuple[float, Union[Literal["start"], Literal["end"]]],
        Tuple[tVec, tVec],
    ],
]


class SummationEstimator(ArgumentEstimator, Loggable):
    """
    TODO.
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
        TODO
        """
        self.numPts = numPts
        self.deltaPhi = deltaPhi
        self.maxPrecision = maxPrecision
        self._cache = cache
        # initialize additional internal caches to avoid function re-evals
        self.cacheHorizontal: tCache = {}
        self.cacheVertical: tCache = {}

        self.logger.info("initialized new phase summation based estimator...")

    @property
    def cache(self) -> EstimatorCache:
        """
        TODO
        """
        return self._cache

    def calcMomentAlongLine(
        self,
        order: int,
        zStart: complex,
        zEnd: complex,
        context: RootContext,
    ) -> complex:
        r"""
        Calculate the total complex argument along a line in the complex plane
        by summing incremental changes in the phase of the function values.

        The result of this method coincides exactly with the integral of the
        logarithmic derivative as long as the increments remain below the
        threshold of :math:`\pi`. It can be proven that local function
        information is not sufficient to verify this condition in general.

        TODO.
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
        TODO
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
                middleIdx = np.where(np.real(value[0]) <= x2)[0][-1]
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
                middleIdx = np.where(x1 <= np.real(value[0]))[0][0]
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
        TODO.
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
                middleIdx = np.where(np.imag(value[0]) <= y2)[0][-1]
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

        :param order:
        :param zStart:
        :param zEnd:
        :param context:
        :return:
        """
        if order != 0:
            raise NotImplementedError(
                f"summation estimator is not implemented for order={order}>0!"
            )
        pos = "horizontal" if zStart.imag == zEnd.imag else "vertical"
        zArr = np.linspace(zStart, zEnd, self.numPts)
        funcArr = context.f(zArr)
        zerosOnLine = np.where(funcArr == 0)[0]
        while zerosOnLine.size > 0:
            self.logger.debug(
                "simple argument found %d roots on the line [%s, %s]",
                zerosOnLine.size,
                str(zArr[0]),
                str(zArr[-1]),
            )
            # order of these zeros is not determined further, so put 0
            for newRoot in zArr[zerosOnLine]:
                context.container.addRoot(
                    (newRoot, 0), context.toFilterContext()
                )
            # adjust line according to 'pos'
            if pos == "vertical":
                zArr += 2 * 10 ** (-context.precision[0])
            else:
                zArr += 2j * 10 ** (-context.precision[1])
            funcArr = context.f(zArr)
            zerosOnLine = np.where(funcArr == 0)[0]

        # build the array f(z_{k+1})/f(z_k) of quotients of successive values
        funcArr = funcArr[1:] / funcArr[:-1]
        # compute change in argument between two points on the line
        phiArr = np.arctan2(funcArr.imag, funcArr.real)

        # loop over entries in phiArr larger than deltaPhi
        idxPhi = np.where(abs(phiArr) >= self.deltaPhi)[0]
        # increase the refinement size periodically
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
            zArrRefinement = np.linspace(
                cast(complex, zArr[k]),
                cast(complex, zArr[k + 1]),
                refinementFactor,
            )
            funcArr = context.f(zArrRefinement)
            zerosOnLine = np.where(funcArr == 0)[0]
            while zerosOnLine.size > 0:
                for newZero in zArrRefinement[zerosOnLine]:
                    context.container.addRoot(
                        (newZero, 0), context.toFilterContext()
                    )
                if pos == "vertical":
                    zArrRefinement += 2 * 10 ** (-context.precision[0])
                else:
                    zArrRefinement += 2j * 10 ** (-context.precision[1])
                funcArr = context.f(zArrRefinement)
                zerosOnLine = np.where(funcArr == 0)[0]

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
        TODO.

        :param z: _description_
        :param order: _description_
        :param start: _description_
        :param end: _description_
        :param cache: _description_
        :param newValue: _description_
        """
        cache[(z, order)][(start, "start")] = newValue
        cache[(z, order)][(end, "end")] = newValue
