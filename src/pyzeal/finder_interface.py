"""
Module rootfinder of the pyzeal package.
This module contains the base interface for all rootfinder implementations.

Authors:\n
- Philipp Schuette\n
"""

import logging
from abc import ABC, abstractmethod
from multiprocessing import Manager, Pool
from os import cpu_count, getpid
from signal import SIG_IGN, SIGINT, signal
from typing import Final, List, Tuple, cast, Optional

from numpy import complex128, linspace
from numpy.typing import NDArray
from rich.progress import Progress, SpinnerColumn, TaskID, TimeElapsedColumn
from pyzeal_types.root_types import MyManager, tQueue

####################
# Global Constants #
####################

CPU_COUNT: Final[int] = cpu_count() or 1


#################################
# Abstract Base for Root Finder #
#################################


class RootFinder(ABC):
    r"""
    Base interface for class implementations of root finding algorithms.
    """

    def calcRoots(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        precision: Tuple[int, int],
    ) -> None:
        r"""
        Calculate roots in the rectangle `reRan x imRan` up to accurancy
        `precision` in real and imaginary part.

        :param reRan: boundaries of calculation rectangle in real direction
        :type reRan: Tuple[float, float]
        :param imRan: boundaries of calculation rectangle in imaginary
            direction
        :type imRan: Tuple[float, float]
        :param precision: accuracy of root calculation in real and imaginary
            directions in terms of decimal places
        :type precision: Tuple[int, int]
        """
        # initialize list of root calculation sub-tasks
        rootJobs: List[
            Tuple[
                Tuple[float, float],
                Tuple[float, float],
                tQueue,
                Progress,
                TaskID,
                Tuple[int, int],
            ]
        ] = []
        # initialize result queue for subprocesses to put results into
        resultQueue: tQueue = cast(tQueue, Manager().Queue())

        # generate initial array on rectangle
        x1, x2 = sorted(reRan)
        y1, y2 = sorted(imRan)
        # 'desymmetrize' initial array to improve numerical stability
        x1, x2 = x1 - 10 ** (-1 * precision[0]), x2 + 10 ** (-1 * precision[0])
        y1, y2 = y1 - 10 ** (-1 * precision[1]), y2 + 10 ** (-1 * precision[1])
        recNum: Final[int] = 1
        imagPts: NDArray = linspace(y1, y2, num=recNum * CPU_COUNT + 1)
        self.logger.info(
            f"Calculating roots in [{reRan[0]}, {reRan[1]}]\
             x [{imRan[0]}, {imRan[1]}]"
        )
        MyManager.register("progress", Progress)
        with MyManager() as manager:
            manager = cast(MyManager, manager)
            progress = manager.progress(
                *Progress.get_default_columns()[:],
                SpinnerColumn(),
                "Elapsed:",
                TimeElapsedColumn(),
                transient=False,
                refresh_per_second=3,
                speed_estimate_period=10,
                expand=True,
            )
            total = (x2 - x1) * (y2 - y1)
            task = progress.add_task(
                (f"[magenta]{getpid()}: " + "[g]getting roots..."),
                total=total,
            )
            progress.start()
            for i in range(recNum * CPU_COUNT):
                rootJobs.append(
                    (
                        (x1, x2),
                        (float(imagPts[i]), float(imagPts[i + 1])),
                        resultQueue,
                        progress,
                        task,
                        precision,
                    )
                )
            self.logger.info("Using %d total jobs", len(rootJobs))
            # calculate roots in parallel using the concrete algorithm
            # implemented in `runRootJobs`
            with Pool(
                processes=CPU_COUNT, initializer=RootFinder.suppressSig()
            ) as p:
                try:
                    p.starmap(self.runRootJobs, rootJobs, chunksize=recNum)
                    progress.update(
                        task,
                        description=("[green]finished" + " calculation..."),
                    )
                except KeyboardInterrupt:
                    progress.stop_task(task)
                    progress.update(task, visible=False)
                    progress.refresh()
                    p.terminate()
                    p.join()
            progress.stop()

        # append new roots to previously calculated roots
        if resultQueue.empty():
            self.addRoot(None)
        while not resultQueue.empty():
            self.addRoot(resultQueue.get())

    @abstractmethod
    def runRootJobs(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        resultQueue: tQueue,
        progress: Progress,
        task: TaskID,
        precision: Tuple[int, int],
    ) -> None:
        r"""
        Method template to overwrite during implemention of concrete root
        finding algorithms. New roots must be added by putting them into
        `resultQueue` and `progress` must be updated accordingly.
        """

    @abstractmethod
    def getRoots(self) -> NDArray[complex128]:
        r"""
        Return roots previously calculated using `.calcRoots()` as an ndarray.

        :return: array of complex roots calculated previously
        :rtype: numpy.ndarray[complex128]
        """

    @abstractmethod
    def addRoot(self, newRoot: Optional[Tuple[complex, int]]) -> None:
        r"""
        Method template to overwrite during implementation of concrete root
        finding algorithms. This method must contain the logic that handles
        duplicate roots, differing orders of duplicates roots, etc.

        If an algorithm does not supply zero orders put order=0 by convention!
        """

    @property
    @abstractmethod
    def logger(self) -> logging.Logger:
        """Subclasses need to provide a logger.

        :return: Initizialized logger from pyzeal_logging.init_logger
        :rtype: logging.Logger
        """

    @staticmethod
    def suppressSig() -> None:
        "Initialization routine setting workers to ignore `ctrl+c`."
        signal(SIGINT, SIG_IGN)
