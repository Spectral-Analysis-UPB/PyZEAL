"""
Module newton_grid of the rootfinder package.
This module contains a simple root finder implementation for holomorphic
functions based on the Newton algorithm.

Authors:\n
- Luca Wasmuth\n
- Philipp Schuette\n
"""

from pathos.pools import ProcessPool
from typing import Callable, Optional, Set, Tuple
from numpy import complex128
from numpy.typing import NDArray
import numpy as np
import scipy as sp
import itertools

from rootfinder.finder_interface import RootFinder


class NewtonGridRootFinder(RootFinder):
    r"""
    Root finder based on the Newton algorithm, with starting points
    on an evenly spaced grid.
    """

    __slots__ = ("f", "df", "_roots", "numSamplePoints")

    def __init__(
        self,
        f: Callable[[float], float],
        df: Callable[[float], float],
        numSamplePoints: int = 50,
    ) -> None:
        r"""
        Initialize a root finder which searches for roots of a given function
        `f` using the Newton algorithm with starting points on an evenly spaced
        grid.

        :param f: differentiable function
        :type f: Callable[[float], float]
        :param df: derivative of f
        :type df: Callable[[float], float]
        """
        super().__init__()
        self.f: Callable[[float], float] = f
        self.df: Callable[[float], float] = df
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
        roots: Set[complex] = set()

        def _runNewton(start: Tuple[float, float]) -> Optional[complex]:
            try:
                result = sp.optimize.newton(
                    self.f, start[0] + start[1] * 1j, self.df
                )
                return (
                    round(result.real, precision[0])
                    + round(result.imag, precision[1]) * 1j
                )
            except RuntimeError:
                return None

        pool = ProcessPool()
        result = pool.map(_runNewton, itertools.product(rePoints, imPoints))
        for res in result:
            if res is not None:
                roots.add(res)

        def _inside(z: complex) -> bool:
            "Filter predicate to determine points inside the search area."
            u, v = z.real, z.imag
            return reRan[0] <= u <= reRan[1] and imRan[0] <= v <= imRan[1]

        def _closeToZero(z: complex) -> bool:
            r"""Filter predicate to ensure that the results are actually
            close to zero, as scipy sometimes returns incorrect results"""
            # 0.1 is an arbitrary constant that works for all tests
            return np.abs(self.f(z)) < 0.1

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
