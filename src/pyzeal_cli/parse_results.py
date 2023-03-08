"""
TODO

Authors:\n
- Philipp Schuette\n
"""

from dataclasses import dataclass


@dataclass
class ParseResults:
    """
    TODO
    """

    doPrint: bool
    container: str
    algorithm: str
    logLevel: str
    verbose: str
    listPlugins: bool
    listModules: bool
    install: str
    uninstall: str
