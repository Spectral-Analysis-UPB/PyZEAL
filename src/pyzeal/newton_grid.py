"""
Module newton_grid of the pyzeal package.
This module contains a simple root finder implementation for holomorphic
functions based on the Newton algorithm.

Authors:\n
- Luca Wasmuth\n
- Philipp Schuette\n
"""

import itertools
import os
import warnings
from typing import Callable, Optional, Set, Tuple, Final
from rich.progress import Progress, TaskID
import numpy as np
import scipy as sp
from numpy import complex128
from numpy.typing import NDArray
from pyzeal_logging.logger import initLogger
from pyzeal_types.root_types import tQueue

from pyzeal.finder_interface import RootFinder

newton_logger = initLogger("newton_grid")

CPU_COUNT: Final[int] = os.cpu_count() or 1


class NewtonGridRootFinder(RootFinder):
    r"""
    Root finder based on the Newton algorithm, with starting points
    on an evenly spaced grid.
    """

    __slots__ = ("f", "df", "_roots", "numSamplePoints")

    def __init__(
        self,
        f: Callable[[complex], complex],
        df: Optional[Callable[[complex], complex]],
        numSamplePoints: int = 50,
    ) -> None:
        r"""
        Initialize a root finder which searches for roots of a given function
        `f` using the Newton algorithm with starting points on an evenly spaced
        grid.

        :param f: differentiable function
        :type f: Callable[[complex], complex]
        :param df: derivative of f
        :type df: Callable[[complex], complex]
        """
        super().__init__()
        self.f = f
        self.df = df
        self.numSamplePoints = numSamplePoints
        self._roots: Optional[Set[Tuple[complex, int]]] = None
        if hasattr(f, "__name__"):
            self.logger.info(
                "Initialized Newton-Grid-Rootfinder for %s", f.__name__
            )
        else:
            self.logger.info(
                "Initialized Newton-Grid-Rootfinder for unnamed function"
            )

    def getRoots(self) -> NDArray[complex128]:
        if self._roots is None:
            raise ValueError(
                "Must calculate roots first before retrieving them!"
            )
        return np.array(list(self._roots))

    def runRootJobs(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        resultQueue: tQueue,
        progress: Progress,
        task: TaskID,
        precision: Tuple[int, int],
    ) -> None:
        r"""
        Internal function for the newton-grid rootfinder. Runs the
        newton-method starting from each point in points with a given
        precision.
        :param points: List of starting points
        :param precision: Precision in real and imaginary parts
        :return: A set of roots
        """
        self._roots = set()
        rePoints = np.linspace(
            reRan[0], reRan[1], self.numSamplePoints, dtype=complex128
        )
        imPoints = np.linspace(
            imRan[0],
            imRan[1],
            int(self.numSamplePoints / (CPU_COUNT + 1)),
            dtype=complex128,
        )
        self.logger.debug(
            "Running job for [%f, %f] x [%f, %f]",
            reRan[0],
            reRan[1],
            imRan[0],
            imRan[1],
        )
        points = [
            x + y * 1j for (x, y) in itertools.product(rePoints, imPoints)
        ]
        roots = set()
        warnings.filterwarnings("ignore", ".*some failed to converge")
        try:
            result: NDArray = sp.optimize.newton(self.f, points, self.df)
            for z in result:
                roots.add(
                    round(z.real, precision[0])
                    + round(z.imag, precision[1]) * 1j
                )
            progress.update(
                task, advance=((reRan[1] - reRan[0]) * (imRan[1] - imRan[0]))
            )
        except RuntimeError:
            pass

        def _inside(z: complex) -> bool:
            "Filter predicate to determine points inside the search area."
            u, v = z.real, z.imag
            return reRan[0] <= u <= reRan[1] and imRan[0] <= v <= imRan[1]

        for r in roots:
            if _inside(r):
                resultQueue.put((r, 0))

    def addRoot(self, newRoot: Optional[Tuple[complex, int]]) -> None:
        if self._roots is None:
            self._roots = set()
        if newRoot is None:
            return

        def _closeToZero(z: complex) -> bool:
            r"""
            Filter predicate to ensure that the results are actually
            close to zero, as scipy sometimes returns incorrect results.
            """
            # 0.1 is an arbitrary constant that works for all tests
            return abs(self.f(z)) < 0.1

        if _closeToZero(newRoot[0]):
            self.logger.debug(
                "Found zero at %f + %fi", newRoot[0].real, newRoot[0].imag
            )
            self._roots.add(newRoot)

    @property
    def logger(self):
        return newton_logger
