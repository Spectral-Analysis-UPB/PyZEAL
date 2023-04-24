"""
TODO

Authors:\n
- Philipp Schuette\n
"""

from typing import Protocol, runtime_checkable

import pytest

from pyzeal.utils.configuration_exception import InvalidServiceConfiguration
from pyzeal.utils.service_locator import ServiceLocator


# some classes for testing
@runtime_checkable
class FooInterface(Protocol):
    "Interface for test class."

    def method(self) -> None:
        "This does nothing."
        ...


class Foo(FooInterface):
    "Test class."

    def method(self) -> None:
        "Interface implementation."


@pytest.mark.locator
def testRegisterSingleton() -> None:
    "Test singleton registration."
    ServiceLocator.clearConfigurations()
    instance: FooInterface = Foo()

    # try valid registration
    assert ServiceLocator is ServiceLocator.registerAsSingleton(
        FooInterface, instance
    )
    resolvent = ServiceLocator.tryResolve(FooInterface)

    assert resolvent is instance

    # try invalid registration
    with pytest.raises(InvalidServiceConfiguration):
        ServiceLocator.registerAsSingleton(
            FooInterface, 0
        ).registerAsSingleton(FooInterface, Foo())


@pytest.mark.locator
def testRegisterTransient() -> None:
    "Test transient registration."
    ServiceLocator.clearConfigurations()

    # try valid registration
    assert ServiceLocator is ServiceLocator.registerAsTransient(
        FooInterface, Foo
    )
    resolvent1 = ServiceLocator.tryResolve(FooInterface)
    resolvent2 = ServiceLocator.tryResolve(FooInterface)

    assert isinstance(resolvent1, FooInterface)
    assert isinstance(resolvent1, Foo)
    assert isinstance(resolvent2, FooInterface)
    assert isinstance(resolvent2, Foo)

    # check that genuinely new objects were resolved
    assert resolvent1 is not resolvent2


@pytest.mark.locator
def testLocatorSealing() -> None:
    "Test sealing operation on locator."
    ServiceLocator.clearConfigurations()
    ServiceLocator.seal()

    # try valid registration on sealed locator
    with pytest.raises(ValueError):
        ServiceLocator.registerAsSingleton(FooInterface, Foo())

    # try valid registration on sealed locator
    with pytest.raises(ValueError):
        ServiceLocator.registerAsTransient(FooInterface, Foo)

    # try sealing locator twice
    with pytest.raises(ValueError):
        ServiceLocator.seal()


@pytest.mark.locator
def testInvalidConfiguration() -> None:
    "Test if invalid registered configurations raise exceptions."
    ServiceLocator.clearConfigurations()

    # try to resolve a non-existing configuration
    with pytest.raises(InvalidServiceConfiguration):
        ServiceLocator.tryResolve(FooInterface)

    # register an invalid configuration and try to resolve it
    ServiceLocator.registerAsTransient(
        FooInterface, lambda: None  # type: ignore
    )
    with pytest.raises(InvalidServiceConfiguration):
        ServiceLocator.tryResolve(FooInterface)
