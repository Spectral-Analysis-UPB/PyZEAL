"""
Module test_algorithm_plugin.py from the package PyZEAL.
TODO

Authors:\n
- Philipp Schuette\n
"""

from typing import Callable, Optional, Tuple, Type

from pyzeal_algorithms.finder_algorithm import FinderAlgorithm
from pyzeal_plugins.pyzeal_plugin import PyZEALPlugin
from pyzeal_utils.root_context import RootContext


class TestAlgorithm(FinderAlgorithm):
    "TODO"

    def calcRoots(self, context: RootContext) -> None:
        raise NotImplementedError("test algorithm has no implementation!")

    def __str__(self) -> str:
        return "a TestObject instance..."


class AlgorithmPlugin(PyZEALPlugin[FinderAlgorithm]):
    "TODO"

    _instance: Optional[PyZEALPlugin[FinderAlgorithm]] = None

    @staticmethod
    def initialize() -> Callable[..., FinderAlgorithm]:
        return lambda: TestAlgorithm()

    @staticmethod
    def getInstance() -> PyZEALPlugin[FinderAlgorithm]:
        if AlgorithmPlugin._instance is None:
            AlgorithmPlugin._instance = AlgorithmPlugin()
        return AlgorithmPlugin._instance

    @property
    def pluginType(self) -> Type[FinderAlgorithm]:
        return FinderAlgorithm

    @property
    def pluginName(self) -> str:
        return "MyTestAlgorithm"

    @property
    def pluginVersion(self) -> Tuple[int, int, int]:
        return (22, 1, 0)
