"""
TODO

Authors:\n
- Philipp Schuette\n
"""

from os import chdir
from os.path import dirname, join, realpath
from typing import Union

import pytest

from pyzeal.utils.install_test_facade import InstallTestingHandlerFacade


class InstallTestingHandler(InstallTestingHandlerFacade):
    "Concrete implementation of the `TestingHandlerFacade` interface."

    def __init__(self) -> None:
        "Initialize a new `TestingHandler` instance."

    # docstr-coverage:inherited
    def testModule(self, module: str) -> Union[int, pytest.ExitCode]:
        # change to the directory just above the tests/ directory
        chdir(dirname(realpath(__file__)))
        chdir("..")
        # obtain the full path to the module under test
        path = join("tests", module)
        # test the given module
        return pytest.main([path])
