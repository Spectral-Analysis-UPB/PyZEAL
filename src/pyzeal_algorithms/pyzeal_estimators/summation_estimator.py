"""
TODO

Authors:\n
- Philipp Schuette
"""

from typing import Final, Literal, Tuple, Union, cast

import numpy as np

from pyzeal_logging.loggable import Loggable
from pyzeal_types.root_types import tVec
from pyzeal_utils.root_context import RootContext

from .argument_estimator import ArgumentEstimator
from .estimator_cache import EstimatorCache

####################
# Global Constants #
####################

# constant determining the refinement of complex arrays for large phi values
Z_REFINE: Final[int] = 100
# constant determining the maximal length of z-arrays
MAX_Z_LENGTH: Final[int] = 100


class SummationEstimator(ArgumentEstimator, Loggable):
    """
    TODO
    """

    __slots__ = ("numPts", "deltaPhi", "maxPrecision")

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
        self.cache = cache
        self.logger.info("initialized new phase summation based estimator...")

    def calcMoment(
        self,
        order: int,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        context: RootContext,
    ) -> float:
        """
        Calculate the zeroth moment by summing incremental changes in the
        phase of the function values. This coincides exactly with the integral
        of the logarithmic derivative as long as the incremental changes stay
        below a certain threshold.

        TODO
        """
        if order != 0:
            raise NotImplementedError(
                "argument estimation via phase summation only works for n=0!"
            )

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

        # check if the requested argument change resides in cache
        if entry := self.cache.retrieve(x1 + y1 * 1j, x2 + y1 * 1j):
            phi += entry
        else:
            deltaPhi = self.genPhiArr(
                x1 + y1 * 1j, x2 + y1 * 1j, context, "horizontal"
            ).sum()
            # store the missing entry in the cache
            self.cache.store(x1 + y1 * 1j, x2 + y1 * 1j, deltaPhi)
            phi += deltaPhi
        if entry := self.cache.retrieve(x2 + y1 * 1j, x2 + y2 * 1j):
            phi += entry
        else:
            deltaPhi = self.genPhiArr(
                x2 + y1 * 1j, x2 + y2 * 1j, context, "vertical"
            ).sum()
            self.cache.store(x2 + y1 * 1j, x2 + y2 * 1j, deltaPhi)
            phi += deltaPhi
        if entry := self.cache.retrieve(x2 + y2 * 1j, x1 + y2 * 1j):
            phi += entry
        else:
            deltaPhi = self.genPhiArr(
                x2 + y2 * 1j, x1 + y2 * 1j, context, "horizontal"
            ).sum()
            self.cache.store(x2 + y2 * 1j, x1 + y2 * 1j, deltaPhi)
            phi += deltaPhi
        if entry := self.cache.retrieve(x1 + y2 * 1j, x1 + y1 * 1j):
            phi += entry
        else:
            deltaPhi = self.genPhiArr(
                x1 + y2 * 1j, x1 + y1 * 1j, context, "vertical"
            ).sum()
            self.cache.store(x1 + y2 * 1j, x1 + y1 * 1j, deltaPhi)
            phi += deltaPhi

        self.logger.debug("estimated argument is %f", phi / (2.0 * np.pi))
        return phi

    def genPhiArr(
        self,
        zStart: complex,
        zEnd: complex,
        context: RootContext,
        pos: Union[Literal["horizontal"], Literal["vertical"]],
    ) -> tVec:
        """
        Calculate an array of complex argument values from the function values
        of the target function `context.func` on the complex line
        `[zStart, zEnd]`. Zeros of the target function found during this
        procedure are put into `context.container` immediately and the complex
        line is adjusted by translating into direction `pos` by a small offset.

        :param zStart:
        :type zStart: complex
        :param zEnd:
        :type zEnd: complex
        :param context:
        :type context: RootContext
        :param pos:
        :type pos: `horizontal` | `vertical`
        :return:
        :rtype: NDArray[complex]
        """
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

        return phiArr
