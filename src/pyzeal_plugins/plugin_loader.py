"""
Module plugin_loader.py from the package PyZEAL.
TODO

Authors:\n
- Philipp Schuette\n
"""

from __future__ import annotations

from abc import ABCMeta
from importlib import import_module
from os import listdir
from os.path import dirname, join, splitext
from re import compile as compileRegex
from types import ModuleType
from typing import Final, List, Optional, Type

from pyzeal_logging.loggable import Loggable
from pyzeal_plugins.pyzeal_plugin import PyZEALPlugin, tPluggable
from pyzeal_utils.service_locator import ServiceLocator

# default location where custom plugins are installed
PLUGIN_INSTALL_DIR: Final[str] = join(dirname(__file__), "custom_plugins")


class PluginLoader(Loggable):
    """
    _summary_
    """

    _instance: Optional[PluginLoader] = None

    @staticmethod
    def getInstance() -> PluginLoader:
        """
        _summary_

        :return: _description_
        :rtype: _type_
        """
        return (
            PluginLoader._instance
            if PluginLoader._instance is not None
            else PluginLoader()
        )

    @staticmethod
    def loadPlugins(
        path: str = PLUGIN_INSTALL_DIR,
    ) -> List[PyZEALPlugin[tPluggable]]:
        """
        _summary_

        :param path: _description_, defaults to PLUGIN_INSTALL_DIR
        :type path: str
        :return: _description
        :rtype: List[str]
        """
        instance = PluginLoader.getInstance()
        plugins: List[PyZEALPlugin[tPluggable]] = []
        for plugin in instance.locateAndLoadPlugins(path):
            pluginInstance = plugin.getInstance()
            ServiceLocator.registerAsTransient(
                pluginInstance.pluginType, plugin.initialize()
            )
            plugins.append(pluginInstance)
        return plugins

    def locateAndLoadPlugins(
        self, path: str
    ) -> List[Type[PyZEALPlugin[tPluggable]]]:
        """
        _summary_

        :param path: _description_
        :type path: _type_
        :return: _description_
        :rtype: _type_
        """
        plugins: List[Type[PyZEALPlugin[tPluggable]]] = []
        self.logger.info("starting plugin discovery in %s...", path)
        candidates = PluginLoader.discoverModules(path)
        self.logger.debug("contents of plugin directory: %s", str(candidates))
        for candidate in candidates:
            if not (candidate := PluginLoader.isPyFile(candidate)):
                continue
            self.logger.info("module %s might contain a plugin...", candidate)
            module = import_module(
                candidate, package="pyzeal_plugins.custom_plugins"
            )
            plugin = self.loadPlugin(module)
            if plugin is not None:
                plugins.append(plugin)
        return plugins

    def loadPlugin(
        self, candidateModule: ModuleType
    ) -> Optional[Type[PyZEALPlugin[tPluggable]]]:
        """
        _summary_

        :param pluginName: _description_
        :type pluginName: _type_
        :return: _description_
        :rtype: _type_
        """
        attributeNames = PluginLoader.discoverAttributes(candidateModule)
        self.logger.debug(
            "module attributes %s found during plugin discovery!",
            str(attributeNames),
        )
        for attributeName in attributeNames:
            attribute = getattr(candidateModule, attributeName)
            if attribute == PyZEALPlugin:
                continue
            if isinstance(attribute, ABCMeta):
                if issubclass(attribute, PyZEALPlugin):
                    self.logger.info(
                        "plugin implementation [ %s ] found!",
                        str(attribute),
                    )
                    return attribute
        return None

    @staticmethod
    def isPyFile(filename: str) -> str:
        """
        _summary_

        :param filename: _description_
        :type filename: _type_
        :return: _description_
        :rtype: _type_
        """
        if filename == "__init__.py":
            return ""

        name, extension = splitext(filename)
        return "." + name if extension.lower() == ".py" else ""

    @staticmethod
    def discoverModules(path: str) -> List[str]:
        """
        _summary_

        :param path: _description_
        :type path: _type_
        :return: _description_
        :rtype: _type_
        """
        regex = compileRegex(r"__.*")
        candidates = [c for c in listdir(path) if not regex.match(c)]
        return candidates

    @staticmethod
    def discoverAttributes(candidateModule: ModuleType) -> List[str]:
        """
        _summary_

        :param moduleType: _description_
        :type moduleType: _type_
        :return: _description_
        :rtype: _type_
        """
        regex = compileRegex(r"__.*")
        candidates = [c for c in dir(candidateModule) if not regex.match(c)]
        return candidates
