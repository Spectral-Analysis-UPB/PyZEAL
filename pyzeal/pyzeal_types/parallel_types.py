"""
This module provides type aliases used in conjunction with multiprocessing.

Authors:\n
- Philipp Schuette\n
"""

from multiprocessing.managers import BaseManager
from typing import Callable, Protocol, Tuple

from pyzeal.utils.finder_progress import FinderProgressBar


# typed queues to be used for message passing with multiprocessing.Queue
class tQueue(Protocol):
    r"""
    Queue that stores tuples of the form (root: complex, order: int).
    """

    def get(self) -> Tuple[complex, int]:
        "Get first element of the queue."
        ...

    def put(self, item: Tuple[complex, int]) -> None:
        "Put element into the queue."
        ...

    def empty(self) -> bool:
        "Check if queue is empty."
        ...


# multiprocessing managers used to share access to progress bars
class FinderProgressManager(BaseManager):
    r"""
    Multiprocessing.BaseManager containing a rich.progress.Progress instance.
    """
    finderProgress: Callable[..., FinderProgressBar]
