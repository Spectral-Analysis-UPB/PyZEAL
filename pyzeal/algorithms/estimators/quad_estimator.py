"""
This module provides an argument estimator based on numerical integration
using Romberg quadrature.

Authors:\n
- Philipp Schuette
"""

from typing import Final

import numpy as np
from scipy.integrate import romb  # type: ignore

from pyzeal.algorithms.estimators.argument_estimator import ArgumentEstimator
from pyzeal.algorithms.estimators.estimator_cache import EstimatorCache
from pyzeal.pyzeal_types.root_types import tVec
from pyzeal.utils.root_context import RootContext

####################
# Global Constants #
####################

EXP_SAMPLE_POINTS: Final[int] = 12  # number of sample points for integration


class QuadratureEstimator(ArgumentEstimator):
    """
    This class implements an argument estimator using numerical quadrature
    to integrate the logarithmic derivative.
    """

    __slots__ = ("_cache",)

    def __init__(self, *, cache: EstimatorCache) -> None:
        """
        Initialize a `QuadratureEstimator`.

        :param cache: Cache to store intermediate values in.
        """
        self._cache = cache

    def calcMomentAlongLine(
        self,
        order: int,
        zStart: complex,
        zEnd: complex,
        context: RootContext,
    ) -> complex:
        """
        Calculate the `order`-th moment of the logarithmic derivative along
        the line given by `zStart` and `zEnd`.

        :param order: Moment to compute
        :param zStart: Start z-value
        :param zEnd: End z-value
        :param context: `RootContext` containing the necessary information
        :raises ValueError: An error is raised when no derivative is supplied,
            as the `QuadratureEstimator` does not support derivative-free
            argument estimation.
        :return: The moment as calculated along the given line.
        """
        if context.df is None:
            raise ValueError(
                "derivative required for quadrature-based argument estimation!"
            )

        # TODO: caching of function evaluations!
        # TODO: adjust line if zero on line found!
        zArr = np.linspace(zStart, zEnd, 2**EXP_SAMPLE_POINTS + 1)
        funcValues: tVec = context.df(zArr) * zArr**order / context.f(zArr)
        distance = abs(zEnd - zStart)

        realResult = romb(
            np.real(funcValues), distance / (2**EXP_SAMPLE_POINTS)
        )
        imagResult = romb(
            np.imag(funcValues), distance / (2**EXP_SAMPLE_POINTS)
        )
        # result (divided by 1j) is only necessarily real if order=0!
        return complex(
            (zEnd - zStart) * (-1j * realResult + imagResult) / distance
        )

    @property
    def cache(self) -> EstimatorCache:
        """
        Returns the cache used by this argument estimator.

        :return: Cache used by this argument estimator.
        """
        return self._cache
