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
from typing import cast, List

import numpy as np
from numpy.typing import NDArray
from pyzeal_types.root_types import tRoot, tVec
from pyzeal_types.parallel_types import tQueue

from pyzeal_utils.filter_context import FilterContext
from pyzeal_utils.root_container import RootContainer, tRootFilter


class PlainContainer(RootContainer):
    """
    TODO
    """

    __slots__ = ("rootBuffer", )

    def __init__(self) -> None:
        """
        Initialize a new PlainContainer.
        """
        self.rootBuffer = cast(tQueue, Manager().Queue())
        self.logger.info("initialized a plain root container")

    def addRoot(self, root: tRoot, context: FilterContext) -> None:
        """
        Add a new root to the internal buffer, ignoring the filter context.

        :param root: the root to be added to the container
        :type root: tRoot
        :param context: the context of the new root, ignored
        :type context: FilterContext
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
        :type root: tRoot
        :return: always returns False
        :rtype: bool
        """
        return False

    def getRoots(self) -> tVec:
        """
        Returns all roots currently held in this container as a vector.

        :return: a vector of complex roots
        :rtype: NDArray[complex128]
        """
        result: List[complex] = []
        while not self.rootBuffer.empty():
            result.append(self.rootBuffer.get()[0])
        return np.array(result)

    def getRootOrders(self) -> NDArray[np.int32]:
        """
        Returns the orders of all roots currently held in this container as a
        vector which is parallel to the vector returned by `getRoots`.

        :return: a vector of integer root orders (multiplicities)
        :rtype: NDArray[int32]
        """
        result: List[complex] = []
        while not self.rootBuffer.empty():
            result.append(self.rootBuffer.get()[0])
        return np.array(result)

    def clear(self) -> None:
        "Plain containers cannot be cleared."
        raise NotImplementedError("cannot clear plain containers!")

    def registerFilter(self, filterPredicate: tRootFilter, key: str) -> None:
        """
        TODO
        """
        raise NotImplementedError("plain containers do not support filtering!")

    def unregisterFilter(self, key: str) -> None:
        """
        TODO
        """
        raise NotImplementedError("plain containers do not support filtering!")
