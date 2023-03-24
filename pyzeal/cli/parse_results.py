"""
This module contains dataclasses for storing results fof command-line parsing.

Authors:\n
- Philipp Schuette\n
"""

from dataclasses import dataclass


@dataclass
class SettingsParseResults:
    """
    Container for parsing results related to settings.
    """

    doPrint: bool
    container: str
    algorithm: str
    estimator: str
    logLevel: str
    verbose: str


@dataclass
class PluginParseResults:
    """
    Container for parsing results related to plugins.
    """

    listPlugins: bool
    listModules: bool
    install: str
    uninstall: str
