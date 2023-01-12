#!/usr/bin/python3
"""
Module simple_argument.py of the pyzeal package.
This module contains a simple implementation of a root finder based on the
argument principle and integration of the logarithmic derivative by calculating
the total change in argument along a curve.

Authors:\n
- Philipp Schuette\n
"""

import os
import signal
from multiprocessing import Manager, Pool
from typing import Callable, Final, List, Optional, Tuple, cast

import numpy as np
from rich.progress import Progress, SpinnerColumn, TaskID, TimeElapsedColumn
from scipy.optimize import newton
from pyzeal_logging.config import initLogger
from pyzeal_types.root_types import (
    MyManager,
    tErrVec,
    tQueue,
    tRecGrid,
    tResVec,
    tVec,
)
from deprecated.filter_roots import filterCoincidingRoots

#################
# Logging Setup #
#################

logger = initLogger("simple_argument")


####################
# Global Constants #
####################

# os.cpu_count() might return None, in that case assume single core
CPU_COUNT: Final[int] = os.cpu_count() or 1
# constants determining the numerical cutoff between 0 and 2*pi
TWO_PI: Final[float] = 5.0
FOUR_PI: Final[float] = 8.0
# constant determining the refinement of complex arrays for large phi values
Z_REFINE: Final[int] = 10
# default values for rootfinder arguments
DEFAULT_NUM_PTS = 6500
DEFAULT_DELTA_PHI = 0.01
DEFAULT_MAX_PRECISION = 1e-12


#################################
# Holomorphic Root Finder Class #
#################################


