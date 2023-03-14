"""
TODO
"""

from pyzeal.types.container_types import ContainerTypes
from pyzeal.utils.factories.container_factory import ContainerFactory
from pyzeal.utils.filter_context import FilterContext


def testRoundingContainer():
    """
    Test the rounding container implementation.
    """
    container = ContainerFactory.getConcreteContainer(
        containerType=ContainerTypes.ROUNDING_CONTAINER
    )
    filterContext = FilterContext(
        lambda x: (x - 1.23456789) * (x + 1.23456789), (-5, 5), (-5, 5), (3, 3)
    )
    container.addRoot((1.23456789, 0), filterContext)
    assert container.getRoots() == [1.235]
    container.addRoot((1.2345678, 0), filterContext)
    assert container.getRoots() == [1.235]
    filterContext = FilterContext(
        lambda x: (x - 1.23456789) * (x + 1.23456789), (-5, 5), (-5, 5), (5, 5)
    )
    container.addRoot((-1.23456789, 0), filterContext)
    assert container.getRoots() == [-1.23457]
    container.addRoot((1.2345678, 0), filterContext)
    container.removeRoot((-1.23456789, 0))
    assert container.getRoots() == [1.23457]
