"""
Implementation PlainContainer of the RootContainer protocol from the
pyzeal_utils package.
The concrete container class implemented here simply adds roots to an internal
buffer without any further action. Its main use is the collection of potential
roots in subprocesses during parallel calculations.

Authors:\n
- Philipp Schuette\n
"""

from multiprocessing import Manager
from typing import List, Optional, cast

import numpy as np
from numpy.typing import NDArray

from pyzeal.pyzeal_types.parallel_types import tQueue
from pyzeal.pyzeal_types.root_types import tRoot, tVec
from pyzeal.utils.containers.root_container import RootContainer
from pyzeal.utils.filter_context import FilterContext, tRootFilter


class PlainContainer(RootContainer):
    """
    Minimal container implementation. Simply adds roots to an internal buffer
    of type `tQueue` without any further action.

    This class is mainly designed for application with a `queue` instance
    obtained from a `multiprocessing.Manager`. With this particular choice of
    root buffer it can serve as shared memory for several distinct processes
    each running their own instance of a `FinderAlgorithm`.
    """

    __slots__ = ("rootBuffer", "_roots")

    def __init__(self, queue: Optional[tQueue]) -> None:
        """
        Initialize a new PlainContainer.

        :param queue: the internal buffer used for root storage
        """
        self.rootBuffer = cast(tQueue, queue or Manager().Queue())
        self._roots: List[tRoot] = []
        self.logger.info("initialized a new plain root container")

    def addRoot(self, root: tRoot, context: FilterContext) -> None:
        """
        Add a new root to the internal buffer, ignoring the filter context.

        :param root: the root to be added to the container
        :param context: the context of the new root, ignored
        """
        self.logger.debug(
            "adding new root %f + %fi to plain container!",
            root[0].real,
            root[0].imag,
        )
        self.rootBuffer.put(root)

    def removeRoot(self, root: tRoot) -> bool:
        """
        Roots cannot be removed from a plain container.

        :param root: the root to be removed from the container
        :return: always returns False
        """
        return False

    def getRoots(self) -> tVec:
        """
        Returns all roots currently held in this container as a vector.

        :return: a vector of complex roots
        """
        self._transferRootBuffer()
        return np.array([root for root, _ in self._roots], dtype=np.complex128)

    def getRootOrders(self) -> NDArray[np.int32]:
        """
        Returns the orders of all roots currently held in this container as a
        vector which is parallel to the vector returned by `getRoots`.

        :return: a vector of integer root orders (multiplicities)
        """
        self._transferRootBuffer()
        return np.array([order for _, order in self._roots], dtype=np.int32)

    def _transferRootBuffer(self) -> None:
        """
        Transfer roots from the root buffer to an internal list of roots.
        """
        while not self.rootBuffer.empty():
            self._roots.append(self.rootBuffer.get())

    def clear(self) -> None:
        "Plain containers cannot be cleared."
        raise NotImplementedError("cannot clear plain containers!")

    def registerFilter(self, filterPredicate: tRootFilter, key: str) -> None:
        """
        Cannot register filters with an instance of `PlainContainer`.

        :param filterPredicate: New filter to register
        :param key: A key to identify this filter
        """
        raise NotImplementedError("plain containers do not support filtering!")

    def unregisterFilter(self, key: str) -> None:
        """
        Cannot unregister filters with an instance of `PlainContainer`.

        :param key: Filter key
        """
        raise NotImplementedError("plain containers do not support filtering!")
