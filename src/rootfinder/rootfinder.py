"""
Module rootfinder of the rootfinder package.
This module contains the base interface for all rootfinder implementations.

Authors:\n
- Philipp Schuette\n
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple

from numpy import complex128
from numpy.typing import NDArray


class RootFinder(ABC):
    r"""
    Base interface for class implementations of root finding algorithms.
    """
    @abstractmethod
    def calcRoots(self, reRan: Tuple[float, float], imRan: Tuple[float, float],
                  epsCplx: Optional[complex]) -> None:
        r"""
        Calculate roots in the rectangle `reRan x imRan` up to accurancy
        `epsCplx` in real and imaginary part.

        :param reRan: boundaries of calculation rectangle in real direction
        :type reRan: Tuple[float, float]
        :param imRan: boundaries of calculation rectangle in imaginary
            direction
        :type imRan: Tuple[float, float]
        :param epsCplx: accuracy of root calculation in real and imaginary
            directions, re-uses last value if `None`
        :type epsCplx: Optional[complex]
        """

    @abstractmethod
    def getRoots(self) -> NDArray[complex128]:
        r"""
        Return roots previously calculated using `.calcRoots()` as an ndarray.

        :return: array of complex roots calculated previously
        :rtype: numpy.ndarray[complex128]
        """
