"""
This module contains tests for the plain container implementation.
"""

from typing import List

import numpy as np

from pyzeal.utils.containers.root_container import RootContainer
from pyzeal.utils.filter_context import FilterContext


def testAddPlainContainer(
    roundingContainer: RootContainer, filterContexts: List[FilterContext]
) -> None:
    """
    Test the plain container `addRoot` implementation.
    """
    assert len(roundingContainer.getRoots()) == 0
    # filter contexts differ in precision, effectively clearing container
    for filterContext in filterContexts:
        roundingContainer.addRoot((1.23456789, 1), filterContext)
        assert len(roundingContainer.getRoots()) == 1

        # root should be rejected due to equality
        roundingContainer.addRoot((1.2345678, 1), filterContext)
        assert len(roundingContainer.getRoots()) == 1

        roundingContainer.addRoot((-1.23456789, 2), filterContext)
        assert len(roundingContainer.getRoots()) == 2

        # root should not be rejected due to inequality of orders
        roundingContainer.addRoot((1.2345678, 2), filterContext)
        assert len(roundingContainer.getRoots()) == 3

    containerContents = np.sort(roundingContainer.getRoots())
    assert (containerContents == [-1.235, 1.235, 1.235]).all()


def testRemovePlainContainer(
    roundingContainer: RootContainer, filterContexts: List[FilterContext]
) -> None:
    """
    Test the plain container `removeRoot` implementation.
    """
    roundingContainer.addRoot((0, 1), filterContexts[0])
    roundingContainer.addRoot((1, 1), filterContexts[0])

    assert len(roundingContainer.getRoots()) == 2
    assert not roundingContainer.removeRoot((-1, 1))
    assert roundingContainer.removeRoot((0, 1))
    assert len(roundingContainer.getRoots()) == 1
    assert roundingContainer.removeRoot((1, 1))
    assert len(roundingContainer.getRoots()) == 0
    assert not roundingContainer.removeRoot((0, 1))


def testClearPlainContainer(
    roundingContainer: RootContainer, filterContexts: List[FilterContext]
) -> None:
    """
    Test the plain container `clear` implementation.
    """
    roundingContainer.addRoot((0, 1), filterContexts[0])
    roundingContainer.addRoot((-2, 1), filterContexts[0])

    assert len(roundingContainer.getRoots()) == 2
    roundingContainer.clear()
    assert len(roundingContainer.getRoots()) == 0


def testRegisterUnregisterFilterPlainContainer(
    roundingContainer: RootContainer, filterContexts: List[FilterContext]
) -> None:
    """
    Test the plain container `registerFilter` implementation.
    """
    roundingContainer.registerFilter(lambda r, c: False, "alwaysFalse")
    roundingContainer.addRoot((1j, 0), filterContexts[0])
    assert len(roundingContainer.getRoots()) == 0

    roundingContainer.unregisterFilter("alwaysFalse")
    roundingContainer.addRoot((1j, 0), filterContexts[0])
    assert len(roundingContainer.getRoots()) == 1
