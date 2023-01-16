"""
Class SimpleHoloAlgorithm from the package pyzeal_algorithms.
This module defines a root finding algorithm based on a simple, straight
forward approach to the argument principle. The simplicity comes from the fact
that we avoid numeric quadrature by approximating integration of the
logarithmic derivative via changes in the complex argument of the target
function.

Authors:\n
- Philipp Schuette\n
"""

from typing import cast, Final, Literal, Tuple, Union

import numpy as np

from pyzeal_algorithms.finder_algorithm import FinderAlgorithm
from pyzeal_logging.loggable import Loggable
from pyzeal_utils.root_context import RootContext
from pyzeal_types.root_types import tRecGrid


####################
# Global Constants #
####################

# constants determining the numerical cutoff between 0 and 2*pi
TWO_PI: Final[float] = 5.0
FOUR_PI: Final[float] = 8.0
# constant determining the refinement of complex arrays for large phi values
Z_REFINE: Final[int] = 10
# default values for rootfinder arguments
DEFAULT_NUM_PTS = 6500
DEFAULT_DELTA_PHI = 0.01
DEFAULT_MAX_PRECISION = 1e-12


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
        *,
        numPts: int = DEFAULT_NUM_PTS,
        deltaPhi: float = DEFAULT_DELTA_PHI,
        maxPrecision: float = DEFAULT_MAX_PRECISION,
    ) -> None:
        r"""
        TODO
        """
        self.numPts = numPts
        self.deltaPhi = deltaPhi
        self.maxPrecision = maxPrecision
        self.logger.debug("initialized a new SimpleArgumentAlgorithm!")

    def calcRoots(self, context: RootContext) -> None:
        r"""
        TODO

        :param context: context in which the algorithm operates
        :type context: RootContext
        """
        self.logger.info(
            "starting simple argument search for %s on [%f, %f] x [%f, %f]",
            (
                context.f.__name__
                if hasattr(context.f, "__name__")
                else "<unknown>"
            ),
            context.reRan[0],
            context.reRan[1],
            context.imRan[0],
            context.imRan[1],
        )

        x1, x2 = context.reRan
        y1, y2 = context.imRan
        aZ, aPhi = self.genPhiArr(
            x1 + y1 * 1j, x2 + y1 * 1j, context, "horizontal"
        )
        bZ, bPhi = self.genPhiArr(
            x2 + y1 * 1j, x2 + y2 * 1j, context, "vertical"
        )
        cZ, cPhi = self.genPhiArr(
            x2 + y2 * 1j, x1 + y2 * 1j, context, "horizontal"
        )
        dZ, dPhi = self.genPhiArr(
            x1 + y2 * 1j, x1 + y1 * 1j, context, "vertical"
        )

        self.calcRootsRecursion(
            (aZ, bZ, cZ, dZ), (aPhi, bPhi, cPhi, dPhi), context
        )

    def genPhiArr(
        self,
        zStart: complex,
        zEnd: complex,
        context: RootContext,
        pos: Union[Literal["horizontal"], Literal["vertical"]],
    ) -> Tuple[np.ndarray, np.ndarray]:
        r"""
        Calculate an array of complex argument values from the function values
        of `self.func` on the complex line `[zStart, zEnd]`. Zeros of
        `self.func` found during this procedure are put into `resultQueue` and
        the complex line is adjusted by translating into direction `pos` by a
        small offset.

        TODO
        """
        zArr = np.linspace(zStart, zEnd, self.numPts)
        funcArr = context.f(zArr)
        zerosOnLine = np.where(funcArr == 0)[0]
        while zerosOnLine.size > 0:
            self.logger.debug(
                "simple argument found root on the line [%s, %s]",
                str(zArr[0]),
                str(zArr[-1]),
            )
            newZeros = zArr[zerosOnLine]
            # order of these zeros is not determined further, so put 0
            for pair in zip(newZeros, np.zeros_like(newZeros, dtype=int)):
                context.container.addRoot(pair, context.toFilterContext())
            # adjust line according to 'pos'
            if pos == "vertical":
                zArr += 2 * 10 ** (-context.precision[0])
            else:
                zArr += 2j * 10 ** (-context.precision[1])
            funcArr = context.f(zArr)
            zerosOnLine = np.where(funcArr == 0)[0]

        # facFuncArr is of the form f(z_{k+1})/f(z_k)
        facFuncArr = funcArr[1:] / funcArr[:-1]
        # compute change in argument between two points on the line
        phiArr = np.arctan2(facFuncArr.imag, facFuncArr.real)

        # loop over entries in phiArr larger than deltaPhi
        idxPhi = np.where(abs(phiArr) >= self.deltaPhi)[0]
        while idxPhi.size > 0:
            # refine grid between z values at large phi values
            k = idxPhi[0]
            self.logger.debug(
                "Refining the line between [%s, %s] as phi=%s",
                str(zArr[k]),
                str(zArr[k + 1]),
                str(phiArr[k]),
            )
            if abs(zArr[k] - zArr[k + 1]) < self.maxPrecision:
                break
            refinementFactor = int(Z_REFINE * abs(phiArr[k]) / self.deltaPhi)
            zArrRefinement = np.linspace(
                cast(complex, zArr[k]),
                cast(complex, zArr[k + 1]),
                refinementFactor,
            )
            funcArr = context.f(zArrRefinement)
            zerosOnLine = np.where(funcArr == 0)[0]
            while zerosOnLine.size > 0:
                newZeros = zArrRefinement[zerosOnLine]
                for pair in zip(newZeros, np.zeros_like(newZeros, dtype=int)):
                    context.container.addRoot(pair, context.toFilterContext())
                if pos == "vertical":
                    zArrRefinement += 2 * 10 ** (-context.precision[0])
                else:
                    zArrRefinement += 2j * 10 ** (-context.precision[1])
                funcArr = context.f(zArrRefinement)
                zerosOnLine = np.where(funcArr == 0)[0]

            facFuncArr = funcArr[1:] / funcArr[:-1]
            phiArrRefinement = np.arctan2(facFuncArr.imag, facFuncArr.real)

            # concatenate old and new arrays
            zArr = np.concatenate(
                (zArr[: k + 1], zArrRefinement[1:-1], zArr[k + 1 :])
            )

            phiArr = np.concatenate(
                (phiArr[:k], phiArrRefinement, phiArr[k + 1 :])
            )
            idxPhi = np.where(abs(phiArr) >= self.deltaPhi)[0]

        return zArr, phiArr

    def calcRootsRecursion(
        self, zParts: tRecGrid, phiParts: tRecGrid, context: RootContext
    ) -> None:
        r"""
        Calculates zeros of `self.func` by applying the argument principle over
        a rectangle and recursively dividing this rectangle into smaller ones.
        Zeros found are put into `resultQueue`. The finished calculation gets
        reported to the progress bar `progress` under the task id `task`.

        TODO
        """
        # calculate difference between right/left and top/bottom
        deltaRe = zParts[1][0].real - zParts[3][0].real
        deltaIm = zParts[2][0].imag - zParts[0][0].imag
        # check if the given rectangle contains at least one zero
        phi = (
            phiParts[0].sum()
            + phiParts[1].sum()
            + phiParts[2].sum()
            + phiParts[3].sum()
        )

        # check if current rectangle contains zeros
        if phi > TWO_PI:
            self.logger.debug(
                "Rectangle [%s, %s] x [%s, %s] contains zeros with phase=%s",
                str(zParts[1][0]),
                str(zParts[3][0]),
                str(zParts[2][0]),
                str(zParts[0][0]),
                str(phi),
            )
            self.logger.debug("Rectangle size is %f x %f", deltaRe, deltaIm)
            # check if desired accuracy is aquired
            if deltaRe < 10 ** (-context.precision[0]) and deltaIm < 10 ** (
                -context.precision[1]
            ):
                newZero = 0.5 * (
                    zParts[1][0].real
                    + zParts[3][0].real
                    + 1j * (zParts[2][0].imag + zParts[0][0].imag)
                )
                zOrder = int(np.round(phi / (2 * np.pi)))
                context.container.addRoot(
                    (newZero, zOrder), context.toFilterContext()
                )
                if context.progress is not None and context.task is not None:
                    context.progress.update(
                        context.task, advance=deltaRe * deltaIm
                    )
            else:
                if deltaRe / (10 ** (-context.precision[0])) > deltaIm / (
                    10 ** (-context.precision[0])
                ):
                    zPartsNew, phiPartsNew = self.divideVertical(
                        zParts, phiParts, context
                    )
                    self.calcRootsRecursion(
                        zPartsNew[0], phiPartsNew[0], context
                    )

                    self.calcRootsRecursion(
                        zPartsNew[1], phiPartsNew[1], context
                    )

                else:
                    zPartsNew, phiPartsNew = self.divideHorizontal(
                        zParts, phiParts, context
                    )
                    self.calcRootsRecursion(
                        zPartsNew[0], phiPartsNew[0], context
                    )

                    self.calcRootsRecursion(
                        zPartsNew[1], phiPartsNew[1], context
                    )
        else:
            if context.progress is not None and context.task is not None:
                context.progress.update(
                    context.task, advance=deltaRe * deltaIm
                )

    def divideVertical(
        self, zParts: tRecGrid, phiParts: tRecGrid, context: RootContext
    ) -> Tuple[Tuple[tRecGrid, tRecGrid], Tuple[tRecGrid, tRecGrid]]:
        r"""
        Divide a rectangle in the complex plane, given by its z-support points
        `zParts` and corresponding argument values `phiParts` of the function
        values of `self.func` vertically in the middle. Zeros of `self.func`
        found during the division process are put into `resultQueue`.

        TODO
        """
        reMiddle = 0.5 * (zParts[1][0].real + zParts[3][0].real)
        mIdxLow = np.where(zParts[0].real <= reMiddle)[0][-1]
        mIdxHigh = np.where(zParts[2].real <= reMiddle)[0][0]

        # create new arrays on the middle line
        zNew, phiNew = self.genPhiArr(
            complex(reMiddle, zParts[0][0].imag),
            complex(reMiddle, zParts[2][0].imag),
            context,
            "vertical",
        )
        # left rectangular part
        aZ = zParts[0][: mIdxLow + 1]
        bZ = zNew
        cZ = zParts[2][mIdxHigh:]
        dZ = zParts[3]
        aPhi = phiParts[0][: mIdxLow + 1]
        bPhi = phiNew
        cPhi = phiParts[2][mIdxHigh:]
        dPhi = phiParts[3]
        # check truncated arrays for length >= 10
        if aZ.size < 10:
            aZ, aPhi = self.genPhiArr(
                complex(dZ[0].real, aZ[0].imag),
                complex(bZ[0].real, aZ[0].imag),
                context,
                "horizontal",
            )
        if cZ.size < 10:
            cZ, cPhi = self.genPhiArr(
                complex(bZ[0].real, cZ[0].imag),
                complex(dZ[0].real, cZ[0].imag),
                context,
                "horizontal",
            )
        zTmp = (aZ, bZ, cZ, dZ)
        phiTmp = (aPhi, bPhi, cPhi, dPhi)

        # right rectangular part
        aZ = zParts[0][mIdxLow:]
        bZ = zParts[1]
        cZ = zParts[2][: mIdxHigh + 1]
        dZ = zNew[::-1]
        aPhi = phiParts[0][mIdxLow:]
        bPhi = phiParts[1]
        cPhi = phiParts[2][: mIdxHigh + 1]
        dPhi = -phiNew[::-1]
        # check truncated arrays for length >= 10
        if aZ.size < 10:
            aZ, aPhi = self.genPhiArr(
                complex(dZ[0].real, aZ[0].imag),
                complex(bZ[0].real, aZ[0].imag),
                context,
                "horizontal",
            )
        if cZ.size < 10:
            cZ, cPhi = self.genPhiArr(
                complex(bZ[0].real, cZ[0].imag),
                complex(dZ[0].real, cZ[0].imag),
                context,
                "horizontal",
            )

        return ((zTmp, (aZ, bZ, cZ, dZ)), (phiTmp, (aPhi, bPhi, cPhi, dPhi)))

    def divideHorizontal(
        self, zParts: tRecGrid, phiParts: tRecGrid, context: RootContext
    ) -> Tuple[Tuple[tRecGrid, tRecGrid], Tuple[tRecGrid, tRecGrid]]:
        r"""
        Divide a rectangle in the complex plane, given by its z-support points
        `zParts` and corresponding argument values `phiParts` of the function
        values of `self.func` horizontally in the middle. Zeros of `self.func`
        found during the division process are put into `resultQueue`.

        TODO
        """
        imagMiddle = 0.5 * (zParts[2][0].imag + zParts[0][0].imag)
        mIdxR = np.where(zParts[1].imag <= imagMiddle)[0][-1]
        mIdxL = np.where(zParts[3].imag <= imagMiddle)[0][0]
        # create new arrays on the middle line
        zNew, phiNew = self.genPhiArr(
            complex(zParts[3][0].real, imagMiddle),
            complex(zParts[1][0].real, imagMiddle),
            context,
            "horizontal",
        )
        # lower rectangular part
        aZ = zParts[0]
        bZ = zParts[1][: mIdxR + 1]
        cZ = zNew[::-1]
        dZ = zParts[3][mIdxL:]
        aPhi = phiParts[0]
        bPhi = phiParts[1][: mIdxR + 1]
        cPhi = -phiNew[::-1]
        dPhi = phiParts[3][mIdxL:]

        # check truncated arrays for length >= 10
        if bZ.size < 10:
            bZ, bPhi = self.genPhiArr(
                complex(bZ[0].real, aZ[0].imag),
                complex(bZ[0].real, cZ[0].imag),
                context,
                "vertical",
            )
        if dZ.size < 10:
            dZ, dPhi = self.genPhiArr(
                complex(dZ[0].real, cZ[0].imag),
                complex(dZ[0].real, aZ[0].imag),
                context,
                "vertical",
            )
        zTmp = (aZ, bZ, cZ, dZ)
        phiTmp = (aPhi, bPhi, cPhi, dPhi)

        # right rectangular part
        aZ = zNew
        bZ = zParts[1][mIdxR:]
        cZ = zParts[2]
        dZ = zParts[3][: mIdxL + 1]
        aPhi = phiNew
        bPhi = phiParts[1][mIdxR:]
        cPhi = phiParts[2]
        dPhi = phiParts[3][: mIdxL + 1]
        # check truncated arrays for length >= 10
        if bZ.size < 10:
            bZ, bPhi = self.genPhiArr(
                complex(bZ[0].real, aZ[0].imag),
                complex(bZ[0].real, cZ[0].imag),
                context,
                "vertical",
            )
        if dZ.size < 10:
            dZ, dPhi = self.genPhiArr(
                complex(dZ[0].real, cZ[0].imag),
                complex(dZ[0].real, aZ[0].imag),
                context,
                "vertical",
            )

        return ((zTmp, (aZ, bZ, cZ, dZ)), (phiTmp, (aPhi, bPhi, cPhi, dPhi)))
