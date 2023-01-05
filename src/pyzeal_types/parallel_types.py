"""
This module provides type aliases used in conjunction with multiprocessing.

Authors:\n
- Philipp Schuette\n
"""

from abc import ABC, abstractmethod
from multiprocessing.managers import BaseManager
from typing import Callable, Tuple

from rich.progress import Progress


# typed queues to be used for message passing with multiprocessing.Queue
class tQueue(ABC):
    r"""
    Queue that stores tuples of the form (root: complex, order: int).
    """

    @abstractmethod
    def get(self) -> Tuple[complex, int]:
        "Get first element of the queue."

    @abstractmethod
    def put(self, item: Tuple[complex, int]) -> None:
        "Put element into the queue."

    @abstractmethod
    def empty(self) -> bool:
        "Check if queue is empty."


# multiprocessing managers used to share access to progress bars
class MyManager(BaseManager):
    r"""
    Multiprocessing.BaseManager containing a rich.progress.Progress instance.
    """
    progress: Callable[..., Progress]
