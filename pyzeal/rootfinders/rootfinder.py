"""
Class RootFinder from the package pyzeal.

This module defines an implementation of the main root finding API as defined
by the `RootFinderInterface` protocol. The class implemented here provides only
the most basic context for a root finding strategy, e.g. no support for
multiprocessing.

Authors:\n
- Philipp Schuette\n
"""

from typing import Optional, Tuple

import numpy as np
from numpy.typing import NDArray
from rich.progress import TaskID

from pyzeal.algorithms.finder_algorithm import FinderAlgorithm
from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_logging.loggable import Loggable
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.pyzeal_types.root_types import tHoloFunc, tVec
from pyzeal.pyzeal_types.settings_types import SettingsServicesTypes
from pyzeal.rootfinders.finder_interface import RootFinderInterface
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.containers.root_container import RootContainer
from pyzeal.utils.finder_progress import FinderProgressBar
from pyzeal.utils.root_context import RootContext
from pyzeal.utils.service_locator import ServiceLocator


class RootFinder(RootFinderInterface, Loggable):
    """
    Simple (i.e. non-parallel) implementation of the main root finding API.
    """

    __slots__ = (
        "f",
        "df",
        "algorithm",
        "_container",
        "precision",
        "numSamplePoints",
        "verbose",
    )

    def __init__(
        self,
        f: tHoloFunc,
        df: Optional[tHoloFunc] = None,
        *,
        containerType: ContainerTypes = ContainerTypes.DEFAULT,
        algorithmType: AlgorithmTypes = AlgorithmTypes.DEFAULT,
        estimatorType: EstimatorTypes = EstimatorTypes.DEFAULT,
        precision: Optional[Tuple[int, int]] = None,
        numSamplePoints: Optional[int] = None,
        verbose: Optional[bool] = None,
    ) -> None:
        """
        Initialize a simple, non-parallel root finder.

        :param f: the function whose roots should be calculated
        :param df: the derivative of `f`
        :param containerType: the type of container found roots are stored in
        :param algorithmType: the type of algorithm used for root finding
        :param estimatorType: the type of argument estimator used
        :param precision: the accuracy at which roots are considered exact
        :param numSamplePoints: determines grid size for `NewtonGridAlgorithm`
        :param verbose: flag that toggles the command line progress bar
        """
        self.f = f
        self.df = df
        self.algorithm: FinderAlgorithm = ServiceLocator.tryResolve(
            FinderAlgorithm,
            algoType=algorithmType,
            estimatorType=estimatorType,
            numSamplePoints=numSamplePoints,
        )
        self._container = ServiceLocator.tryResolve(
            RootContainer, containerType=containerType, precision=precision
        )
        self.precision = (
            precision or ServiceLocator.tryResolve(SettingsService).precision
        )

        self.verbose = (
            verbose
            if verbose is not None
            else ServiceLocator.tryResolve(
                SettingsService, settingsType=SettingsServicesTypes.DEFAULT
            ).verbose
        )
        self.logger.debug("initialized the new root finder %s!", str(self))

    def __str__(self) -> str:
        """
        Return a simple string representation of a `RootFinder` instance.
        """
        if self.df is not None:
            return (
                f"RootFinder(f={getattr(self.f, '__name__', '<unnamed>')}, "
                + f"df={getattr(self.df, '__name__', '<unnamed>')})"
            )
        return (
            f"RootFinder(f={getattr(self.f, '__name__', '<unnamed>')}, "
            + "df=None)"
        )

    def calculateRoots(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        precision: Optional[Tuple[int, int]] = None,
    ) -> None:
        """
        Start a (non-parallel) root finding calculation in the rectangle
        `reRan x imRan` up to a number of `precision` significant digits in
        real and imaginary part.

        :param reRan: horizontal extend of the complex region to search in
        :param imRan: vertical extend of the complex region to search in
        :param precision: accuracy of the search in real and imaginary parts
        """
        # if no precision was given, use default precision from constructor
        precision = precision or self.precision
        # if a rounding container is used we must calculate with an additional
        # digit of internal precision to obtain correct results after rounding
        precision = (precision[0] + 1, precision[1] + 1)
        # desymmetrize the input rectangle
        (x1, x2), (y1, y2) = self.desymmetrizeDomain(reRan, imRan, precision)

        # initialize the progress bar
        progress = FinderProgressBar() if self.verbose else None
        task: Optional[TaskID] = None
        if progress is not None:
            task = progress.addTask((x2 - x1) * (y2 - y1))
            progress.start()
            self.logger.debug("starting progress bar...")

        # construct the root finding context
        context = RootContext(
            f=self.f,
            df=self.df,
            container=self.container,
            precision=precision,
            reRan=(x1, x2),
            imRan=(y1, y2),
            progress=progress,
            task=task,
        )
        # shut down root finding in orderly fashion upon command line signals
        try:
            self.logger.info("attempting to calculate roots...")
            self.algorithm.calcRoots(context)
            if progress is not None and task is not None:
                progress.update(task, description="[green] search finished!")
        except KeyboardInterrupt:
            self.logger.warning(
                "root calculation interrupted - some roots may be missing!"
            )
            if progress and task:
                progress.stop_task(task)
                progress.update(task, visible=False)
                progress.refresh()
        if progress is not None and task is not None:
            progress.stop()
        self.logger.info("non-parallel root search finished!")

    @property
    def roots(self) -> tVec:
        """
        Return the roots calculated with this root finder through previous
        calls to `calculateRoots()`.

        :return: the set of roots calculated by this finder
        """
        return self.container.getRoots()

    @property
    def orders(self) -> NDArray[np.int32]:
        """
        Return the orders of the roots calculated with this finder. The output
        is parallel to the return value of the `roots` property.

        :return: the orders of the roots calculated by this finder
        """
        return self.container.getRootOrders()

    def setLevel(self, level: LogLevel) -> None:
        """
        Set the logging level of this `RootFinder` and all dependent objects
        like containers and algorithms.

        :param level: the new logging level
        """
        super().setLevel(level)
        self.container.setLevel(level)
        self.algorithm.setLevel(level)

    @property
    def container(self) -> RootContainer:
        """
        Return the container attached to this rootfinder
        """
        return self._container

    def desymmetrizeDomain(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        precision: Tuple[int, int],
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Desymmetrize the domain to improve numerical stability.

        In practice one notices that target domains as given by `reRan x imRan`
        often contain roots on/near their boundaries if given e.g. in terms of
        integers. This method is automatically called by `calculateRoots` so a
        user does not need to worry about (slightly) perturbing their domains.

        :param reRan: Search range for the real part
        :param imRan: Search range for the imaginary part
        :param precision: Accuracy in real and imaginary part
        :return: New bounds for real and imaginary parts
        """
        (x1, x2), (y1, y2) = sorted(reRan), sorted(imRan)
        x1 = x1 - 1 * 10 ** (-1 * precision[0])
        x2 = x2 + 2 * 10 ** (-1 * precision[0])
        y1 = y1 - 3 * 10 ** (-1 * precision[1])
        y2 = y2 + 4 * 10 ** (-1 * precision[1])
        self.logger.debug(
            "desymmetrized root finding domain to [%f, %f] x [%f, %f]",
            x1,
            x2,
            y1,
            y2,
        )
        return (x1, x2), (y1, y2)
