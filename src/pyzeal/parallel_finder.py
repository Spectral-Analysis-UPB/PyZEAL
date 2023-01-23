"""
Class ParallelRootFinder from the package pyzeal.
This module defines an implementation of the main root finding API as defined
by the `RootFinderInterface` protocol. It differs from `RootFinder` in the fact
that it devides the search region into sub-regions and delegates these to a
number of appropriate algorithms working in parallel. The parallelism is
realized by using the standard library `multiprocessing` module.

Authors:\n
- Philipp Schuette\n
"""

from multiprocessing import Manager, Pool
from os import cpu_count, getpid
from signal import signal, SIG_IGN, SIGINT
from typing import cast, List, Optional, Tuple

from numpy import linspace

from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_types.container_types import ContainerTypes
from pyzeal_types.root_types import tHoloFunc
from pyzeal_types.parallel_types import FinderProgressManager, tQueue
from pyzeal_utils.finder_progress import FinderProgressBar
from pyzeal_utils.root_context import RootContext
from pyzeal_utils.filter_context import FilterContext
from pyzeal_utils.pyzeal_factories.container_factory import ContainerFactory
from pyzeal_logging.logger_facade import PyZEALLogger
from rich.progress import TaskID

from .rootfinder import RootFinder


class ParallelRootFinder(RootFinder):
    """
    Parallel (multiprocessing) implementation of the main root finding API.
    """

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
        Initialize a parallel (multiprocessing) root finder.

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
        super().__init__(
            f=f,
            df=df,
            containerType=containerType,
            algorithmType=algorithmType,
            precision=precision,
            numSamplePoints=numSamplePoints,
            verbose=verbose,
        )

    def __str__(self) -> str:
        "Simple string representation of a `ParallelRootFinder`."
        if self.df is not None:
            return (
                "ParallelRootFinder(f="
                + f"{getattr(self.f, '__name__', '<unnamed>')}, "
                + f"df={getattr(self.df, '__name__', '<unnamed>')})"
            )
        return (
            "ParallelRootFinder(f="
            + f"{getattr(self.f, '__name__', '<unnamed>')}, "
            + "df=None"
        )

    def calculateRoots(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        precision: Optional[Tuple[int, int]] = None,
    ) -> None:
        """
        Parallel implementation of the root finding interface as defined in
        `RootFinderInterface`.

        :param reRan: horizontal extend of the complex region to search in
        :type reRan: Tuple[int, int]
        :param imRan: vertical extend of the complex region to search in
        :type imRan: Tuple[int, int]
        :param precision: accuracy of the search in real and imaginary parts
        :type precision: Tuple[int, int]
        """
        # if no precision was given, use default precision from constructor
        precision = self.precision if precision is None else precision
        # desymmetrize the input rectangle
        (x1, x2), (y1, y2) = self.desymmetrizeDomain(reRan, imRan, precision)

        # initialize a shared progress bar
        FinderProgressManager.register("finderProgress", FinderProgressBar)
        with FinderProgressManager() as manager:
            progress = manager.finderProgress() if self.verbose else None
            task: Optional[TaskID] = None
            if progress is not None:
                task = progress.addTask((x2 - x1) * (y2 - y1))
                progress.start()
                self.logger.debug("starting progress bar...")

            # construct a list of root contexts, several for each child process
            rootQueue: tQueue = cast(tQueue, Manager().Queue())
            contexts = self.createRootJobs(
                cpu_count() or 1,
                (x1, x2),
                (y1, y2),
                rootQueue,
                precision,
                progress,
                task,
            )

            with Pool(initializer=lambda: signal(SIGINT, SIG_IGN)) as pool:
                # shut down root finding orderly upon command line signals
                try:
                    self.logger.info("attempting to calculate roots...")
                    pool.starmap(
                        self.rootWorker,
                        [(context, self.logger) for context in contexts],
                        chunksize=cpu_count() or 1,
                    )
                    if progress is not None and task is not None:
                        progress.update(
                            task, description=("[green] search finished!")
                        )
                    self.logger.debug("all child processes returned normally!")
                except KeyboardInterrupt:
                    self.logger.warning(
                        "root calculation interrupted \
                        - some roots may be missing!"
                    )
                    if progress and task:
                        progress.stop_task(task)
                        progress.update(task, visible=False)
                        progress.refresh()
                if progress is not None and task is not None:
                    progress.stop()

            # add found roots to the current instance's container
            self.logger.debug("transferring roots from queue to container!")
            while not rootQueue.empty():
                self.container.addRoot(
                    rootQueue.get(),
                    FilterContext(self.f, (x1, x2), (y1, y2), precision),
                )
            self.logger.info("parallel root search finished!")

    def createRootJobs(
        self,
        numProcesses: int,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        rootQueue: tQueue,
        precision: Tuple[int, int],
        progress: Optional[FinderProgressBar],
        task: Optional[TaskID],
    ) -> List[RootContext]:
        """
        Convenience method that constructs a list of RootContext objects on
        which child processes operate by applying a concrete RootAlgorithm.

        TODO
        """
        self.logger.debug(
            "initializing context jobs for %d child processes...", numProcesses
        )
        realPts = linspace(reRan[0], reRan[1], numProcesses + 1)
        imagPts = linspace(imRan[0], imRan[1], numProcesses + 1)
        plainContainer = ContainerFactory.getConcreteContainer(
            ContainerTypes.PLAIN_CONTAINER, queue=rootQueue
        )
        contexts: List[RootContext] = []
        for i in range(len(realPts) - 1):
            for j in range(len(imagPts) - 1):
                contexts.append(
                    RootContext(
                        self.f,
                        self.df,
                        plainContainer,
                        (realPts[i], realPts[i + 1]),
                        (imagPts[j], imagPts[j + 1]),
                        precision,
                        progress,
                        task,
                    )
                )
        return contexts

    def rootWorker(self, context: RootContext, logger: PyZEALLogger) -> None:
        """
        Worker function that executes a root finding algorithm in a child
        process.

        TODO
        """
        self.logger.info("starting root job in pid=%d!", getpid())
        self.algorithm.calcRoots(context)
        self.logger.info("finished root job in pid=%d!", getpid())
