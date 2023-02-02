"""
TODO

Authors:\n
- Philipp Schuette\n
"""

from typing import Protocol, Tuple

from pyzeal_utils.root_context import RootContext


class ArgumentEstimator(Protocol):
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
        ...