class HoloRootFinder:
    r"""
    Class used to find roots and associated orders of holomorphic functions via
    the argument principle.
    """

    __slots__ = (
        "func",
        "_res",
        "_err",
        "epsCplx",
        "numPts",
        "deltaPhi",
        "maxPrecision",
        "funcArgs",
    )

    def __init__(
        self,
        func: Callable[..., tVec],
        prevRes: Optional[tResVec] = None,
        prevErr: Optional[tErrVec] = None,
        epsCplx: complex = 1e-4 * (1 + 1j),
        funcArgs: Tuple = (),
    ) -> None:
        """Initialize an argument-based rootfinder.

        :param func: Target function
        :type func: Callable[..., tVec]
        :param prevRes: Known zeroes with their corresponding orders,
            defaults to None
        :type prevRes: Optional[tResVec]
        :param prevErr: Errors associated to known roots,
            defaults to None
        :type prevErr: Optional[tErrVec]
        :param epsCplx: Desired accuracy, defaults to 1e-4*(1 + 1j)
        :type epsCplx: complex, optional
        :param funcArgs: Additional arguments for the target function,
            defaults to ()
        :type funcArgs: Tuple, optional
        """
        self.func = func
        self.funcArgs = funcArgs
        self.epsCplx = epsCplx
        self.numPts = DEFAULT_NUM_PTS
        self.deltaPhi = DEFAULT_DELTA_PHI
        self.maxPrecision = DEFAULT_MAX_PRECISION
        if prevRes is None:
            self._res: List[Tuple[complex, int]] = []
            self._err: List[complex] = []
        else:
            if prevErr is None:
                prevErr = [self.epsCplx for root in prevRes]
            self._res, self._err = filterCoincidingRoots(
                prevRes, prevErr, returnLists=True
            )
        if hasattr(func, "__name__"):
            logger.info(
                "Initialized argument-principle-Rootfinder for %s",
                func.__name__,
            )
        else:
            logger.info(
                "Initialized argument-principle-Rootfinder for an\
                unnamed function"
            )

    def __str__(self) -> str:
        return f"Holomorphic root finder for {self.func.__name__}"

    @property
    def res(self) -> np.ndarray:
        """Getter method for calculated roots of Rootfinder instances."""
        if len(self._res) != 0:
            return np.sort_complex(np.array(self._res)[:, 0])
        return np.array([], dtype=np.complex128)

    @property
    def order(self) -> np.ndarray:
        """Getter method for zero orders of Rootfinder instances."""
        if len(self._res) != 0:
            idx = np.argsort(np.array(self._res)[:, 0])
            orders = np.array(self._res)[idx, 1].real
            return orders.astype(np.int8)  # type: ignore
        return np.array([], dtype=np.int8)

    @property
    def err(self) -> np.ndarray:
        r"""Getter method for errors of Rootfinder instances."""
        if len(self._res) != 0:
            idx = np.argsort(np.array(self._res)[:, 0])
            return np.array(self._err)[idx]  # type: ignore
        return np.array([], dtype=np.complex128)

    def addRoots(
        self, newRoots: tResVec, newErrors: tErrVec, recalcOrders: bool = False
    ) -> None:
        r"""
        Add new roots to the `_res` attribute of the Rootfinder instance.

        :param newRoots: array of roots together with their root order
        :type newRoots: List[Tuple[complex, int]]
        :param newErrors: array of errors associated with each root
        :type newErrors: List[complex]
        :param recalcOrders: whether the root orders of two coinciding roots
            should be properly recalculated, otherwise the smaller root order
            is kept, defaults to False
        :type recalcOrders: bool, optional
        """
        if isinstance(newRoots, np.ndarray):
            newRoots = list(
                zip(
                    newRoots[:, 0].tolist(),
                    newRoots[:, 1].real.astype(int).tolist(),
                )
            )
        if isinstance(newErrors, np.ndarray):
            newErrors = list(newErrors)

        self._res.extend(newRoots)
        self._err.extend(newErrors)

        self._res, self._err = filterCoincidingRoots(
            self._res, self._err, recalcOrders=recalcOrders, returnLists=True
        )

    def genPhiArr(
        self, zStart: complex, zEnd: complex, resultQueue: tQueue, pos: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        r"""
        Calculate an array of complex argument values from the function values
        of `self.func` on the complex line `[zStart, zEnd]`. Zeros of
        `self.func` found during this procedure are put into `resultQueue` and
        the complex line is adjusted by translating into direction `pos` by a
        small offset.
        """
        zArr = np.linspace(zStart, zEnd, self.numPts)
        funcArr = self.func(zArr, *self.funcArgs)
        zerosOnLine = np.where(funcArr == 0)[0]
        while zerosOnLine.size > 0:
            logger.debug(f"Root found on the line [{zArr[0]}, {zArr[-1]}]")
            newZeros = zArr[zerosOnLine]
            # order of these zeros is not determined further, so put 0
            for pair in zip(newZeros, np.zeros_like(newZeros, dtype=int)):
                resultQueue.put(pair)
            # adjust line according to 'pos'
            if pos == "vertical":
                zArr += 2 * self.epsCplx.real
            else:
                zArr += 2j * self.epsCplx.imag
            funcArr = self.func(zArr, *self.funcArgs)
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
            logger.debug(
                f"Refining the line between [{zArr[k]}, {zArr[k+1]}]\
                 as phi={phiArr[k]}"
            )
            if abs(zArr[k] - zArr[k + 1]) < self.maxPrecision:
                break
            refinementFactor = int(Z_REFINE * abs(phiArr[k]) / self.deltaPhi)
            zArrRefinement = np.linspace(
                zArr[k], zArr[k + 1], refinementFactor
            )
            funcArr = self.func(zArrRefinement, *self.funcArgs)
            zerosOnLine = np.where(funcArr == 0)[0]
            while zerosOnLine.size > 0:
                newZeros = zArrRefinement[zerosOnLine]
                for pair in zip(newZeros, np.zeros_like(newZeros, dtype=int)):
                    resultQueue.put(pair)
                if pos == "vertical":
                    zArrRefinement += 2 * self.epsCplx.real
                else:
                    zArrRefinement += 2j * self.epsCplx.imag
                funcArr = self.func(zArrRefinement, *self.funcArgs)
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

    def divideVertical(
        self, zParts: tRecGrid, phiParts: tRecGrid, resultQueue: tQueue
    ) -> Tuple[Tuple[tRecGrid, tRecGrid], Tuple[tRecGrid, tRecGrid]]:
        r"""
        Divide a rectangle in the complex plane, given by its z-support points
        `zParts` and corresponding argument values `phiParts` of the function
        values of `self.func` vertically in the middle. Zeros of `self.func`
        found during the division process are put into `resultQueue`.
        """
        reMiddle = 0.5 * (zParts[1][0].real + zParts[3][0].real)
        mIdxLow = np.where(zParts[0].real <= reMiddle)[0][-1]
        mIdxHigh = np.where(zParts[2].real <= reMiddle)[0][0]

        # create new arrays on the middle line
        zNew, phiNew = self.genPhiArr(
            complex(reMiddle, zParts[0][0].imag),
            complex(reMiddle, zParts[2][0].imag),
            resultQueue,
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
                resultQueue,
                "horizontal",
            )
        if cZ.size < 10:
            cZ, cPhi = self.genPhiArr(
                complex(bZ[0].real, cZ[0].imag),
                complex(dZ[0].real, cZ[0].imag),
                resultQueue,
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
                resultQueue,
                "horizontal",
            )
        if cZ.size < 10:
            cZ, cPhi = self.genPhiArr(
                complex(bZ[0].real, cZ[0].imag),
                complex(dZ[0].real, cZ[0].imag),
                resultQueue,
                "horizontal",
            )

        return ((zTmp, (aZ, bZ, cZ, dZ)), (phiTmp, (aPhi, bPhi, cPhi, dPhi)))

    def divideHorizontal(
        self, zParts: tRecGrid, phiParts: tRecGrid, resultQueue: tQueue
    ) -> Tuple[Tuple[tRecGrid, tRecGrid], Tuple[tRecGrid, tRecGrid]]:
        r"""
        Divide a rectangle in the complex plane, given by its z-support points
        `zParts` and corresponding argument values `phiParts` of the function
        values of `self.func` horizontally in the middle. Zeros of `self.func`
        found during the division process are put into `resultQueue`.
        """
        imagMiddle = 0.5 * (zParts[2][0].imag + zParts[0][0].imag)
        mIdxR = np.where(zParts[1].imag <= imagMiddle)[0][-1]
        mIdxL = np.where(zParts[3].imag <= imagMiddle)[0][0]
        # create new arrays on the middle line
        zNew, phiNew = self.genPhiArr(
            complex(zParts[3][0].real, imagMiddle),
            complex(zParts[1][0].real, imagMiddle),
            resultQueue,
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
                resultQueue,
                "vertical",
            )
        if dZ.size < 10:
            dZ, dPhi = self.genPhiArr(
                complex(dZ[0].real, cZ[0].imag),
                complex(dZ[0].real, aZ[0].imag),
                resultQueue,
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
                resultQueue,
                "vertical",
            )
        if dZ.size < 10:
            dZ, dPhi = self.genPhiArr(
                complex(dZ[0].real, cZ[0].imag),
                complex(dZ[0].real, aZ[0].imag),
                resultQueue,
                "vertical",
            )

        return ((zTmp, (aZ, bZ, cZ, dZ)), (phiTmp, (aPhi, bPhi, cPhi, dPhi)))

    def calcRootsRecursion(
        self,
        zParts: tRecGrid,
        phiParts: tRecGrid,
        resultQueue: tQueue,
        progress: Progress,
        task: TaskID,
    ) -> None:
        r"""
        Calculates zeros of `self.func` by applying the argument principle over
        a rectangle and recursively dividing this rectangle into smaller ones.
        Zeros found are put into `resultQueue`. The finished calculation gets
        reported to the progress bar `progress` under the task id `task`.
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
            logger.debug(
                f"Rectangle [{zParts[1][0]}, {zParts[3][0]}] x\
                 [{zParts[2][0]}, {zParts[0][0]}] contains\
                 zeros with total phi={phi}"
            )
            logger.debug(f"Rectangle size is {deltaRe} x {deltaIm}")
            # check if desired accuracy is aquired
            if deltaRe < self.epsCplx.real and deltaIm < self.epsCplx.imag:
                newZero = 0.5 * (
                    zParts[1][0].real
                    + zParts[3][0].real
                    + 1j * (zParts[2][0].imag + zParts[0][0].imag)
                )
                zOrder = int(np.round(phi / (2 * np.pi)))
                resultQueue.put((newZero, zOrder))
                progress.update(task, advance=deltaRe * deltaIm)
            else:
                if deltaRe / self.epsCplx.real > deltaIm / self.epsCplx.imag:
                    zPartsNew, phiPartsNew = self.divideVertical(
                        zParts, phiParts, resultQueue
                    )
                    self.calcRootsRecursion(
                        zPartsNew[0],
                        phiPartsNew[0],
                        resultQueue,
                        progress,
                        task,
                    )

                    self.calcRootsRecursion(
                        zPartsNew[1],
                        phiPartsNew[1],
                        resultQueue,
                        progress,
                        task,
                    )

                else:
                    zPartsNew, phiPartsNew = self.divideHorizontal(
                        zParts, phiParts, resultQueue
                    )
                    self.calcRootsRecursion(
                        zPartsNew[0],
                        phiPartsNew[0],
                        resultQueue,
                        progress,
                        task,
                    )

                    self.calcRootsRecursion(
                        zPartsNew[1],
                        phiPartsNew[1],
                        resultQueue,
                        progress,
                        task,
                    )
        else:
            progress.update(task, advance=deltaRe * deltaIm)

    def setupWorker(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        resultQueue: tQueue,
        progress: Progress,
        task: TaskID,
    ) -> None:
        r"""
        Driver routine for `self.calcRootsRecursion` meant for execution in a
        single process. Takes the same arguments.
        """
        x1, x2 = reRan
        y1, y2 = imRan
        # The search area as given by (reRan, imRan) is split up into 4 edges:
        # (x1,y2) -c- (x2,y2)
        #    |           |
        #    d           b
        #    |           |
        # (x1,y1) -a- (x2,y1)
        aZ, aPhi = self.genPhiArr(
            x1 + y1 * 1j, x2 + y1 * 1j, resultQueue, "horizontal"
        )
        bZ, bPhi = self.genPhiArr(
            x2 + y1 * 1j, x2 + y2 * 1j, resultQueue, "vertical"
        )
        cZ, cPhi = self.genPhiArr(
            x2 + y2 * 1j, x1 + y2 * 1j, resultQueue, "horizontal"
        )
        dZ, dPhi = self.genPhiArr(
            x1 + y2 * 1j, x1 + y1 * 1j, resultQueue, "vertical"
        )

        self.calcRootsRecursion(
            (aZ, bZ, cZ, dZ),
            (aPhi, bPhi, cPhi, dPhi),
            resultQueue,
            progress,
            task,
        )

    def initWorker(self) -> None:
        r"""
        Initialization function for workers executing `self.setupWorker`. This
        step is necessary to guarantee correct processing of user signals
        `ctrl+c`.
        """
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def calcRoots(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        epsCplx: Optional[complex] = None,
        *,
        numPts: Optional[int] = None,
        deltaPhi: Optional[float] = None,
        maxPrecision: Optional[float] = None,
    ) -> None:
        r"""
        Driver function for parallel execution of `self.calcRootsRecursion`.

        TODO: only display progress bar in verbose mode?!
        """
        if epsCplx is not None:
            self.epsCplx = epsCplx
        if numPts is not None:
            self.numPts = numPts
        if deltaPhi is not None:
            self.deltaPhi = deltaPhi
        if maxPrecision is not None:
            self.maxPrecision = maxPrecision

        # initialize list of root calculation sub-tasks
        rootJobs: List[
            Tuple[
                Tuple[float, float],
                Tuple[float, float],
                tQueue,
                Progress,
                TaskID,
            ]
        ] = []
        # initialize result queue for subprocesses to put results into
        resultQueue: tQueue = cast(tQueue, Manager().Queue())

        # generate initial array on rectangle
        x1, x2 = sorted(reRan)
        y1, y2 = sorted(imRan)
        # 'desymmetrize' initial array to improve numerical stability
        x1, x2 = x1 - self.epsCplx.real, x2 + 2 * self.epsCplx.real
        y1, y2 = y1 - 3 * self.epsCplx.imag, y2 + 4 * self.epsCplx.imag
        recNum: Final[int] = 1
        imagPts = np.linspace(y1, y2, num=recNum * CPU_COUNT + 1)
        logger.info(
            f"Calculating roots in [{reRan[0]}, {reRan[1]}]\
             x [{imRan[0]}, {imRan[1]}]"
        )
        MyManager.register("progress", Progress)
        with MyManager() as manager:
            manager = cast(MyManager, manager)
            progress = manager.progress(
                *Progress.get_default_columns()[:],
                SpinnerColumn(),
                "Elapsed:",
                TimeElapsedColumn(),
                transient=False,
                refresh_per_second=3,
                speed_estimate_period=10,
                expand=True,
            )
            total = (x2 - x1) * (y2 - y1)
            task = progress.add_task(
                (f"[magenta]{os.getpid()}: " + "[g]getting roots..."),
                total=total,
            )
            progress.start()
            for i in range(recNum * CPU_COUNT):
                rootJobs.append(
                    (
                        (x1, x2),
                        (imagPts[i], imagPts[i + 1]),
                        resultQueue,
                        progress,
                        task,
                    )
                )

            # calculate roots
            logger.info("Using %d total jobs", len(rootJobs))
            with Pool(processes=CPU_COUNT, initializer=self.initWorker) as p:
                try:
                    p.starmap(self.setupWorker, rootJobs, chunksize=recNum)
                    progress.update(
                        task,
                        description=("[green]finished" + " calculation..."),
                    )
                except KeyboardInterrupt:
                    progress.stop_task(task)
                    progress.update(task, visible=False)
                    progress.refresh()
                    p.terminate()
                    p.join()
            progress.stop()
        # append new roots to previously calculated roots
        newRoots = []
        while not resultQueue.empty():
            newRoots.append(resultQueue.get())
        newErrors = [self.epsCplx for root in newRoots]
        self.addRoots(newRoots, newErrors)


############################
# Newton Root Finder Class #
############################


class NewtonRootFinder(HoloRootFinder):
    r"""
    Class for the calculation of roots of holomorphic functions that combines
    the argument principle with a Newton algorithm.
    """

    def __str__(self) -> str:
        return f"NewtonRootFinder for {self.func.__name__}"

    def calcRootsRecursion(
        self,
        zParts: tRecGrid,
        phiParts: tRecGrid,
        resultQueue: tQueue,
        progress: Progress,
        task: TaskID,
    ) -> None:
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
            # check if desired accuracy is aquired
            if deltaRe < self.epsCplx.real and deltaIm < self.epsCplx.imag:
                newZero = 0.5 * (
                    zParts[1][0].real
                    + zParts[3][0].real
                    + 1j * (zParts[2][0].imag + zParts[0][0].imag)
                )
                zOrder = int(np.round(phi / (2 * np.pi)))
                resultQueue.put((newZero, zOrder))
                progress.update(task, advance=deltaRe * deltaIm)
            elif (phi < FOUR_PI) and (deltaRe < 0.1) and (deltaIm < 0.1):
                xStart = 0.5 * (
                    zParts[1][0].real
                    + zParts[3][0].real
                    + 1j * (zParts[2][0].imag + zParts[0][0].imag)
                )
                try:
                    newZero = newton(
                        self.func,
                        xStart,
                        args=self.funcArgs,
                        maxiter=500,
                        tol=min(self.epsCplx.real, self.epsCplx.imag),
                    )
                    if isinstance(newZero, np.ndarray):
                        for pair in zip(
                            newZero, np.ones_like(newZero, dtype=int)
                        ):
                            resultQueue.put(pair)
                    else:
                        resultQueue.put((newZero, 1))
                except RuntimeError:
                    pass
                finally:
                    progress.update(task, advance=deltaRe * deltaIm)
            else:
                if deltaRe / self.epsCplx.real > deltaIm / self.epsCplx.imag:
                    zPartsNew, phiPartsNew = self.divideVertical(
                        zParts, phiParts, resultQueue
                    )
                    self.calcRootsRecursion(
                        zPartsNew[0],
                        phiPartsNew[0],
                        resultQueue,
                        progress,
                        task,
                    )

                    self.calcRootsRecursion(
                        zPartsNew[1],
                        phiPartsNew[1],
                        resultQueue,
                        progress,
                        task,
                    )

                else:
                    zPartsNew, phiPartsNew = self.divideHorizontal(
                        zParts, phiParts, resultQueue
                    )
                    self.calcRootsRecursion(
                        zPartsNew[0],
                        phiPartsNew[0],
                        resultQueue,
                        progress,
                        task,
                    )

                    self.calcRootsRecursion(
                        zPartsNew[1],
                        phiPartsNew[1],
                        resultQueue,
                        progress,
                        task,
                    )
        else:
            progress.update(task, advance=deltaRe * deltaIm)


if __name__ == "__main__":
    roots: List[complex] = [
        -1.89 - 1.91j,
        -1.9 - 1.2j,
        -1.9 - 0.1j,
        -1.9 + 1.7j,
        -1.9 + 1.8j,
        -1.79 - 1.92j,
        -1.8 - 1.2j,
        -1.8 - 0.1j,
        -1.8 + 1.7j,
        -1.8 + 1.8j,
        0.01 - 1.919j,
        -0.02 - 1.21j,
        0.02 - 0.09j,
        -0.01 + 1.7j,
        0.01 + 1.77j,
        +0.41 - 1.88j,
        +0.6 - 1.2j,
        +1.2 - 0.1j,
        +1.6 + 1.7j,
        +1.99 + 1.8j,
    ]
    param: complex = 1.74152j

    def myfunc1(z: tVec) -> tVec:
        "Evalulate the polynomial with roots `roots` at the point `z`."
        result = np.ones_like(z)
        for power, root in enumerate(np.sort_complex(roots), start=2):
            result *= (z - root) ** (power // 2)
        return result

    def myfunc2(z: tVec) -> tVec:
        "Evaluate the function `sin(z - param * 1j) + param * 1j` at `z`."
        return np.array(np.sin(z - param * 1j) + param * 1j)

    hrf1 = HoloRootFinder(myfunc1, epsCplx=1e-8 * (1 + 1j))
    hrf1.calcRoots((-3.219, 2.958), (-4.269, 2.323))
    print(f"Found {len(hrf1.res)} root(s) of order(s) {hrf1.order}!")
    hrf2 = HoloRootFinder(myfunc2, epsCplx=1e-8 * (1 + 1j))
    hrf2.calcRoots((-5, 5), (-5, 5), numPts=6500)
    print(f"Found {len(hrf2.res)} root(s) of order(s) {hrf2.order}!")

    nrf1 = NewtonRootFinder(myfunc1, epsCplx=1e-8 * (1 + 1j))
    nrf1.calcRoots((-3.219, 2.958), (-4.269, 2.323))
    print(f"Found {len(nrf1.res)} root(s) of order(s) {nrf1.order}!")
    nrf2 = NewtonRootFinder(myfunc2, epsCplx=1e-8 * (1 + 1j))
    nrf2.calcRoots((-5, 5), (-5, 5), numPts=6500)
    print(f"Found {len(nrf2.res)} root(s) of order(s) {nrf2.order}!")

    displayRoots: bool = False
    if displayRoots:
        for zero in hrf1.res:
            print(f"Zero: {zero:.4f}, Func Value: {myfunc1(zero):.4f}")
        print("-" * 50)
        for zero in hrf2.res:
            print(f"Zero: {zero:.4f}, Func Value: {myfunc2(zero):.4f}")
