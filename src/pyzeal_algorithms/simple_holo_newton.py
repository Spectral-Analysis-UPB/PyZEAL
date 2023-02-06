"""
Class FinderAlgorithm from the package pyzeal_algorithms.
This module defines a refined version of the `SimpleArgumentAlgorithm`
by supplementing the argument principle with a Newton algorithm once a starting
point has been identified with sufficient accuracy.

Authors:\n
- Philipp Schuette\n
"""

from typing import Tuple, cast

import numpy as np
from scipy.optimize import newton

from pyzeal_algorithms.simple_holo import (
    FOUR_PI,
    TWO_PI,
    SimpleArgumentAlgorithm,
)
from pyzeal_logging.loggable import Loggable
from pyzeal_utils.root_context import RootContext


class SimpleArgumentNewtonAlgorithm(SimpleArgumentAlgorithm, Loggable):
    """
    Class representation of a root finding algorithm combining the phase
    interpretation of the argument principle used in `SimpleArgumentAlgorithm`
    with a number of Newton steps once a sufficient refinement depth has been
    reached.
    """

    def calcRootsRecursion(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        context: RootContext,
    ) -> None:
        """
        TODO
        """
        # calculate difference between right/left and top/bottom
        x1, x2 = reRan
        y1, y2 = imRan
        deltaRe = x2 - x1
        deltaIm = y2 - y1
        # check if the given rectangle contains at least one zero
        phi = self.estimator.calcMoment(
            0, reRan=reRan, imRan=imRan, context=context
        )
        # check if desired accuracy is aquired
        epsReal = 10 ** (-context.precision[0])
        epsImag = 10 ** (-context.precision[1])
        if phi > TWO_PI and deltaRe < epsReal and deltaIm < epsImag:
            SimpleArgumentAlgorithm.getRootFromRectangle(
                x2, x1, y2, y1, phi, context
            )
            return

        # check if the current box contains a simple root
        if TWO_PI < phi < FOUR_PI and deltaRe < 0.1 and deltaIm < 0.1:
            try:
                self.logger.debug(
                    "starting Newton algorithm from %f+%fj", x1, (y1 + y2) / 2
                )
                newZero = newton(
                    func=context.f,
                    x0=x1 + 0.5 * (y1 + y2) * 1j,
                    x1=x2 + 0.5 * (y1 + y2) * 1j,
                    fprime=context.df,
                    maxiter=50,
                    tol=min(epsReal, epsImag),
                )
                # results of scipy.optimize.newton are either numpy arrays
                # (when started on sequences) or floats
                if isinstance(newZero, np.ndarray):
                    for pair in zip(newZero, np.ones_like(newZero, dtype=int)):
                        context.container.addRoot(
                            pair, context.toFilterContext()
                        )
                else:
                    context.container.addRoot(
                        (cast(complex, newZero), 1), context.toFilterContext()
                    )
            except RuntimeError:
                pass
            finally:
                if context.progress is not None and context.task is not None:
                    context.progress.update(
                        context.task, advance=deltaRe * deltaIm
                    )
            return

        self.decideRefinement((x1, x2), (y1, y2), phi, context)
