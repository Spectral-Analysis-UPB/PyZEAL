"""
Module pyzeal_plugin.py from the package PyZEAL.
TODO

Authors:\n
- Philipp Schuette\n
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Tuple, Type, TypeVar, Union

from pyzeal_algorithms.finder_algorithm import FinderAlgorithm
from pyzeal_algorithms.pyzeal_estimators.argument_estimator import (
    ArgumentEstimator,
)
from pyzeal_utils.pyzeal_containers.root_container import RootContainer

# adding Any to the Union (effectively rendering it an Any-expression) allows
# the injection of arbitrary objects via Plugins
# TODO: remove Any before release!
tPluggable = Union[Any, FinderAlgorithm, ArgumentEstimator, RootContainer]
T_co = TypeVar("T_co", bound=tPluggable, covariant=True)


class PyZEALPlugin(ABC, Generic[T_co]):
    """
    _summary_

    :param ABC: _description_
    :type ABC: _type_
    """

    @staticmethod
    @abstractmethod
    def initialize() -> Callable[..., T_co]:
        """
        _summary_

        :return: _description_
        :rtype: _type_
        """

    @staticmethod
    @abstractmethod
    def getInstance() -> PyZEALPlugin[T_co]:
        """
        _summary_

        :return: _description_
        :rtype: _type_
        """

    @property
    @abstractmethod
    def pluginType(self) -> Type[T_co]:
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
