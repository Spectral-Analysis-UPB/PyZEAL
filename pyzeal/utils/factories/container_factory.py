"""
This module provides a static factory class which maps the containers available
in the `ContainerTypes` enumeration to appropriate implementations of the
interface `RootContainer`.

Authors:\n
- Philipp Schuette\n
"""

from functools import partial
from typing import Callable, Optional, Tuple, cast

import numpy as np

from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_logging.log_manager import LogManager
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.filter_types import FilterTypes
from pyzeal.pyzeal_types.parallel_types import tQueue
from pyzeal.pyzeal_types.root_types import tRoot
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.containers.plain_container import PlainContainer
from pyzeal.utils.containers.root_container import RootContainer
from pyzeal.utils.containers.rounding_container import RoundingContainer
from pyzeal.utils.filter_context import FilterContext
from pyzeal.utils.service_locator import ServiceLocator


class ContainerFactory:
    "Static factory class used to create instances of root containers."

    # initialize the module level logger
    logger = LogManager.initLogger(__name__.rsplit(".", maxsplit=1)[-1])

    @staticmethod
    def _func_value_zero(
        threshold: int, root: tRoot, context: FilterContext
    ) -> bool:
        """
        Filter predicate to determine if a possible root has a function
        value sufficiently close to zero

        :param threshold: A function is considered zero if its absolute value
            is below 10^-(threshold)
        :param root: Root candidate
        :param context: Context containing information about the search
        :return: `True` if the function is close enough to zero
        """
        return cast(
            bool,
            np.abs(context.f(np.array([root[0]], dtype=np.complex128)))
            < 10 ** (-threshold),
        )

    @staticmethod
    def _zero_in_bounds(root: tRoot, context: FilterContext) -> bool:
        """
        Filter predicate to determine if `root` is in bounds for `context`.

        :param root: Root to filter
        :param context: Context containing information about the search
        :return: `True` if root is in bounds
        """
        return (
            context.reRan[0] <= root[0].real <= context.reRan[1]
            and context.imRan[0] <= root[0].imag <= context.imRan[1]
        )

    @staticmethod
    def getConcreteContainer(
        containerType: ContainerTypes = ContainerTypes.DEFAULT,
        *,
        precision: Tuple[int, int] = (3, 3),
        queue: Optional[tQueue] = None,
    ) -> RootContainer:
        """
        Initialize and return a root container instance based on the given type
        `algoType` of container and a given accuracy in real and imaginary
        parts.

        :param containerType: type of container to construct
        :param precision: the accuracy of the given container
        :param queue: an existing queue instance as base for a plain container
        :return: a concrete `RootContainer` instance
        """
        if containerType == ContainerTypes.ROUNDING_CONTAINER:
            ContainerFactory.logger.debug(
                "requested a new rounding container..."
            )
            return RoundingContainer(precision)
        if containerType == ContainerTypes.PLAIN_CONTAINER:
            ContainerFactory.logger.debug("requested a new plain container...")
            return PlainContainer(queue)

        # return the current default container
        ContainerFactory.logger.debug("requested a new default container...")
        settings = ServiceLocator.tryResolve(SettingsService)
        return ContainerFactory.getConcreteContainer(
            settings.defaultContainer,
            precision=precision,
            queue=queue,
        )

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
        :param filterType: one of the predefined filters
        :param threshold: the threshold for evaluation of `f` on roots
        :return: the enhanced container
        """
        predicate: Callable[[tRoot, FilterContext], bool]
        if filterType == FilterTypes.FUNCTION_VALUE_ZERO:
            predicate = partial(ContainerFactory._func_value_zero, threshold)
        elif filterType == FilterTypes.ZERO_IN_BOUNDS:
            predicate = ContainerFactory._zero_in_bounds

        container.registerFilter(predicate, filterType.value)
        ContainerFactory.logger.debug(
            "registered a new %s filter!", filterType.value
        )

    @staticmethod
    def setLevel(level: LogLevel) -> None:
        """
        Set the log level.

        :param level: the new log level
        """
        ContainerFactory.logger.setLevel(level=level.value)
