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
from multiprocessing import Pool
from typing import Callable, Optional, Set, Tuple
from numpy import complex128
from numpy.typing import NDArray
import numpy as np
import scipy as sp

from pyzeal.finder_interface import RootFinder


class NewtonGridRootFinder(RootFinder):
    r"""
    Root finder based on the Newton algorithm, with starting points
    on an evenly spaced grid.
    """

    __slots__ = ("f", "df", "_roots", "numSamplePoints")

    def __init__(
        self,
        f: Callable[[complex], complex],
        df: Callable[[complex], complex],
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
        roots: Set[complex] = set()
        if self.numSamplePoints > 50:
            batches = np.array_split(points, os.cpu_count())
            with Pool(os.cpu_count()) as p:
                rootList = p.starmap(
                    self.runNewton, [(batch, precision) for batch in batches]
                )
            roots = {r for rootset in rootList for r in rootset}
        else:
            roots = self.runNewton(points, precision)

        def _inside(z: complex) -> bool:
            "Filter predicate to determine points inside the search area."
            u, v = z.real, z.imag
            return reRan[0] <= u <= reRan[1] and imRan[0] <= v <= imRan[1]

        def _closeToZero(z: complex) -> bool:
            r"""Filter predicate to ensure that the results are actually
            close to zero, as scipy sometimes returns incorrect results"""
            # 0.1 is an arbitrary constant that works for all tests
            return abs(self.f(z)) < 0.1

        self._roots = np.array(
            [root for root in roots if _inside(root) and _closeToZero(root)],
            dtype=complex128,
        )

    def getRoots(self) -> NDArray[complex128]:
        if self._roots is None:
            raise ValueError(
                "Must calculate roots first before retrieving them!"
            )
        return self._roots

    def runNewton(self, points, precision):
        r"""
        Internal function for the newton-grid rootfinder. Runs the
        newton-method starting from each point in points with a given
        precision.
        :param points: List of starting points
        :param precision: Precision in real and imaginary parts
        :return: A set of roots
        """
        roots: Set[complex] = set()
        try:
            result = sp.optimize.newton(self.f, points, self.df)
            for r in result:
                roots.add(
                    round(r.real, precision[0])
                    + round(r.imag, precision[1]) * 1j
                )
        except RuntimeError:
            pass
        return roots
