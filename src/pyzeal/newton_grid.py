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
from multiprocessing import Pool, Manager
from typing import Callable, Optional, Set, Tuple, cast

import numpy as np
import scipy as sp
from numpy import complex128
from numpy.typing import NDArray
from pyzeal_logging.logger import initLogger

from pyzeal.finder_interface import RootFinder

logger = initLogger("newton_grid")


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
        self._roots: Optional[NDArray[complex128]] = None
        if hasattr(f, "__name__"):
            logger.info("Initialized Newton-Grid-Rootfiner for %s", f.__name__)
        else:
            logger.info(
                "Initialized Newton-Grid-Rootfinder for unnamed function"
            )

    def calcRoots(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        precision: Tuple[int, int] = (6, 6),
    ) -> None:
        rePoints = np.linspace(
            reRan[0], reRan[1], self.numSamplePoints, dtype=complex128
        )
        imPoints = np.linspace(
            imRan[0], imRan[1], self.numSamplePoints, dtype=complex128
        )
        points = [
            x + y * 1j for (x, y) in itertools.product(rePoints, imPoints)
        ]
        print("Finished calculating starting points")
        roots: Set[complex] = set()
        logger.info(
            "Calculating roots in [%f.3, %f.3] x [%f.3, %f.3]\
                 with %d total starting points",
            reRan[0],
            reRan[1],
            imRan[0],
            imRan[1],
            self.numSamplePoints**2,
        )
        rootQueue = Manager().Queue()
        if self.numSamplePoints > 50:
            logger.debug(
                "As numSamplePoints is %d, roots\
                 are calculated using %d processes",
                self.numSamplePoints,
                os.cpu_count(),
            )
            cpuCount: int = cast(
                int, os.cpu_count() if os.cpu_count() is not None else 1
            )
            batches = np.array_split(points, cpuCount * 10)
            with Pool(cpuCount, initializer=self.initWorker) as p:
                try:
                    p.starmap(
                        self.runNewton, [(batch, precision, rootQueue) for batch in batches]
                    )
                except KeyboardInterrupt:
                    p.terminate()
                    p.join()
        else:
            logger.debug("Running using a single process")
            self.runNewton(points, precision, rootQueue)
        while not rootQueue.empty():
            roots.add(rootQueue.get())

        def _inside(z: complex) -> bool:
            "Filter predicate to determine points inside the search area."
            u, v = z.real, z.imag
            return reRan[0] <= u <= reRan[1] and imRan[0] <= v <= imRan[1]

        def _closeToZero(z: complex) -> bool:
            r"""
            Filter predicate to ensure that the results are actually
            close to zero, as scipy sometimes returns incorrect results.
            """
            # 0.1 is an arbitrary constant that works for all tests
            return abs(self.f(z)) < 0.1

        self._roots = np.array(
            [root for root in roots if _inside(root) and _closeToZero(root)],
            dtype=complex128,
        )
        logger.info("Calculated %d roots", len(self._roots))

    def getRoots(self) -> NDArray[complex128]:
        if self._roots is None:
            raise ValueError(
                "Must calculate roots first before retrieving them!"
            )
        return self._roots

    def runNewton(self, points, precision, rootList):
        r"""
        Internal function for the newton-grid rootfinder. Runs the
        newton-method starting from each point in points with a given
        precision.

        :param points: List of starting points
        :param precision: Precision in real and imaginary parts
        :return: A set of roots
        """
        roots: Set[complex] = set()
        warnings.filterwarnings("ignore", ".*some failed to converge")
        try:
            result = sp.optimize.newton(self.f, points, self.df)
            for r in result:
                roots.add(
                    round(r.real, precision[0])
                    + round(r.imag, precision[1]) * 1j
                )
        except RuntimeError:
            pass
        for r in roots:
            rootList.put(r)
