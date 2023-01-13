"""
Implementation RoundingContainer of the RootContainer protocol from the
pyzeal_utils package.
The concrete container class implemented here automatically rounds added roots
to a fixed number of decimal places.

Authors:\n
- Philipp Schuette\n
"""

from typing import Dict, Set, Tuple

import numpy as np
from numpy.typing import NDArray
from pyzeal_types.root_types import tRoot, tVec

from pyzeal_utils.filter_context import FilterContext
from pyzeal_utils.root_container import RootContainer, tRootFilter


class RoundingContainer(RootContainer):
    """
    This simple container implementation rounds every added root to a given
    number of decimal places and simple ignores any attempts to add additional
    roots which coincide with a previously added root after rounding. The
    multiplicity is not taken into account when comparing old and new roots.
    Changing the desired accuracy automatically removes all calculated roots
    to preserve consistency.
    """

    __slots__ = ("precision", "rootSet", "filters")

    def __init__(self, precision: Tuple[int, int]) -> None:
        """
        Initialize a rounding RootContainer with a given accuracy.

        :param precision: expected accuracy of roots to be added
        :type precision: Tuple[int, int]
        """
        self.precision = precision
        self.rootSet: Set[tRoot] = set()
        self.filters: Dict[str, tRootFilter] = {}
        self.logger.info("initialized a rounding root container")

    def addRoot(self, root: tRoot, context: FilterContext) -> None:
        """
        Add a new root with given accuracy to the container. If the accuracy
        differs from the accuracy of roots already added then all previous
        roots are removed.

        :param root: the root to be added to the container
        :type root: tRoot
        :param context: the context of the new root, required for filtering
        :type context: FilterContext
        """
        for filterPredicate in self.filters.values():
            if not filterPredicate(root, context):
                self.logger.debug(
                    "root %f+%fi was rejected by container filter!",
                    root[0].real,
                    root[0].imag,
                )
                return
        if context.precision != self.precision:
            self.clear()
            self.logger.debug(
                "new accuracy detected - rounding container cleared!"
            )
            self.precision = context.precision
        self.logger.debug(
            "attempting to add new root %f+%fi to rounding container!",
            root[0].real,
            root[0].imag,
        )
        self.rootSet.add(RoundingContainer.roundRoot(root, self.precision))

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
                RoundingContainer.roundRoot(root, self.precision)
            )
            self.logger.debug(
                "removed root %f+%fi from rounding container!",
                root[0].real,
                root[0].imag,
            )
            return True
        except KeyError:
            self.logger.debug(
                "failed to remove root %f+%fi from rounding container!",
                root[0].real,
                root[0].imag,
            )
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
    def roundRoot(root: tRoot, precision: Tuple[int, int]) -> tRoot:
        """
        Round a given root to a given number of decimal places.

        :param root: a root to be rounded
        :type root: tRoot
        :param precision: the number of decimal places to round to
        :type precision: int
        :return: the rounded root (multiplicity stays constant)
        :rtype: tRoot
        """
        x, y = root[0].real, root[0].imag
        return complex(round(x, precision[0]), round(y, precision[1])), root[1]

    def registerFilter(self, filterPredicate: tRootFilter, key: str) -> None:
        """
        TODO
        """
        self.filters[key] = filterPredicate

    def unregisterFilter(self, key: str) -> None:
        """
        TODO
        """
        try:
            self.filters.pop(key)
            self.logger.debug("removed filter %s", key)
        except KeyError:
            self.logger.info("tried to remove non-existent filter %s!", key)
