"""
Implementation RoundingContainer of the RootContainer protocol from the
pyzeal_utils package.
The concrete container class implemented here automatically rounds added roots
to a fixed number of decimal places.

Authors:\n
- Philipp Schuette\n
"""

from logging import INFO
from typing import Dict, Optional, Set, Tuple

import numpy as np
from numpy.typing import NDArray

from pyzeal.pyzeal_types.root_types import tRoot, tVec
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.containers.root_container import RootContainer
from pyzeal.utils.filter_context import FilterContext, tRootFilter
from pyzeal.utils.service_locator import ServiceLocator


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

    def __init__(self, precision: Optional[Tuple[int, int]]) -> None:
        """
        Initialize a rounding RootContainer. If no precision is given,
        default precision is used.

        :param precision: expected accuracy of roots to be added
        """
        self.precision = (
            precision or ServiceLocator.tryResolve(SettingsService).precision
        )
        self.rootSet: Set[tRoot] = set()
        self.filters: Dict[str, tRootFilter] = {}
        self.logger.info("initialized a new rounding root container")

    def addRoot(self, root: tRoot, context: FilterContext) -> None:
        """
        Add a new root with given accuracy to the container. If the accuracy
        differs from the accuracy of roots already added then all previous
        roots are removed.

        :param root: the root to be added to the container
        :param context: the context of the new root, required for filtering
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
            "attempting to add new root %f + %fi to rounding container!",
            root[0].real,
            root[0].imag,
        )
        roundedRoot = RoundingContainer.roundRoot(root, self.precision)
        if self.logger.isEnabledFor(INFO) and roundedRoot in self.rootSet:
            self.logger.info("duplicate root discarded by rounding container!")
            return
        self.logger.info(
            "new root %f + %fi added to rounding container",
            roundedRoot[0].real,
            roundedRoot[0].imag,
        )
        self.rootSet.add(roundedRoot)

    def removeRoot(self, root: tRoot) -> bool:
        """
        Remove a given root from the container. Return value indicates success.

        :param root: the root to be removed from the container
        :return: a boolean flag indicating if a removal happened
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
        :param precision: the number of decimal places to round to
        :return: the rounded root (multiplicity stays constant)
        """
        x, y = root[0].real, root[0].imag
        return complex(round(x, precision[0]), round(y, precision[1])), root[1]

    def registerFilter(self, filterPredicate: tRootFilter, key: str) -> None:
        """
        Register a new filter to check possible roots against

        :param filterPredicate: New filter to register
        :param key: A key to identify this filter
        """
        self.filters[key] = filterPredicate

    def unregisterFilter(self, key: str) -> None:
        """
        Remove the filter identified by `key`.

        :param key: Filter key
        """
        try:
            self.filters.pop(key)
            self.logger.debug("removed filter %s", key)
        except KeyError:
            self.logger.info("tried to remove non-existent filter %s!", key)
