"""
This module contains dataclasses for storing results fof command-line parsing.

Authors:\n
- Philipp Schuette\n
"""

from dataclasses import dataclass
from typing import Optional, Tuple


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
    precision: Optional[Tuple[int, int]]


@dataclass
class PluginParseResults:
    """
    Container for parsing results related to plugins.
    """

    listPlugins: bool
    listModules: bool
    install: str
    uninstall: str


@dataclass
class InstallTestingParseResults:
    """
    Container for parsing results related to testing of the installation.
    """

    doTest: bool
