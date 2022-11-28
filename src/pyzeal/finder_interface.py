"""
Module rootfinder of the pyzeal package.
This module contains the base interface for all rootfinder implementations.

Authors:\n
- Philipp Schuette\n
"""

import signal
from abc import ABC, abstractmethod
from typing import Tuple

from numpy import complex128
from numpy.typing import NDArray


class RootFinder(ABC):
    r"""
    Base interface for class implementations of root finding algorithms.
    """

    @abstractmethod
    def calcRoots(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        precision: Tuple[int, int],
    ) -> None:
        r"""
        Calculate roots in the rectangle `reRan x imRan` up to accurancy
        `precision` in real and imaginary part.

        :param reRan: boundaries of calculation rectangle in real direction
        :type reRan: Tuple[float, float]
        :param imRan: boundaries of calculation rectangle in imaginary
            direction
        :type imRan: Tuple[float, float]
        :param precision: accuracy of root calculation in real and imaginary
            directions in terms of decimal places
        :type precision: Tuple[int, int]
        """

    @abstractmethod
    def getRoots(self) -> NDArray[complex128]:
        r"""
        Return roots previously calculated using `.calcRoots()` as an ndarray.

        :return: array of complex roots calculated previously
        :rtype: numpy.ndarray[complex128]
        """

    
    def initWorker(self) -> None:
        r"""
        Initialization function for workers executing `self.setupWorker`. This
        step is necessary to guarantee correct processing of user signals
        `ctrl+c`.
        """
        signal.signal(signal.SIGINT, signal.SIG_IGN)