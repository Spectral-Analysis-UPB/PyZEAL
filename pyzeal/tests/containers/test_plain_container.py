"""
TODO
"""

from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.utils.factories.container_factory import ContainerFactory
from pyzeal.utils.filter_context import FilterContext


def testPlainContainer() -> None:
    """
    Test the plain container implementation.
    """
    container = ContainerFactory.getConcreteContainer(
        containerType=ContainerTypes.PLAIN_CONTAINER
    )
    filterContext = FilterContext(
        lambda x: (x - 1.23456789) * (x + 1.23456789), (-5, 5), (-5, 5), (3, 3)
    )
    container.addRoot((1.23456789, 0), filterContext)
    assert container.getRoots() == [1.23456789]
    container.addRoot((1.2345678, 0), filterContext)
    assert (container.getRoots() == [1.23456789, 1.2345678]).all()
    container.addRoot((-1.23456789, 0), filterContext)
    assert (container.getRoots() == [1.23456789, 1.2345678, -1.23456789]).all()
