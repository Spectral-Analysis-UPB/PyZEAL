"""
TODO.

Authors:\n
- Philipp\
"""

from typing import Protocol, Union, runtime_checkable

from pytest import ExitCode


@runtime_checkable
class InstallTestingHandlerFacade(Protocol):
    """
    An interface for a simple helper that handles testing of local
    installations.
    """

    def testModule(self, module: str) -> Union[int, ExitCode]:
        """
        Test a given module of the local `PyZEAL` installation.

        :param module: path to the module under test
        :return: exit status of the test conducted
        """
        ...
