"""
Class PyZEALParserInterface from the package pyzeal_cli.
This module provides a facade for `argparser.ArgumentParser` class from the
standard library `argparse` module. Any access to (CLI-)parsers in this project
should happen only through this interface.

Authors:\n
- Philipp Schuette\n
"""

from typing import Protocol, Tuple, runtime_checkable

from pyzeal.cli.parse_results import (
    InstallTestingParseResults,
    PluginParseResults,
    SettingsParseResults,
)


@runtime_checkable
class PyZEALParserInterface(Protocol):
    """
    Acts as a facade for the standard library `ArgumentParser`.
    """

    def parseArgs(
        self,
    ) -> Tuple[
        SettingsParseResults, PluginParseResults, InstallTestingParseResults
    ]:
        """
        Read command line arguments, parse the read arguments and return them
        wrapped according to the `pyzeal_cli` data contract for parsed command
        line arguments.

        :return: the wrapped parsing results
        """
        ...
