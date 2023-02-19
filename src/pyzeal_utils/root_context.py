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

from pyzeal_types.root_types import tHoloFunc
from pyzeal_utils.filter_context import FilterContext
from pyzeal_utils.finder_progress import FinderProgressBar
from pyzeal_utils.pyzeal_containers.root_container import RootContainer
from pyzeal_settings.json_settings_service import JSONSettingsService

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
    precision: Tuple[int, int] = JSONSettingsService().precision
    progress: Optional[FinderProgressBar] = None
    task: Optional[TaskID] = None

    def toFilterContext(self) -> FilterContext:
        """Get a `FilterContext` object with the same parameters as this
        `RootContext`

        :return: `FilterContext` object with the same parameters as this
            `RootContext`
        :rtype: FilterContext
        """
        return FilterContext(self.f, self.reRan, self.imRan, self.precision)

    def functionDataToString(self) -> str:
        """Return a string describing the data stored by this object

        :return: Object data
        :rtype: str
        """
        return (
            f"{getattr(self.f, '__name__', '<unnamed>')} on rectangle "
            + f"[{self.reRan[0]}, {self.reRan[1]}] "
            + f"x [{self.imRan[0]}, {self.imRan[1]}]"
        )
