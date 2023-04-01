"""
Protocol RootContainer from the package pyzeal_utils.
This module defines an interface to container types which are meant to hold
root data. The underlying strategy used in cases where e.g. almost identical
roots are added or the precision of roots is changed between add operations is
up to the concrete container implementation (and transparent to the user).
Additional checks could also be implemented in subclasses, e.g. checking if a
root is contained in a certain region.

Authors:\n
- Philipp Schuette\n
"""

from typing import Protocol, runtime_checkable

import numpy as np
from numpy.typing import NDArray

from pyzeal.pyzeal_logging.loggable import Loggable
from pyzeal.pyzeal_types.root_types import tRoot, tVec
from pyzeal.utils.filter_context import FilterContext, tRootFilter


@runtime_checkable
class RootContainer(Loggable, Protocol):
    "Structural interface for container classes meant to hold root data."

    def addRoot(self, root: tRoot, context: FilterContext) -> None:
        """
        Add a root to the container.

        :param root: the root to be added to the container
        :param context: the number of valid decimal places of `root`
        """
        ...

    def getRoots(self) -> tVec:
        """
        Returns all roots currently held in this container as a vector.

        :return: a vector of complex roots
        """
        ...

    def getRootOrders(self) -> NDArray[np.int32]:
        """
        Returns the orders of all roots currently held in this container as a
        vector which is parallel to the vector returned by `getRoots`.

        :return: a vector of integer root orders (multiplicities)
        """
        ...

    def removeRoot(self, root: tRoot) -> bool:
        """
        Remove a root from the container and indicate whether or not a removal
        actually happened via the return value.

        :param root: the root to be removed from the container
        :return: a boolean flag indicating if a removal happened
        """
        ...

    def clear(self) -> None:
        "Clear all data from the container."
        ...

    def registerFilter(self, filterPredicate: tRootFilter, key: str) -> None:
        """
        Add a new filter predicate to this container instance. The filtering
        applies to all roots added after the filter is registered. To guarantee
        a consistent set of roots any implementation should clear its internal
        root buffer before/after registering a filter.

        :param filterPredicate: the predicate used to filter roots
        :param key: a (unique) key under which the filter is registered
        """
        ...

    def unregisterFilter(self, key: str) -> None:
        """
        Remove a previously registered filter by key.

        :param key: key value for the filter to remove
        """
        ...
