"""
Implementation RoundingContainer of the RootContainer protocol from the
pyzeal_utils package.
The concrete container class implemented here automatically rounds added roots
to a fixed number of decimal places.

Authors:\n
- Philipp Schuette\n
"""

from typing import Optional, Set

import numpy as np
from numpy.typing import NDArray

from pyzeal_utils.root_container import RootContainer
from pyzeal_types.root_types import tRoot, tVec


class RoundingContainer(RootContainer):
    """
    This simple container implementation rounds every added root to a given
    number of decimal places and simple ignores any attempts to add additional
    roots which coincide with a previously added root after rounding. The
    multiplicity is not taken into account when comparing old and new roots.
    Changing the desired accuracy automatically removes all calculated roots
    to preserve consistency.
    """

    __slots__ = ("accuracy", "rootSet", )

    def __init__(self, accuracy: int) -> None:
        """
        Initialize a rounding RootContainer with a given accuracy.

        :param accuracy: expected accuracy of roots to be added
        :type accuracy: int
        """
        self.accuracy = accuracy
        self.rootSet: Set[tRoot] = set()

    def addRoot(self, root: tRoot, accuracy: Optional[int] = None) -> None:
        """
        Add a new root with given accuracy to the container. If the accuracy
        differs from the accuracy of roots already added then all previous
        roots are removed.

        :param root: the root to be added to the container
        :type root: tRoot
        :param accuracy: the number of valid decimal places of `root`
        :type accuracy: int
        """
        if accuracy is not None and accuracy != self.accuracy:
            self.clear()
            self.accuracy = accuracy
        self.rootSet.add(RoundingContainer.roundRoot(root, self.accuracy))

    def removeRoot(self, root: tRoot) -> bool:
        """
        Remove a given root from the container. Return value indicates success.

        :param root: the root to be removed from the container
        :type root: tRoot
        :return: a boolean flag indicating if a removal happened
        :rtype: bool
        """
        try:
            self.rootSet.remove(
                RoundingContainer.roundRoot(root, self.accuracy)
            )
            return True
        except KeyError:
            return False

    def getRoots(self) -> tVec:
        """
        Returns all roots currently held in this container as a vector.

        :return: a vector of complex roots
        :rtype: NDArray[complex128]
        """
        result = np.empty((len(self.rootSet)), dtype=np.complex128)
        for i, root in enumerate(self.rootSet):
            result[i] = root[0]
        return result

    def getRootOrders(self) -> NDArray[np.int32]:
        """
        Returns the orders of all roots currently held in this container as a
        vector which is parallel to the vector returned by `getRoots`.

        :return: a vector of integer root orders (multiplicities)
        :rtype: NDArray[int32]
        """
        result = np.empty((len(self.rootSet)), dtype=np.int32)
        for i, root in enumerate(self.rootSet):
            result[i] = root[1]
        return result

    def clear(self) -> None:
        "Clear the container by removing all roots."
        self.rootSet.clear()

    @staticmethod
    def roundRoot(root: tRoot, accuracy: int) -> tRoot:
        """
        Round a given root to a given number of decimal places.

        :param root: a root to be rounded
        :type root: tRoot
        :param accuracy: the number of decimal places to round to
        :type accuracy: int
        :return: the rounded root (multiplicity stays constant)
        :rtype: tRoot
        """
        x, y = root[0].real, root[0].imag
        return complex(round(x, accuracy), round(y, accuracy)), root[1]
