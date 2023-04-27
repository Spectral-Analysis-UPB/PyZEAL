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
from signal import SIG_IGN, SIGINT, signal
from typing import List, Optional, Tuple, cast

from numpy import linspace
from rich.progress import TaskID

from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.pyzeal_types.parallel_types import FinderProgressManager, tQueue
from pyzeal.pyzeal_types.root_types import tHoloFunc
from pyzeal.rootfinders.rootfinder import RootFinder
from pyzeal.utils.factories.container_factory import ContainerFactory
from pyzeal.utils.filter_context import FilterContext
from pyzeal.utils.finder_progress import FinderProgressBar
from pyzeal.utils.root_context import RootContext


class ParallelRootFinder(RootFinder):
    """
    Parallel (multiprocessing) implementation of the main root finding API.
    """

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
        Initialize a parallel (multiprocessing) root finder.

        :param f: the function whose roots should be calculated
        :param df: the derivative of `f`
        :param containerType: the type of container found roots are stored in
        :param algorithmType: the type of algorithm used for root finding
        :param precision: the accuracy at which roots are considered exact
        :param numSamplePoints: determines grid size for `NewtonGridAlgorithm`
        :param verbose: flag that toggles the command line progress bar
        """
        # every algorithm invocation uses numSamplePoints on its subgrid!
        numSamplePoints = (
            int(numSamplePoints / (cpu_count() or 1)) + 1
            if numSamplePoints
            else None
        )
        super().__init__(
            f=f,
            df=df,
            containerType=containerType,
            algorithmType=algorithmType,
            estimatorType=estimatorType,
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
            + "df=None)"
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
                numProcesses=cpu_count() or 1,
                reRan=(x1, x2),
                imRan=(y1, y2),
                rootQueue=rootQueue,
                precision=precision,
                progress=progress,
                task=task,
            )

            with Pool(initializer=ParallelRootFinder.suppressSig) as pool:
                # shut down root search orderly upon command line signals
                try:
                    self.logger.info("attempting to calculate roots...")
                    pool.starmap(
                        self.rootWorker,
                        [(context,) for context in contexts],
                        chunksize=cpu_count() or 1,
                    )
                    if progress is not None and task is not None:
                        progress.update(
                            task, description=("[green] search finished!")
                        )
                    self.logger.debug("all child processes returned normally!")
                except KeyboardInterrupt:
                    self.logger.warning(
                        "calculation interrupted - some roots may be missing!"
                    )
                    if progress and task:
                        progress.stop_task(task)
                        progress.update(task, visible=False)
                        progress.refresh()
                if progress is not None and task is not None:
                    progress.stop()

            # add found roots to the current instance's container
            self.logger.debug("transferring roots from queue to container!")
            precision = (precision[0] - 1, precision[1] - 1)
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

        :param numProcesses: The number of processes, which determines the
            amount of contexts that are returned
        :param reRan: Search range for the real part
        :param imRan: Search range for the imaginary part
        :param rootQueue: Queue in which new roots are added
        :param precision: accuracy of search in real and imaginary parts
        :param progress: Progress bar handle
        :param task: TaskID for the progress bar
        :return: List of RootContexts on which child processes can operate
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
                        f=self.f,
                        df=self.df,
                        container=plainContainer,
                        reRan=(realPts[i], realPts[i + 1]),
                        imRan=(imagPts[j], imagPts[j + 1]),
                        precision=precision,
                        progress=progress,
                        task=task,
                    )
                )
        return contexts

    def rootWorker(self, context: RootContext) -> None:
        """
        Worker function that executes a root finding algorithm in a child
        process.

        :param context: Context object on which roots are searched
        """
        self.logger.info("starting root job in pid=%d!", getpid())
        self.algorithm.calcRoots(context)
        self.logger.info("finished root job in pid=%d!", getpid())

    @staticmethod
    def suppressSig() -> None:
        "Initialization routine setting workers to ignore `ctrl+c`."
        signal(SIGINT, SIG_IGN)
