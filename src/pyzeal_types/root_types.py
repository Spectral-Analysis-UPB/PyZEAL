"""
This module provides type aliases used throughout the PyZEAL project.

Authors:\n
- Philipp Schuette\n
"""

from abc import ABC, abstractmethod
from multiprocessing.managers import BaseManager
from typing import Callable, List, Tuple, Union

import numpy as np
from numpy.typing import NDArray
from rich.progress import Progress

# general purpose types used throughout
tScal = Union[float, complex]
tVec = NDArray[np.complex128]

# types used for rootfinder results and internally
tRecGrid = Tuple[
    NDArray[np.complex128],
    NDArray[np.complex128],
    NDArray[np.complex128],
    NDArray[np.complex128],
]

tResVec = Union[List[Tuple[tScal, int]], tVec]
tErrVec = Union[List[tScal], tVec]


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
