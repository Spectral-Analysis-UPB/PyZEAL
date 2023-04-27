"""
TODO.

Authors:\n
- Philipp Schuette\n
"""

from typing import Protocol, runtime_checkable

from pyzeal.cli.parse_results import (
    InstallTestingParseResults,
    PluginParseResults,
    SettingsParseResults,
)


@runtime_checkable
class CLIControllerFacade(Protocol):
    """
    Interface for a generic controller instance used with the `PyZEAL` cli.
    """

    def handleViewSubcommand(self, args: SettingsParseResults) -> None:
        """
        Check if the 'view' subcommand was selected and print current settings.

        :param args: Parsed settings values
        """
        ...

    def handleChangeSubcommand(self, args: SettingsParseResults) -> None:
        """
        Check if the 'change' subcommand was selected and change settings
        accordingly.

        :param args: Parsed settings values
        """
        ...

    def handlePluginSubcommand(self, args: PluginParseResults) -> None:
        """
        Check if the 'plugin' subcommand was selected and manipulate plugins
        accordingly.

        :param args: Parsed plugin request values
        """
        ...

    def handleTestingOption(self, args: InstallTestingParseResults) -> bool:
        """
        Check if the '--test' option was selected and start testing the local
        `PyZEAL` installation accordingly.

        :param args: parsed testing option
        :return: flag indicating if the testing option was given
        """
        ...
