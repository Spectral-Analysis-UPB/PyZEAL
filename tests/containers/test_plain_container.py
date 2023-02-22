from pyzeal_types.container_types import ContainerTypes
from pyzeal_utils.filter_context import FilterContext
from pyzeal_utils.pyzeal_factories.container_factory import ContainerFactory


def testPlainContainer():
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
