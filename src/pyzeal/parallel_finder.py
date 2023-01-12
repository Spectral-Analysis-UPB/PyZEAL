"""
Class ParallelRootFinder from the package pyzeal.
This module defines an implementation of the main root finding API as defined
by the `RootFinderInterface` protocol. It differs from `RootFinder` in the fact
that it devides the search region into sub-regions and delegates these to a
number of appropriate algorithms working in parallel. The parallelism is
realized by using the standard library `multiprocessing` module.

Authors:\n
- Philipp Schuette\n
"""

from typing import Tuple
from numpy import int32
from numpy.typing import NDArray

from pyzeal_types.root_types import tVec
from pyzeal_logging.loggable import Loggable
from .finder_interface import RootFinderInterface


class ParallelRootFinder(RootFinderInterface, Loggable):
    """
    Parallel (multiprocessing) implementation of the main root finding API.
    """

    def calculateRoots(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        precision: Tuple[int, int],
    ) -> None:
        """
        Entry point for starting a parallel root finding calculation in the
        rectangle `reRan x imRan` up to a number of `precision` significant
        digits in real and imaginary part.

        :param reRan: horizontal extend of the complex region to search in
        :type reRan: Tuple[int, int]
        :param imRan: vertical extend of the complex region to search in
        :type imRan: Tuple[int, int]
        :param precision: accuracy of the search in real and imaginary parts
        :type precision: Tuple[int, int]
        """
        ...

    @property
    def roots(self) -> tVec:
        """
        Return the roots calculated with this root finder through previous
        calls to `calculateRoots()`.

        :return: the set of roots calculated by this finder
        :rtype: NDArray[np.complex128]
        """
        ...

    @property
    def orders(self) -> NDArray[int32]:
        """
        Return the orders of the roots calculated with this finder. The output
        is parallel to the return value of the `roots` property.

        :return: the orders of the roots calculated by this finder
        :rtype: NDArray[np.int32]
        """
        ...
