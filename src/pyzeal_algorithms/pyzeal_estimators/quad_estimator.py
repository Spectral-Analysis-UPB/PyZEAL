"""
TODO

Authors:\n
- Philipp Schuette
"""

from typing import Literal, Union

import numpy as np
from scipy.integrate import quad

from pyzeal_types.root_types import tVec
from pyzeal_utils.root_context import RootContext

from .argument_estimator import ArgumentEstimator
from .estimator_cache import EstimatorCache


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
        pos: Union[Literal["horizontal"], Literal["vertical"]],
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

        realResult = quad(
            lambda t: np.real(_logDeriv(zStart + t * (zEnd - zStart))), 0, 1
        )
        imagResult = quad(
            lambda t: np.imag(_logDeriv(zStart + t * (zEnd - zStart))), 0, 1
        )
        # the result is expected to be real (after devision by 1j)
        return complex(
            (zEnd - zStart) * (-1j * realResult[0] + imagResult[0])
        ).real

    @property
    def cache(self) -> EstimatorCache:
        """
        TODO
        """
        return self._cache
