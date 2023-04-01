"""
Module plugin_loader.py from the package PyZEAL.
This module handles discovering, loading and registering of plugins.

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

from pyzeal.plugins.pyzeal_plugin import PyZEALPlugin, tPluggable
from pyzeal.pyzeal_logging.loggable import Loggable
from pyzeal.utils.service_locator import ServiceLocator

# default location where custom plugins are installed
PLUGIN_INSTALL_DIR: Final[str] = join(dirname(__file__), "custom_plugins")


class PluginLoader(Loggable):
    """
    This class handles plugin discovery, loading and registration.
    """

    _instance: Optional[PluginLoader] = None

    @staticmethod
    def getInstance() -> PluginLoader:
        """
        Return the global `PluginLoader` instance. If no instance exists,
        a new one is created and returned.

        :return: `PluginLoader` singleton instance.
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
        Load plugins present in `path`.

        :param path: Path to search for plugins, defaults to PLUGIN_INSTALL_DIR
        :return: List of loaded plugins.
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
        self, path: str = PLUGIN_INSTALL_DIR
    ) -> List[Type[PyZEALPlugin[tPluggable]]]:
        """
        Discover plugins at a given path and load them.

        :param path: Path to search for plugins, defaults to PLUGIN_INSTALL_DIR
        :return: List of found plugins.
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
        Try to load a candidate plugin and return it if successful.

        :param candidateModule: Candidate plugin module
        :return: Plugin if an implementation has been found, else `None`.
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
        Returns `True` if `filename` corresponds to a python file.

        :param filename: File to evaluate
        :return: `True` if `filename` corresponds to a python file.
        """
        if filename == "__init__.py":
            return ""

        name, extension = splitext(filename)
        return "." + name if extension.lower() == ".py" else ""

    @staticmethod
    def discoverModules(path: str = PLUGIN_INSTALL_DIR) -> List[str]:
        """
        Discover all possible plugin files in `path`. Ignore files starting
        with `__`.

        :param path: Path to search, defaults to PLUGIN_INSTALL_DIR
        :return: List of plugin candidates.
        """
        regex = compileRegex(r"__.*")
        candidates = [c for c in listdir(path) if not regex.match(c)]
        return candidates

    @staticmethod
    def discoverAttributes(candidateModule: ModuleType) -> List[str]:
        """
        Discover attributes of a candidate module. Ignores attributes
        starting with `__`.

        :param candidateModule: Candidate module
        :return: List of attributes.
        """
        regex = compileRegex(r"__.*")
        candidates = [c for c in dir(candidateModule) if not regex.match(c)]
        return candidates
