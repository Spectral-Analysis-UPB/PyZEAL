"""
This module contains the base interface for plugins. Its methods provide the
necessary functions for plugin handling.

Authors:\n
- Philipp Schuette\n
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Generic, Tuple, Type, TypeVar, Union

from pyzeal.algorithms.estimators.argument_estimator import ArgumentEstimator
from pyzeal.algorithms.finder_algorithm import FinderAlgorithm
from pyzeal.cli.parser_facade import PyZEALParserInterface
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.containers.root_container import RootContainer

tPluggable = Union[
    FinderAlgorithm,
    ArgumentEstimator,
    RootContainer,
    SettingsService,
    PyZEALParserInterface,
]
T_co = TypeVar("T_co", bound=tPluggable, covariant=True)


class PyZEALPlugin(ABC, Generic[T_co]):
    """
    Interface for plugins. Methods for instantiation and plugin information
    need to be implemented.
    """

    def __str__(self) -> str:
        "Print a human-readable representation of the plugin."
        major, minor, patch = self.pluginVersion
        maxLength = 30
        cutoff = min(len(self.pluginName), maxLength)
        return (
            f"{self.pluginName[:cutoff]: <{maxLength}} "
            f" @ v{major}.{minor}.{patch}"
        )

    @staticmethod
    @abstractmethod
    def initialize() -> Callable[..., T_co]:
        """
        Returns a factory for the plugin's implementation of `T_co`.

        :return: Factory for plugin implementation of `T_co`.
        """

    @staticmethod
    @abstractmethod
    def getInstance() -> PyZEALPlugin[T_co]:
        """
        Return the singleton instance of `PyZEALPlugin` which provides a
        service of type `T_co`.

        :return: `PyZEALPlugin` instance.
        """

    @property
    @abstractmethod
    def pluginType(self) -> Type[T_co]:
        """
        Return the type provided by the plugin.

        :return: Service type of plugin.
        """
        ...

    @property
    @abstractmethod
    def pluginName(self) -> str:
        """
        Return the name of the plugin.

        :return: Plugin name.
        """
        ...

    @property
    @abstractmethod
    def pluginVersion(self) -> Tuple[int, int, int]:
        """
        Return the version of the plugin as (`major`, `minor`, `patch`).

        :return: Plugin version.
        """
        ...
