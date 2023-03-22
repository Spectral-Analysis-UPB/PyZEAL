"""
Module installation_helper.py from the package PyZEAL.
This module contains various helper functions related to plugin installation.

Authors:\n
- Philipp Schuette\n
"""

from os import remove
from os.path import exists, join
from shutil import copy

from pyzeal.plugins.plugin_loader import PLUGIN_INSTALL_DIR


class InstallationHelper:
    "Static helper class that provides plugin installation related functions."

    @staticmethod
    def installPlugin(fullPath: str) -> bool:
        """
        Copies the plugin located at `fullPath` to the plugin directory to
        install it.

        :param fullPath: Current path of the to-be-installed plugin.
        :return: `True` if successful.
        """
        if not exists(fullPath):
            return False
        copy(fullPath, PLUGIN_INSTALL_DIR)
        return True

    @staticmethod
    def uninstallPlugin(filename: str) -> bool:
        """
        Uninstall the plugin given by `filename`.

        :param filename: Filename of plugin to remove
        :return: `True` if successful.
        """
        try:
            remove(join(PLUGIN_INSTALL_DIR, filename))
            return True
        except (FileNotFoundError, OSError):
            return False

    @staticmethod
    def returnDataPath(
        filename: str, fullPath: str = PLUGIN_INSTALL_DIR
    ) -> str:
        """
        Helper function to construct the full path to plugin data.

        :param filename: Filename of plugin data.
        :param fullPath: Full path to the directory in which the data is
            located, defaults to PLUGIN_INSTALL_DIR
        :return: Path to plugin data
        """
        return join(fullPath, filename)
