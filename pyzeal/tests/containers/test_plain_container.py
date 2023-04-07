"""
This module contains tests for the plain container implementation.
"""

from typing import List

import pytest

from pyzeal.utils.containers.root_container import RootContainer
from pyzeal.utils.filter_context import FilterContext


def testAddPlainContainer(
    plainContainer: RootContainer, filterContexts: List[FilterContext]
) -> None:
    """
    Test the plain container `addRoot` implementation.
    """
    i = 0
    for filterContext in filterContexts:
        assert len(plainContainer.getRoots()) == 3 * i

        plainContainer.addRoot((1.23456789, 0), filterContext)
        assert len(plainContainer.getRoots()) == 3 * i + 1

        plainContainer.addRoot((1.2345678, -1), filterContext)
        assert len(plainContainer.getRoots()) == 3 * i + 2

        plainContainer.addRoot((-1.23456789, 2), filterContext)
        assert len(plainContainer.getRoots()) == 3 * i + 3

        i += 1

    assert (
        plainContainer.getRoots() == [1.23456789, 1.2345678, -1.23456789] * 3
    ).all()


def testRemovePlainContainer(
    plainContainer: RootContainer, filterContexts: List[FilterContext]
) -> None:
    """
    Test the plain container `removeRoot` implementation.
    """
    plainContainer.addRoot((0, 1), filterContexts[0])
    plainContainer.addRoot((0, 1), filterContexts[0])

    assert len(plainContainer.getRoots()) == 2
    assert not plainContainer.removeRoot((0, 1))
    assert len(plainContainer.getRoots()) == 2


def testClearPlainContainer(
    plainContainer: RootContainer, filterContexts: List[FilterContext]
) -> None:
    """
    Test the plain container `clear` implementation.
    """
    plainContainer.addRoot((0, 1), filterContexts[0])
    plainContainer.addRoot((0, 1), filterContexts[0])

    assert len(plainContainer.getRoots()) == 2
    with pytest.raises(NotImplementedError):
        plainContainer.clear()
    assert len(plainContainer.getRoots()) == 2


def testRegisterUnregisterFilterPlainContainer(
    plainContainer: RootContainer,
) -> None:
    """
    Test the plain container `registerFilter` implementation.
    """
    with pytest.raises(NotImplementedError):
        plainContainer.registerFilter(lambda r, c: False, "alwaysFalse")
    with pytest.raises(NotImplementedError):
        plainContainer.unregisterFilter("alwaysFalse")
