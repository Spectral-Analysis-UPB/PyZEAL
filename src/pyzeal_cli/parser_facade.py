"""
Class PyZEALParserInterface from the package pyzeal_cli.
This module provides a facade for `argparser.ArgumentParser` class from the
standard library `argparse` module. Any access to (CLI-)parsers in this project
should happen only through this interface.

Authors:\n
- Philipp Schuette\n
"""

from typing import Protocol

from pyzeal_cli.parse_results import ParseResults


class PyZEALParserInterface(Protocol):
    """
    TODO
    """

    def parseArgs(self) -> ParseResults:
        """
        TODO
        """
        ...
