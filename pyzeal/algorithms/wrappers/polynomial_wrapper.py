"""
TODO

Authors:\n
- Philipp Schuette\n
"""

from abc import ABC, abstractmethod
from typing import List, Tuple

from numpy import int32
from numpy.typing import NDArray

from pyzeal.pyzeal_logging.loggable import Loggable
from pyzeal.pyzeal_types.root_types import tVec


class PolynomialWrapper(ABC, Loggable):
    """
    Abstract base class for a simple wrapper of polynomials with complex
    coefficients.

    In particular it exposes an abstract method to find roots of a polynomial.
    To implement alternative methods (like non-classical approaches based e.g.
    on neural networks) just implement this interface.
    """

    __slots__ = ("_coefficients",)

    def __init__(self, coefficients: List[complex]) -> None:
        """
        Initialize a polynomial wrapper from a given set of coefficients. The
        resulting instance will represent the polynomial
        :math:`coeffcients[0] + coefficients[1] * z + ...`.

        :param coefficients: the coefficients of the polynomial
        """
        self._coefficients = coefficients

    @abstractmethod
    def getRootsWithOrders(
        self, precision: Tuple[int, int]
    ) -> Tuple[tVec, NDArray[int32]]:
        """
        Return the distinct roots of the polynomial together with their orders.

        :param precision: proximity where roots are considered equal
        :returns: parallel arrays of roots and orders
        """
