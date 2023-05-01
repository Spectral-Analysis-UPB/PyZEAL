"""
Class SimpleArgumentNewtonAlgorithm from the package pyzeal_algorithms.

This module defines a refined version of the `SimpleArgumentAlgorithm` by
supplementing the argument principle with a Newton algorithm once a starting
point has been identified with sufficient accuracy.

Authors:\n
- Philipp Schuette\n
"""

from typing import Tuple, cast

from scipy.optimize import newton  # type: ignore

from pyzeal.algorithms.constants import FOUR_PI, TWO_PI
from pyzeal.algorithms.simple_holo import SimpleArgumentAlgorithm
from pyzeal.utils.root_context import RootContext


class SimpleArgumentNewtonAlgorithm(SimpleArgumentAlgorithm):
    """
    Class representation of a root finding algorithm combining the phase
    interpretation of the argument principle used in `SimpleArgumentAlgorithm`
    with a number of Newton steps once a sufficient refinement depth has been
    reached.
    """

    def decideRefinement(
        self,
        reRan: Tuple[float, float],
        imRan: Tuple[float, float],
        phi: float,
        context: RootContext,
    ) -> None:
        """
        Decide which way the current search area should be subdivided and
        calculate roots in the subdivided areas. The simple strategy consists
        of the choices (1) return, if argument indicates no roots, (2) place
        root in `context.container` if roots present and accuracy attained,
        (3) start Newton algorithm if simple root present and sufficent
        accuracy attained, or (4) subdivide further if multiple roots present
        or attained accuracy insufficient for Newton algorithm.

        :param reRan: Real part of current search Range
        :param imRan: Imaginary part of current search range
        :param phi: Change in argument along the boundary of the current range
        :param context: `RootContext` in which the algorithm operates
        """
        # calculate difference between right/left and top/bottom
        x1, x2 = reRan
        y1, y2 = imRan
        deltaRe = x2 - x1
        deltaIm = y2 - y1

        # check if desired accuracy is aquired
        epsReal = 10 ** (-context.precision[0])
        epsImag = 10 ** (-context.precision[1])
        if phi > TWO_PI and deltaRe < epsReal and deltaIm < epsImag:
            SimpleArgumentAlgorithm.getRootFromRectangle(
                x2, x1, y2, y1, phi, context
            )
            return

        # check if the current box contains a simple root - Newton's algorithm
        # does not perform well enough to start within large rectangles
        if TWO_PI < phi < FOUR_PI and deltaRe < 0.1 and deltaIm < 0.1:
            try:
                self.logger.debug(
                    "starting Newton algorithm from %f+%fj", x1, (y1 + y2) / 2
                )
                newRoot = newton(
                    func=context.f,
                    x0=x1 + 0.5 * (y1 + y2) * 1j,
                    x1=x2 + 0.5 * (y1 + y2) * 1j,
                    fprime=None,
                    maxiter=50,
                    tol=min(epsReal, epsImag),
                )
                context.container.addRoot(
                    (cast(complex, newRoot), 1), context.toFilterContext()
                )
                if context.df is not None:
                    newRoot = newton(
                        func=context.f,
                        x0=(x1 + x2 + 1j * (y1 + y2)) * 0.5,
                        fprime=context.df,
                        maxiter=50,
                        tol=min(epsReal, epsImag),
                    )
                    context.container.addRoot(
                        (cast(complex, newRoot), 1), context.toFilterContext()
                    )
            except RuntimeError:
                pass
            finally:
                if context.progress is not None and context.task is not None:
                    context.progress.update(
                        context.task, advance=deltaRe * deltaIm
                    )
            return

        super().decideRefinement((x1, x2), (y1, y2), phi, context)
