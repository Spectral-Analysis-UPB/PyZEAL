"""
Class FinderAlgorithm from the package pyzeal_algorithms.
This module defines a refined version of the `SimpleArgumentAlgorithm`
by supplementing the argument principle with a Newton algorithm once a starting
point has been identified with sufficient accuracy.

Authors:\n
- Philipp Schuette\n
"""

from typing import cast

import numpy as np
from scipy.optimize import newton

from pyzeal_algorithms.simple_holo import (
    FOUR_PI,
    TWO_PI,
    SimpleArgumentAlgorithm,
)
from pyzeal_logging.loggable import Loggable
from pyzeal_types.root_types import tRecGrid
from pyzeal_utils.root_context import RootContext


class SimpleArgumentNewtonAlgorithm(SimpleArgumentAlgorithm, Loggable):
    """
    Class representation of a root finding algorithm combining the phase
    interpretation of the argument principle used in `SimpleArgumentAlgorithm`
    with a number of Newton steps once a sufficient refinement depth has been
    reached.
    """

    def calcRootsRecursion(
        self, zParts: tRecGrid, phiParts: tRecGrid, context: RootContext
    ) -> None:
        """
        TODO
        """
        # calculate difference between right/left and top/bottom
        deltaRe = zParts[1][0].real - zParts[3][0].real
        deltaIm = zParts[2][0].imag - zParts[0][0].imag
        # check if the given rectangle contains at least one zero
        phi = (
            phiParts[0].sum()
            + phiParts[1].sum()
            + phiParts[2].sum()
            + phiParts[3].sum()
        )

        # check if current rectangle contains zeros
        if phi < TWO_PI:
            if context.progress is not None and context.task is not None:
                context.progress.update(
                    context.task, advance=deltaRe * deltaIm
                )
            return

        # check if desired accuracy is aquired
        epsReal = 10 ** (-context.precision[0])
        epsImag = 10 ** (-context.precision[1])
        if deltaRe < epsReal and deltaIm < epsImag:
            SimpleArgumentAlgorithm.getRootFromRectangle(
                zParts[1][0],
                zParts[3][0],
                zParts[2][0],
                zParts[0][0],
                phi,
                context,
            )
            return

        # check if the current box contains a simple root
        if phi < FOUR_PI and deltaRe < 0.1 and deltaIm < 0.1:
            xStart = 0.5 * (
                zParts[1][0].real
                + zParts[3][0].real
                + 1j * (zParts[2][0].imag + zParts[0][0].imag)
            )
            try:
                newZero = newton(
                    context.f,
                    xStart,
                    context.df,
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

        # the current box contains a non-simple root and must be refined
        if deltaRe / epsReal > deltaIm / epsImag:
            zPartsNew, phiPartsNew = self.divideVertical(
                zParts, phiParts, context
            )
            self.calcRootsRecursion(zPartsNew[0], phiPartsNew[0], context)

            self.calcRootsRecursion(zPartsNew[1], phiPartsNew[1], context)

        else:
            zPartsNew, phiPartsNew = self.divideHorizontal(
                zParts, phiParts, context
            )
            self.calcRootsRecursion(zPartsNew[0], phiPartsNew[0], context)

            self.calcRootsRecursion(zPartsNew[1], phiPartsNew[1], context)
