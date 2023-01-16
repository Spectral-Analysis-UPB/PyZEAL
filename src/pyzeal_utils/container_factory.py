"""
This module provides a static factory class which maps the containers available
in the `ContainerTypes` enumeration to appropriate implementations of the
interface `RootContainer`.

Authors:\n
- Philipp Schuette\n
"""

from typing import Tuple, cast

import numpy as np

from pyzeal_logging.config import initLogger
from pyzeal_logging.log_levels import LogLevel
from pyzeal_types.container_types import ContainerTypes
from pyzeal_types.filter_types import FilterTypes
from pyzeal_utils.root_container import RootContainer
from pyzeal_utils.rounding_container import RoundingContainer


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
        # TODO: implement configuration mechanism for default container
        ContainerFactory.logger.debug("requested a new default container...")
        return RoundingContainer(precision)

    @staticmethod
    def registerPreDefinedFilter(
        container: RootContainer,
        filterType: FilterTypes,
        *,
        threshold: int = 3,
    ) -> None:
        """
        Given a container instance this method adds a filter to its addRoot()
        method. The filter checks if the root satisfies some given condition in
        a concrete `FilterContext` and discards the root otherwise.

        :param container: the container which receives a new filter
        :type container: RootContainer
        :param filterType: one of the predefined filters
        :type filterType: FilterTypes
        :param threshold: the threshold for evaluation of `f` on roots
        :type threshold: int
        :return: the enhanced container
        :rtype: RootContainer
        """
        if filterType == FilterTypes.FUNCTION_VALUE_ZERO:
            container.registerFilter(
                lambda root, context: (
                    cast(
                        bool,
                        np.abs(
                            context.f(
                                np.array(
                                    [
                                        root[0],
                                    ],
                                    dtype=np.complex128,
                                )
                            )
                        )
                        < 10 ** (-threshold),
                    )
                ),
                filterType.value,
            )
        elif filterType == FilterTypes.ZERO_IN_BOUNDS:
            container.registerFilter(
                lambda root, context: (
                    context.reRan[0] <= root[0].real <= context.reRan[1]
                    and context.imRan[0] <= root[0].imag <= context.imRan[1]
                ),
                filterType.value,
            )

        ContainerFactory.logger.debug(
            "registered a new %s filter!", filterType.value
        )

    @staticmethod
    def setLevel(level: LogLevel) -> None:
        """
        Set the log level.

        :param level: the new log level
        :type level: pyzeal_logging.log_levels.LogLevel
        """
        ContainerFactory.logger.setLevel(level=level.value)
