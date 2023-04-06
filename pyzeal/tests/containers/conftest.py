"""
Testing fixtures for the `RootContainer` tests.
"""

from typing import List

import pytest

from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.utils.containers.root_container import RootContainer
from pyzeal.utils.factories.container_factory import ContainerFactory
from pyzeal.utils.filter_context import FilterContext


@pytest.fixture(name="filterContexts")
def fixtureFilterContexts() -> List[FilterContext]:
    "Fixture providing a list of `FilterContext` instances."
    fContext1 = FilterContext(
        lambda x: (x - 1.23456789) * (x + 1.23456789), (-5, 5), (-5, 5), (3, 3)
    )
    fContext2 = FilterContext(lambda x: x + 1, (-1, 2), (-3, 4), (5, 6))
    return [fContext1, fContext2, fContext1]


@pytest.fixture(name="plainContainer")
def fixturePlainContainer() -> RootContainer:
    "Fixture providing a `PlainContainer` instance."
    container = ContainerFactory.getConcreteContainer(
        containerType=ContainerTypes.PLAIN_CONTAINER
    )
    return container


@pytest.fixture(name="roundingContainer")
def fixtureRoundingContainer() -> RootContainer:
    "Fixture providing a `PlainContainer` instance."
    container = ContainerFactory.getConcreteContainer(
        containerType=ContainerTypes.ROUNDING_CONTAINER
    )
    return container
