"""
Class RootContext from the package pyzeal_util.
This module defines a data container that holds the information necessary for
a generic root finding algorithm to function.

Authors:\n
- Philipp Schuette\n
"""

from dataclasses import dataclass
from typing import Optional, Tuple

from pyzeal_types.root_types import tHoloFunc


@dataclass(frozen=True)
class RootContext:
    """
    Container for the data context of a root finding algorithm. The container
    is read-only.
    """
    f: tHoloFunc
    df: Optional[tHoloFunc]
    reRan: Tuple[float, float] = (-1., 1.)
    imRan: Tuple[float, float] = (-1., 1.)
    accuracy: int = 3
