"""
TODO

Authors:\n
- Philipp Schuette
"""

from typing import Tuple

from pyzeal_utils.root_context import RootContext

from .argument_estimator import ArgumentEstimator


class QuadratureEstimator(ArgumentEstimator):
    """
    TODO
    """

    def calcMoment(
        self,
        order: int,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        context: RootContext,
    ) -> float:
        """
        TODO
        """
        raise NotImplementedError()
