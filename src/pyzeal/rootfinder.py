"""
Class RootFinder from the package pyzeal.
This module defines an implementation of the main root finding API as defined
by the `RootFinderInterface` protocol. The class implemented here provides only
the most basic context for a root finding strategy, i.e. no multiprocessing.

Authors:\n
- Philipp Schuette\n
"""

from typing import Optional, Tuple

import numpy as np
from numpy.typing import NDArray
from pyzeal_logging.log_levels import LogLevel
from pyzeal_logging.loggable import Loggable
from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_types.container_types import ContainerTypes
from pyzeal_types.root_types import tHoloFunc, tVec
from pyzeal_utils.algorithm_factory import AlgorithmFactory
from pyzeal_utils.container_factory import ContainerFactory
from pyzeal_utils.finder_progress import FinderProgressBar
from pyzeal_utils.root_container import RootContainer
from pyzeal_utils.root_context import RootContext
from rich.progress import TaskID

from pyzeal.finder_interface import RootFinderInterface


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
        "precision",
    )

    def __init__(
        self,
        f: tHoloFunc,
        df: Optional[tHoloFunc] = None,
        *,
        containerType: ContainerTypes = ContainerTypes.ROUNDING_CONTAINER,
        algorithmType: AlgorithmTypes = AlgorithmTypes.NEWTON_GRID,
        precision: Tuple[int, int] = (3, 3),
        numSamplePoints: Optional[int] = None,
        verbose: bool = True,
    ) -> None:
        """
        Initialize a simple, non-parallel root finder.

        :param f: the function whose roots should be calculated
        :type f: Callable[[comlex], complex]
        :param df: the derivative of `f`
        :type df: Optional[Callable[[complex], complex]]
        :param containerType: the type of container found roots are stored in
        :type containerType: ContainerTypes
        :param algorithmType: the type of algorithm used for root finding
        :type algorithmType: AlgorithmTypes
        :param precision: the accuracy at which roots are considered exact
        :type precision: Tuple[int, int]
        :param numSamplePoints: determines grid size for `NewtonGridAlgorithm`
        :type numSamplePoints: Optional[int]
        :param verbose: flag that toggles the command line progress bar
        :type verbose: bool
        """
        self.f = f
        self.df = df
        self.algorithm = AlgorithmFactory.getConcreteAlgorithm(
            algorithmType, numSamplePoints=numSamplePoints
        )
        self._container = ContainerFactory.getConcreteContainer(
            containerType, precision=precision
        )
        self.precision = precision
        self.verbose = verbose
        self.logger.debug(
            "initialized the root finder %s!", str(self)
        )

    def __str__(self) -> str:
        "Simple string representation of a `RootFinder`."
        if self.df is not None:
            return (
                f"RootFinder(f={getattr(self.f, '__name__', '<unnamed>')}, "
                + f"df={getattr(self.df, '__name__', '<unnamed>')})"
            )
        return (
            f"RootFinder(f={getattr(self.f, '__name__', '<unnamed>')}, "
            + "df=None"
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
        :type reRan: Tuple[int, int]
        :param imRan: vertical extend of the complex region to search in
        :type imRan: Tuple[int, int]
        :param precision: accuracy of the search in real and imaginary parts
        :type precision: Optional[Tuple[int, int]]
        """
        # if no precision was given, use default precision from constructor
        precision = self.precision if precision is None else precision
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
            self.f,
            self.df,
            self.container,
            (x1, x2),
            (y1, y2),
            precision,
            progress,
            task,
        )
        # shut down root finding in orderly fashion upon command line signals
        try:
            self.logger.info("attempting to calculate roots...")
            self.algorithm.calcRoots(context)
            if progress is not None and task is not None:
                progress.update(task, description=("[green] search finished!"))
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

    @property
    def roots(self) -> tVec:
        """
        Return the roots calculated with this root finder through previous
        calls to `calculateRoots()`.

        :return: the set of roots calculated by this finder
        :rtype: NDArray[np.complex128]
        """
        return self.container.getRoots()

    @property
    def orders(self) -> NDArray[np.int32]:
        """
        Return the orders of the roots calculated with this finder. The output
        is parallel to the return value of the `roots` property.

        :return: the orders of the roots calculated by this finder
        :rtype: NDArray[np.int32]
        """
        return self.container.getRootOrders()

    def setLevel(self, level: LogLevel) -> None:
        """
        Set the logging level of this `RootFinder` and all dependent objects
        like containers and algorithms.

        :param level: the new logging level
        :type level: pyzeal_logging.log_levels.LogLevel
        """
        super().setLevel(level)
        self.container.setLevel(level)
        self.algorithm.setLevel(level)

    @property
    def container(self) -> RootContainer:
        """
        TODO
        """
        return self._container

    @container.setter
    def container(self, value: RootContainer) -> None:
        self._container = value

    def desymmetrizeDomain(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        precision: Tuple[int, int]
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        TODO
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
