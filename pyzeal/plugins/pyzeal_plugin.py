"""
This module contains the base interface for plugins. Its methods provide the
necessary functions for plugin handling.

Authors:\n
- Philipp Schuette\n
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Tuple, Type, TypeVar, Union

from pyzeal.algorithms.estimators.argument_estimator import ArgumentEstimator
from pyzeal.algorithms.finder_algorithm import FinderAlgorithm
from pyzeal.utils.containers.root_container import RootContainer

# adding Any to the Union (effectively rendering it an Any-expression) allows
# the injection of arbitrary objects via Plugins
# TODO: remove Any before release!
tPluggable = Union[Any, FinderAlgorithm, ArgumentEstimator, RootContainer]
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
        Returns a constructor for the plugin's implementation of `T_co`.

        :return: Constructor for plugin implementation of `T_co`.
        """

    @staticmethod
    @abstractmethod
    def getInstance() -> PyZEALPlugin[T_co]:
        """
        Return a `PyZEALPlugin` with type `T_co`.

        :return: `PyZEALPlugin` with type `T_co`.
        """

    @property
    @abstractmethod
    def pluginType(self) -> Type[T_co]:
        """
        Return the type of plugin.

        :return: Type of plugin.
        """
        ...

    @property
    @abstractmethod
    def pluginName(self) -> str:
        """
        Return the plugin name.

        :return: Plugin name
        """
        ...

    @property
    @abstractmethod
    def pluginVersion(self) -> Tuple[int, int, int]:
        """
        Return the plugin version.

        :return: Plugin version
        """
        ...
