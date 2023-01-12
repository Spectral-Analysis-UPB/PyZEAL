"""
This module provides a static factory class which maps the containers available
in the `ContainerTypes` enumeration to appropriate implementations of the
interface `RootContainer`.

Authors:\n
- Philipp Schuette\n
"""

from typing import cast, Tuple

from pyzeal_types.container_types import ContainerTypes
from pyzeal_types.root_types import tHoloFunc
from pyzeal_utils.root_container import RootContainer
from pyzeal_utils.rounding_container import RoundingContainer
from pyzeal_logging.config import initLogger


class ContainerFactory:
    "Static factory class used to create instances of root containers."

    # initialize the module level logger
    logger = initLogger(__name__.rsplit(".", maxsplit=1)[-1])

    @staticmethod
    def getConcreteContainer(
        containerType: ContainerTypes, *, precision: Tuple[int, int] = (3, 3)
    ) -> RootContainer:
        """
        Initialize and return a root container instance based on the given type
        `algoType` of container and a given accuracy in real and imaginary
        parts.

        :param containerType: type of container to construct
        :type containerType: ContainerTypes
        :param precision: the accuracy of the given container
        :type precision: Tuple[int, int]
        """
        if containerType == ContainerTypes.ROUNDING_CONTAINER:
            ContainerFactory.logger.debug(
                "requested a new rounding container..."
            )
            return RoundingContainer(precision)
        else:
            # TODO: implement configuration mechanism for default containers
            ContainerFactory.logger.debug(
                "requested a new default container..."
            )
            return RoundingContainer(precision)

    @staticmethod
    def registerFunctionValueIsZeroFilter(
        container: RootContainer, f: tHoloFunc, threshold: int = 1
    ) -> None:
        """
        Given a container instance this method adds a filter to its addRoot()
        method. The filter checks if the root to be added yields a sufficiently
        small value upon function evaluation and discards the root otherwise.

        :param container: the container which receives a new filter
        :type container: RootContainer
        :param f: the function which the roots belong to
        :type f: Callable[[complex], complex]
        :param threshold: the threshold for evaluation of `f` on roots
        :type threshold: int
        :return: the enhanced container
        :rtype: RootContainer
        """
        container.registerFilter(
            lambda root: cast(bool, abs(f(root[0])) < 10 ** (-threshold))
        )
        ContainerFactory.logger.debug(
            "registered a new [function-value-zero] filter!"
        )

    @staticmethod
    def registerZeroIsInBoundsFilter(
        container: RootContainer,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
    ) -> None:
        """
        Given a container instance this method adds a filter to its addRoot()
        method. The filter checks if the root to be added yields a value that
        is contained within a specified rectangular region. Otherwise the
        candidate gets discarded.

        :param container: the container which receives a new filter
        :type container: RootContainer
        :param reRan: the horizontal extend of the confinement (test-)region
        :type reRan: Tuple[float, float]
        :param imRan: the vertical extend of the confinement (test-)region
        :type imRan: Tuple[float, float]
        :param threshold: the threshold for evaluation of `f` on roots
        :type threshold: int
        :return: the enhanced container
        :rtype: RootContainer
        """
        container.registerFilter(
            lambda root: (
                reRan[0] <= root[0].real <= reRan[1]
                and imRan[0] <= root[0].imag <= imRan[1]
            )
        )
        ContainerFactory.logger.debug(
            "registered a new [zero-in-bounds] filter!"
        )
