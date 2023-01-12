"""
Module finder_interface of the package pyzeal.
This module contains the base interface for all rootfinder implementations. Its
methods provide the main root finding API for end users. Internally its
implementations should build up an appropriate root finding context and then
employ a `FinderAlgorithm` to calculate the actual roots. Internal book keeping
is facilitated by the implementations of `RootContainer`.

Authors:\n
- Philipp Schuette\n
"""

from typing import Protocol, Tuple
from numpy import int32
from numpy.typing import NDArray

from pyzeal_types.root_types import tVec


class RootFinderInterface(Protocol):
    """
    Interface for the main root finding API. After initializing a root finder
    for a given concrete problem methods for calculating roots as well as
    properties for retrieving roots and their orders are available.
    """

    def calculateRoots(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        precision: Tuple[int, int],
    ) -> None:
        """
        Entry point for starting a root finding calculation in the rectangle
        `reRan x imRan` up to a number of `precision` significant digits in
        real and imaginary part.

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
