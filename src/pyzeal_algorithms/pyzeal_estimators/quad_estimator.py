"""
TODO

Authors:\n
- Philipp Schuette
"""

from typing import Final

import numpy as np
from scipy.integrate import romb

from pyzeal_types.root_types import tVec
from pyzeal_utils.root_context import RootContext

from .argument_estimator import ArgumentEstimator
from .estimator_cache import EstimatorCache

####################
# Global Constants #
####################

EXP_SAMPLE_POINTS: Final[int] = 10  # number of sample points for integration


class QuadratureEstimator(ArgumentEstimator):
    """
    TODO
    """

    __slots__ = ("_cache",)

    def __init__(self, cache: EstimatorCache) -> None:
        """
        TODO
        """
        self._cache = cache

    def calcMomentAlongLine(
        self,
        order: int,
        zStart: complex,
        zEnd: complex,
        context: RootContext,
    ) -> float:
        """
        TODO
        """

        def _logDeriv(x: tVec) -> tVec:
            "Logarithmic derivative of the target function. TODO: zeros!"
            try:
                return context.df(x) * x**order / context.f(x)  # type: ignore
            except TypeError as ex:
                raise ValueError("derivative required for quadrature!") from ex

        funcValues = _logDeriv(
            np.linspace(zStart, zEnd, 2**EXP_SAMPLE_POINTS + 1)
        )
        distance = abs(zEnd - zStart)

        realResult = romb(
            np.real(funcValues), distance / (2**EXP_SAMPLE_POINTS)
        )
        imagResult = romb(
            np.imag(funcValues), distance / (2**EXP_SAMPLE_POINTS)
        )
        # the result is expected to be real (after devision by 1j)
        return complex(
            (zEnd - zStart) * (-1j * realResult + imagResult) / distance
        ).real

    @property
    def cache(self) -> EstimatorCache:
        """
        TODO
        """
        return self._cache
