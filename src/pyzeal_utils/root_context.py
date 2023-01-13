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
from rich.progress import TaskID

from pyzeal_utils.filter_context import FilterContext
from pyzeal_utils.finder_progress import FinderProgressBar
from pyzeal_utils.root_container import RootContainer


@dataclass(frozen=True)
class RootContext:
    """
    Container for the data context of a root finding algorithm. The container
    is read-only.
    """

    f: tHoloFunc
    df: Optional[tHoloFunc]
    container: RootContainer
    reRan: Tuple[float, float] = (-1.0, 1.0)
    imRan: Tuple[float, float] = (-1.0, 1.0)
    precision: Tuple[int, int] = 3, 3
    progress: Optional[FinderProgressBar] = None
    task: Optional[TaskID] = None

    def toFilterContext(self) -> FilterContext:
        """
        TODO
        """
        return FilterContext(self.f, self.reRan, self.imRan, self.precision)
