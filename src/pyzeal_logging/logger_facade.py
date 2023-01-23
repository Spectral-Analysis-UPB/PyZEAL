"""
Class PyZEALLogger from the package pyzeal.
This module provides a facade for `logging.Logger` class from the standard
library `logging` module. Any access to loggers in this project should happen
only through this interface.

Authors:\n
- Philipp Schuette\n
"""

from typing import Protocol, Union


class PyZEALLogger(Protocol):
    "The logging interface used throughout the PyZEAL project."

    def debug(self, msg: str, *args: Union[str, int, float]) -> None:
        """
        TODO
        """
        ...

    def info(self, msg: str, *args: Union[str, int, float]) -> None:
        """
        TODO
        """
        ...

    def warning(self, msg: str, *args: Union[str, int, float]) -> None:
        """
        TODO
        """
        ...

    def error(self, msg: str, *args: Union[str, int, float]) -> None:
        """
        TODO
        """
        ...

    def critical(self, msg: str, *args: Union[str, int, float]) -> None:
        """
        TODO
        """
        ...

    def setLevel(self, level: int) -> None:
        """
        TODO
        """
        ...

    def isEnabledFor(self, level: int) -> bool:
        """
        TODO
        """
        ...
