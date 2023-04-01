"""
Class FinderAlgorithm from the package pyzeal_algorithms.
This module defines a simple root finding algorithm that works on any
continuously differentiable function by constructing a supporting grid in the
complex plane and starting an ordinary Newton algorithm at these support
points. It is expected that this approach underperforms in compared to
algorithms which fully exploit the holomorphic nature of target functions.

Authors:\n
- Philipp Schuette\n
- Luca Wasmuth\n
"""

from itertools import product
from warnings import filterwarnings

import numpy as np
import scipy as sp  # type: ignore

from pyzeal.algorithms.finder_algorithm import FinderAlgorithm
from pyzeal.pyzeal_types.root_types import tVec
from pyzeal.utils.root_context import RootContext


class NewtonGridAlgorithm(FinderAlgorithm):
    """
    Class representation of a root finding algorithm for holomorphic functions
    based on starting an ordinary Newton algorithm on a grid of support points
    in the complex plane.
    """

    __slots__ = ("numSamplePoints",)

    def __init__(self, numSamplePoints: int = 50) -> None:
        r"""
        Initialize a root finding algorithm which searches for roots using the
        Newton algorithm with starting points on an evenly spaced grid.

        :param numSamplePoints: Number of support points in grid rows/columns.
        """
        self.numSamplePoints = numSamplePoints
        self.logger.debug("initialized a new NewtonGridAlgorithm!")

    def calcRoots(self, context: RootContext) -> None:
        """
        Calculate roots in a given context based on the Newton algorithm on a
        grid of support points in the complex plane.

        :param context: Context in which the algorithm operates.
        """
        self.logger.info(
            "starting newton grid search for %s",
            context.functionDataToString(),
        )
        rePoints = np.linspace(
            context.reRan[0],
            context.reRan[1],
            self.numSamplePoints,
            dtype=np.complex128,
        )
        imPoints = np.linspace(
            context.imRan[0],
            context.imRan[1],
            self.numSamplePoints,
            dtype=np.complex128,
        )
        points = [x + y * 1j for (x, y) in product(rePoints, imPoints)]
        filterwarnings("ignore", ".*some failed to converge")
        try:
            roots: tVec = sp.optimize.newton(context.f, points, context.df)
        except RuntimeError:
            return
        for root in roots:
            # the newton algorithm does not determine root orders - placeholder
            # value can be anything non-positive
            context.container.addRoot((root, 0), context.toFilterContext())
        if context.progress and context.task:
            context.progress.update(
                context.task,
                advance=(
                    (context.reRan[1] - context.reRan[0])
                    * (context.imRan[1] - context.imRan[0])
                ),
            )
