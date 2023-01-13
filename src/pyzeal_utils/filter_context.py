"""
Class FilterContext from the package pyzeal_util.
This module defines a data container that holds the information necessary for
a generic root filter predicate to function.

Authors:\n
- Philipp Schuette\n
"""

from dataclasses import dataclass
from typing import Callable, Tuple

from pyzeal_types.root_types import tHoloFunc, tRoot


@dataclass(frozen=True)
class FilterContext:
    """
    Container for the data context of a root filter predicate. The container is
    read-only.
    """

    f: tHoloFunc
    reRan: Tuple[float, float]
    imRan: Tuple[float, float]
    precision: Tuple[int, int]
    threshold: int = 3


# type used for filter predicates that filter roots upon container insertion
tRootFilter = Callable[[tRoot, FilterContext], bool]
