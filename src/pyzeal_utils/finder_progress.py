"""
Class FinderProgressBar from the package pyzeal_utils.
This module defines a progress bar used for command line display of the
progress a running root finding algorithm has made.

Authors:\n
- Philipp Schuette\n
"""

from os import getpid

from rich.progress import Progress, SpinnerColumn, TaskID, TimeElapsedColumn


class FinderProgressBar(Progress):
    """
    This class is a very specialized subtype of the general `rich.Progress`
    type representing a very customizable command line displayed progress bar.
    """

    def __init__(self) -> None:
        "Initialize a root finder specific progress bar with fixed defaults."
        super().__init__(
            *Progress.get_default_columns()[:],
            SpinnerColumn(),
            "Elapsed:",
            TimeElapsedColumn(),
            transient=False,
            refresh_per_second=3,
            speed_estimate_period=10,
            expand=True,
        )

    def addTask(self, total: float) -> TaskID:
        """
        Override the `add_task()` method of generic progress bars by allowing
        only the total amount of work to be adjusted and prescribing a default
        task description.

        :param total: the total amount of work contained in the added task
        :type total: float
        """
        return super().add_task(
            description=(f"[magenta]{getpid()}: " + "[g]getting roots..."),
            total=total,
        )
