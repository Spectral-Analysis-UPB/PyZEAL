"""
Class AssociatedPolynomialAlgorithm from the package pyzeal_algorithms.

This module defines a root finding algorithm based on associated polynomials
whose coefficients are calculated from higher moments of the logarithmic
derivative using Newton's identities. Our implementation follows the original
ideas of [Delves, Lyness].

Authors:\n
- Philipp Schuette\n
"""

from typing import List, Tuple

import numpy as np

from pyzeal.algorithms.constants import MAX_PHASE, TWO_PI
from pyzeal.algorithms.simple_holo import SimpleArgumentAlgorithm
from pyzeal.algorithms.wrappers.classical_polynomial import ClassicalPolynomial
from pyzeal.utils.root_context import RootContext


class AssociatedPolynomialAlgorithm(SimpleArgumentAlgorithm):
    """
    Class representation of a root finding algorithm which uses numerical
    quadrature to calculate higher moments. Then Newton's identities can be
    used to calculate the associated polynomial from these moments. The zeros
    of the latter coincide with the zeros of the original target function.
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
        (3) construct and solve Newton identities if only a few roots present,
        or (4) subdivide further if too many roots present.

        :param reRan: Real part of current search Range
        :param imRan: Imaginary part of current search range
        :param phi: Change in argument along the boundary of the current range
        :param context: `RootContext` in which the algorithm operates
        """
        if context.df is None:
            raise ValueError(
                "holomorphic Newton polynomial algorithm needs the derivative!"
            )
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

        # check if the current box contains sufficiently few roots to construct
        # an associated polynomial with stable coefficients/roots
        if TWO_PI < phi < MAX_PHASE:
            degree = int(round(phi / (2 * np.pi), 0))
            self.logger.debug(
                "constructing associated poly of degree %d from moments!",
                degree,
            )

            # store higher moments for associated polynomial construction
            moments: List[complex] = []
            for order in range(1, degree + 1):
                moment = self.estimator.calcMoment(
                    order=order,
                    reRan=(x1, x2),
                    imRan=(y1, y2),
                    context=context,
                )
                moments.append(moment / (2 * np.pi))

            roots, orders = ClassicalPolynomial(
                coefficients=self.coefficientsFromMoments(moments)
            ).getRootsWithOrders(precision=context.precision)

            for newRoot, newOrder in zip(roots, orders):
                context.container.addRoot(
                    (newRoot, newOrder), context.toFilterContext()
                )

            if context.progress is not None and context.task is not None:
                context.progress.update(
                    context.task, advance=deltaRe * deltaIm
                )
            return

        super().decideRefinement((x1, x2), (y1, y2), phi, context)

    def coefficientsFromMoments(self, moments: List[complex]) -> List[complex]:
        """
        Calculate the coefficients of the associated polynomial from the higher
        moments (=power sums of roots) using Newton's identities.

        :param moments: moments/power sums of roots
        :returns: coefficients of the associated polynomial
        """
        coefficients: List[complex] = [1]
        for k in range(1, len(moments) + 1):
            temp: complex = 0
            tempSign = 1

            for i in range(1, k + 1):
                temp += tempSign * coefficients[-i] * moments[i - 1]
                tempSign *= -1
            coefficients.append(temp / k)
        # correct signs in the coefficients just calculated
        sign = 1
        for i, _ in enumerate(coefficients):
            coefficients[i] *= sign
            sign *= -1
        coefficients.reverse()

        return coefficients
