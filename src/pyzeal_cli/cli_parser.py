"""
Module cli_parser.py from the pyzeal_cli package.
This module implements a very PyZEAL specific command line argument parser
which gets used by the main entry point `__main__.py` to parse incoming user
arguments.

Authors:\n
- Philipp Schuette\n
"""

from argparse import ArgumentParser
from importlib.metadata import version
from typing import Final

from pyzeal_cli.parse_results import ParseResults
from pyzeal_cli.parser_facade import PyZEALParserInterface


class PyZEALParser(ArgumentParser, PyZEALParserInterface):
    """
    Specialized `argparse.ArgumentParser` which parses arguments provided to
    the PyZEAL CLI by a user.
    """

    MAIN_DESCRIPTION: Final[str] = (
        "welcome to the PyZEAL project! from the command line you can control "
        "various aspects of this package, like viewing and manipulating the "
        "settings which control its default behaviour."
    )
    SETTINGS_PLUGINS_DESCRIPTION: Final[str] = (
        "manipulate PyZEAL behaviour by changing the (default) settings and"
        " (un-)installing (custom) plugins"
    )
    PROGRAM_NAME: Final[str] = "pyzeal"
    VERSION: Final[str] = version(PROGRAM_NAME)

    def __init__(self) -> None:
        """
        Initialize a new `PyZEALParser` parser instance. The parser recognizes
        basic optional arguments like `--help` and `--version` as well as the
        subcommands `change` and `view` related to customization of settings.
        """
        super().__init__(
            description=PyZEALParser.MAIN_DESCRIPTION,
            prog=f"{PyZEALParser.PROGRAM_NAME}",
        )

        # add version info option
        self.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {PyZEALParser.VERSION}",
        )

        # add subcommands for options and plugins
        subParsers = self.add_subparsers(
            title=PyZEALParser.SETTINGS_PLUGINS_DESCRIPTION,
            help="view/change settings and (un-)install plugins",
            parser_class=ArgumentParser,
        )
        viewParser = subParsers.add_parser("view")
        viewParser.add_argument(
            "-p", "--print", action="store_true", help="print current settings"
        )

        changeParser = subParsers.add_parser("change")
        changeParser.add_argument(
            "--container",
            dest="container",
            choices=["rounding"],
            help="change current default container",
        )
        changeParser.add_argument(
            "--algorithm",
            choices=[
                "newton_grid",
                "simple_argument",
                "simple_argument_newton",
            ],
            help="change current default algorithm",
        )
        changeParser.add_argument(
            "--log-level",
            choices=["debug", "info", "warning", "error", "critical"],
            help="change current default log level",
        )
        changeParser.add_argument(
            "--verbose",
            choices=["true", "True", "false", "False"],
            help="change current default verbosity level",
        )

        # add subcommands for (un-)installing plugins
        pluginParser = subParsers.add_parser("plugin")
        pluginParser.add_argument(
            "-l", "--list", action="store_true", help="list installed plugins"
        )
        pluginParser.add_argument(
            "-m",
            "--modules",
            action="store_true",
            help="list contents of installation directory",
        )
        pluginParser.add_argument(
            "--install",
            help="install a given file containing a plugin (or plugin data)",
        )
        pluginParser.add_argument(
            "--uninstall",
            help="uninstall a given plugin-related (data or source) file",
        )

    def parseArgs(self) -> ParseResults:
        """
        TODO
        """
        # fetch cli arguments
        args = super().parse_args()

        # extract cli arguments
        doPrint = getattr(args, "print", None)
        container = getattr(args, "container", None)
        algorithm = getattr(args, "algorithm", None)
        logLevel = getattr(args, "log_level", None)
        verbose = getattr(args, "verbose", None)
        listPlugins = getattr(args, "list", None)
        listModules = getattr(args, "modules", None)
        install = getattr(args, "install", None)
        uninstall = getattr(args, "uninstall", None)

        # return wrapped cli arguments
        return ParseResults(
            doPrint=bool(doPrint) if doPrint else False,
            container=container if container else "",
            algorithm=algorithm if algorithm else "",
            logLevel=logLevel if logLevel else "",
            verbose=verbose if verbose else "",
            listPlugins=bool(listPlugins) if listPlugins else False,
            listModules=bool(listModules) if listModules else False,
            install=install if install else "",
            uninstall=uninstall if uninstall else "",
        )
