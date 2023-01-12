"""
Class FinderAlgorithm from the package pyzeal_algorithms.
This module defines an abstract class/interface for a generic root finding
algorithm.

Authors:\n
- Philipp Schuette\n
"""

from abc import ABC, abstractmethod

from pyzeal_utils.root_context import RootContext
from pyzeal_logging.loggable import Loggable


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
        context.

        :param context: context in which the algorithm operates
        :type context: RootContext
        :return: roots calculated by the algorithm in the given context
        :rtype: NDArray[complex128]
        """
