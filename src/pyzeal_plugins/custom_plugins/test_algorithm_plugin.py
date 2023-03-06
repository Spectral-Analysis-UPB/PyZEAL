from typing import Callable, Optional, Tuple, Type

from pyzeal_algorithms.finder_algorithm import FinderAlgorithm
from pyzeal_plugins.pyzeal_plugin import PyZEALPlugin
from pyzeal_utils.root_context import RootContext


class TestAlgorithm(FinderAlgorithm):
    def calcRoots(self, context: RootContext) -> None:
        raise NotImplementedError("test algorithm has no implementation!")

    def __str__(self) -> str:
        return "a TestObject instance..."


class AlgorithmPlugin(PyZEALPlugin):

    _instance: Optional[PyZEALPlugin] = None

    @staticmethod
    def initialize() -> Callable[..., TestAlgorithm]:
        return lambda: TestAlgorithm()

    @staticmethod
    def getInstance() -> PyZEALPlugin:
        if AlgorithmPlugin._instance is None:
            AlgorithmPlugin._instance = AlgorithmPlugin()
        return AlgorithmPlugin._instance

    @property
    def pluginType(self) -> Type[TestAlgorithm]:
        return TestAlgorithm

    @property
    def pluginName(self) -> str:
        return "MyTestAlgorithm"

    @property
    def pluginVersion(self) -> Tuple[int, int, int]:
        return (22, 1, 0)
