"""
Module cli_parser.py from the pyzeal_cli package.
This module implements a very PyZEAL specific command line argument parser
which gets used by the main entry point `__main__.py` to parse incoming user
arguments.

Authors:\n
- Philipp Schuette\n
"""

from __future__ import annotations

from argparse import ArgumentParser, _SubParsersAction
from importlib.metadata import version
from typing import Final, Tuple

from pyzeal.cli.parse_results import (
    InstallTestingParseResults,
    PluginParseResults,
    SettingsParseResults,
)
from pyzeal.cli.parser_facade import PyZEALParserInterface


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

        self.addVersionOption()
        # one could also let the user choose from a set of submodules to test
        self.addTestingOption()

        # add subcommands for options and plugins
        subParsers = self.add_subparsers(
            title=PyZEALParser.SETTINGS_PLUGINS_DESCRIPTION,
            help="view/change settings, (un-)install plugins and run tests",
            parser_class=ArgumentParser,
        )

        self.addViewSubcommand(subParsers)
        self.addChangeSubcommand(subParsers)
        self.addPluginSubcommand(subParsers)

    def addVersionOption(self) -> None:
        """
        Add version info option to the cli.
        """
        self.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {PyZEALParser.VERSION}",
        )

    def addTestingOption(self) -> None:
        """
        Add complete project testing option to the cli.
        """
        self.add_argument(
            "-t", "--test", action="store_true", help="test complete project"
        )

    def addViewSubcommand(
        self, subParsers: _SubParsersAction[ArgumentParser]
    ) -> None:
        """
        Add view subcommand and its options to the cli.

        :param subParsers: _description_
        """
        viewParser = subParsers.add_parser("view")
        viewParser.add_argument(
            "-p", "--print", action="store_true", help="print current settings"
        )

    def addChangeSubcommand(
        self, subParsers: _SubParsersAction[ArgumentParser]
    ) -> None:
        """
        Add change subcommand and its options to the cli.

        :param subParsers: _description_
        """
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
                "associated_polynomial",
            ],
            help="change current default algorithm",
        )
        changeParser.add_argument(
            "--estimator",
            choices=["summation", "quadrature"],
            help="change current default estimator",
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
        changeParser.add_argument(
            "--precision",
            nargs=2,
            type=int,
            help="change current default root finding precision",
        )

    def addPluginSubcommand(
        self, subParsers: _SubParsersAction[ArgumentParser]
    ) -> None:
        """
        Add plugin subcommand and its options to the cli.

        :param subParsers: The subparser to add Plugin commands to
        """
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

    def parseArgs(
        self,
    ) -> Tuple[
        SettingsParseResults, PluginParseResults, InstallTestingParseResults
    ]:
        """
        Read command line arguments, parse the read arguments and return them
        wrapped according to the `pyzeal_cli` data contract for parsed command
        line arguments.

        :return: the wrapped results of the parsing process
        """
        # fetch cli arguments
        args = super().parse_args()

        # return wrapped cli arguments
        parseArgs = SettingsParseResults(
            doPrint=getattr(args, "print", False),
            container=getattr(args, "container", ""),
            algorithm=getattr(args, "algorithm", ""),
            estimator=getattr(args, "estimator", ""),
            logLevel=getattr(args, "log_level", ""),
            verbose=getattr(args, "verbose", ""),
            precision=tuple(precision)  # type: ignore
            if (precision := getattr(args, "precision", None))
            else None,
        )
        pluginArgs = PluginParseResults(
            listPlugins=getattr(args, "list", False),
            listModules=getattr(args, "modules", False),
            install=getattr(args, "install", ""),
            uninstall=getattr(args, "uninstall", ""),
        )
        testingArgs = InstallTestingParseResults(
            doTest=getattr(args, "test", False)
        )

        return parseArgs, pluginArgs, testingArgs
