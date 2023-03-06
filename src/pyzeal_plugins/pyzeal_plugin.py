"""
Module pyzeal_plugin.py from the package PyZEAL.
TODO

Authors:\n
- Philipp Schuette\n
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Generic, Tuple, Type, TypeVar

tPluggable = object
T = TypeVar("T", bound=tPluggable)


class PyZEALPlugin(ABC, Generic[T]):
    """
    _summary_

    :param ABC: _description_
    :type ABC: _type_
    """

    @staticmethod
    @abstractmethod
    def initialize() -> Callable[..., T]:
        """
        _summary_

        :return: _description_
        :rtype: _type_
        """

    @staticmethod
    @abstractmethod
    def getInstance() -> PyZEALPlugin:
        """
        _summary_

        :return: _description_
        :rtype: _type_
        """

    @property
    @abstractmethod
    def pluginType(self) -> Type[T]:
        """
        _summary_

        :return: _description_
        :rtype: _type_
        """
        ...

    @property
    @abstractmethod
    def pluginName(self) -> str:
        """
        _summary_

        :return: _description_
        :rtype: _type_
        """
        ...

    @property
    @abstractmethod
    def pluginVersion(self) -> Tuple[int, int, int]:
        """
        _summary_

        :return: _description_
        :rtype: _type_
        """
        ...
