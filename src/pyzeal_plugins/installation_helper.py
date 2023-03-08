"""
Module installation_helper.py from the package PyZEAL.
TODO

Authors:\n
- Philipp Schuette\n
"""

from os import remove
from os.path import exists, join
from shutil import copy

from pyzeal_plugins.plugin_loader import PLUGIN_INSTALL_DIR


class InstallationHelper:
    "Static helper class that provides plugin installation related functions."

    @staticmethod
    def installPlugin(fullPath: str) -> bool:
        """
        _summary_

        :param fullPath: _description_
        :type fullPath: _type_
        :return: _description_
        :rtype: _type_
        """
        if not exists(fullPath):
            return False
        copy(fullPath, PLUGIN_INSTALL_DIR)
        return True

    @staticmethod
    def uninstallPlugin(filename: str) -> bool:
        """
        _summary_

        :param filename: _description_
        :type filename: _type_
        :return: _description_
        :rtype: _type_
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
        _summary_

        :param filename: _description_
        :type filename: _type_
        :return: _description_
        :rtype: _type_
        """
        return join(fullPath, filename)
