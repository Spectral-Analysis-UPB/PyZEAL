from typing import Callable, Optional, Tuple, Type

from pyzeal_plugins.pyzeal_plugin import PyZEALPlugin


class TestObject:
    def __str__(self) -> str:
        return "a TestObject instance..."


class TestPlugin(PyZEALPlugin):

    _instance: Optional[PyZEALPlugin] = None

    @staticmethod
    def initialize() -> Callable[..., TestObject]:
        return lambda: TestObject()

    @staticmethod
    def getInstance() -> PyZEALPlugin:
        if TestPlugin._instance is None:
            TestPlugin._instance = TestPlugin()
        return TestPlugin._instance

    @property
    def pluginType(self) -> Type[TestObject]:
        return TestObject

    @property
    def pluginName(self) -> str:
        return "MyTestPlugin"

    @property
    def pluginVersion(self) -> Tuple[int, int, int]:
        return (1, 0, 0)
