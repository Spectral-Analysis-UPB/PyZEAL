"""
TODO

Authors:\n
- Philipp Schuette\n
"""

from dataclasses import dataclass


@dataclass
class SettingsParseResults:
    """
    TODO
    """

    doPrint: bool
    container: str
    algorithm: str
    logLevel: str
    verbose: str


@dataclass
class PluginParseResults:
    """
    TODO
    """

    listPlugins: bool
    listModules: bool
    install: str
    uninstall: str
