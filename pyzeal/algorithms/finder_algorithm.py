"""
Class FinderAlgorithm from the package pyzeal_algorithms.

This module defines an abstract class/interface for a generic root finding
algorithm. This builds the foundation for the primary user-facing API of
`PyZEAL`.

Authors:\n
- Philipp Schuette\n
"""

from abc import ABC, abstractmethod

from pyzeal.pyzeal_logging.loggable import Loggable
from pyzeal.utils.root_context import RootContext


class FinderAlgorithm(ABC, Loggable):
    """
    Abstract class representation of a generic root finding algorithm. Concrete
    algorithms are implemented by subclassing this class and overriding the
    virtual method `calcRoots` appropriately.
    """

    @abstractmethod
    def calcRoots(self, context: RootContext) -> None:
        """
        Entry point for a generic root finding algorithm operating in a given
        context. Found roots are expected to be inserted into
        `context.container` upon the algorithms completion.

        :param context: Context in which the algorithm operates.
        """
