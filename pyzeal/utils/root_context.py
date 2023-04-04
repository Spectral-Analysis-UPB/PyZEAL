"""
Class RootContext from the package pyzeal_util.
This module defines a data container that holds the information necessary for
a generic root finding algorithm to function.

Authors:\n
- Philipp Schuette\n
"""

from dataclasses import dataclass
from typing import Optional, Tuple

from rich.progress import TaskID

from pyzeal.pyzeal_types.root_types import tHoloFunc
from pyzeal.utils.containers.root_container import RootContainer
from pyzeal.utils.filter_context import FilterContext
from pyzeal.utils.finder_progress import FinderProgressBar


@dataclass(frozen=True)
class RootContext:
    """
    Container for the data context of a root finding algorithm. The container
    is read-only.
    """

    f: tHoloFunc
    df: Optional[tHoloFunc]
    container: RootContainer
    precision: Tuple[int, int]
    reRan: Tuple[float, float] = (-1.0, 1.0)
    imRan: Tuple[float, float] = (-1.0, 1.0)
    progress: Optional[FinderProgressBar] = None
    task: Optional[TaskID] = None

    def toFilterContext(self) -> FilterContext:
        """
        Get a `FilterContext` object with the same parameters as this
        `RootContext`

        :return: `FilterContext` object with the same parameters as this
            `RootContext`
        """
        return FilterContext(self.f, self.reRan, self.imRan, self.precision)

    def functionDataToString(self) -> str:
        """
        Return a string describing the data stored by this object

        :return: Object data
        """
        return (
            f"{getattr(self.f, '__name__', '<unnamed>')} on rectangle "
            + f"[{self.reRan[0]}, {self.reRan[1]}] "
            + f"x [{self.imRan[0]}, {self.imRan[1]}]"
        )
