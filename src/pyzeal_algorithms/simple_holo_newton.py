"""
Class FinderAlgorithm from the package pyzeal_algorithms.
This module defines a refined version of the `SimpleArgumentAlgorithm`
by supplementing the argument principle with a Newton algorithm once a starting
point has been identified with sufficient accuracy.

Authors:\n
- Philipp Schuette\n
"""

import numpy as np
from scipy.optimize import newton

from pyzeal_algorithms.simple_holo import (
    SimpleArgumentAlgorithm,
    TWO_PI,
    FOUR_PI,
)
from pyzeal_logging.loggable import Loggable
from pyzeal_utils.root_context import RootContext
from pyzeal_types.root_types import tRecGrid


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
        if phi > TWO_PI:
            # check if desired accuracy is aquired
            if deltaRe < 10 ** (-context.precision[0]) and deltaIm < 10 ** (
                -context.precision[1]
            ):
                newZero = 0.5 * (
                    zParts[1][0].real
                    + zParts[3][0].real
                    + 1j * (zParts[2][0].imag + zParts[0][0].imag)
                )
                zOrder = int(np.round(phi / (2 * np.pi)))
                context.container.addRoot(
                    (newZero, zOrder), context.toFilterContext()
                )
                if context.progress is not None and context.task is not None:
                    context.progress.update(
                        context.task, advance=deltaRe * deltaIm
                    )
            elif (phi < FOUR_PI) and (deltaRe < 0.1) and (deltaIm < 0.1):
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
                        tol=10
                        ** (-max(context.precision[0], context.precision[1])),
                    )
                    if isinstance(newZero, np.ndarray):
                        for pair in zip(
                            newZero, np.ones_like(newZero, dtype=int)
                        ):
                            context.container.addRoot(
                                pair, context.toFilterContext()
                            )
                    elif isinstance(newZero, complex):
                        context.container.addRoot(
                            (newZero, 1), context.toFilterContext()
                        )
                except RuntimeError:
                    pass
                finally:
                    if (
                        context.progress is not None
                        and context.task is not None
                    ):
                        context.progress.update(
                            context.task, advance=deltaRe * deltaIm
                        )
            else:
                if deltaRe / (10 ** (-context.precision[0])) > deltaIm / (
                    10 ** (-context.precision[1])
                ):
                    zPartsNew, phiPartsNew = self.divideVertical(
                        zParts, phiParts, context
                    )
                    self.calcRootsRecursion(
                        zPartsNew[0], phiPartsNew[0], context
                    )

                    self.calcRootsRecursion(
                        zPartsNew[1], phiPartsNew[1], context
                    )

                else:
                    zPartsNew, phiPartsNew = self.divideHorizontal(
                        zParts, phiParts, context
                    )
                    self.calcRootsRecursion(
                        zPartsNew[0], phiPartsNew[0], context
                    )

                    self.calcRootsRecursion(
                        zPartsNew[1], phiPartsNew[1], context
                    )
        else:
            if context.progress is not None and context.task is not None:
                context.progress.update(
                    context.task, advance=deltaRe * deltaIm
                )
