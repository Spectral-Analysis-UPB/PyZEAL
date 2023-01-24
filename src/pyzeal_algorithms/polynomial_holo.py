"""
Class AssociatedPolynomialAlgorithm from the package pyzeal_algorithms.
This module defines a root finding algorithm based on associated polynomials
whose coefficients are calculated from higher moments of the logarithmic
derivative using Newton's identities. Our implementation follows the original
ideas of [Delves, Lyness].

Authors:\n
- Philipp Schuette\n
"""

from pyzeal_algorithms.finder_algorithm import FinderAlgorithm
from pyzeal_logging.loggable import Loggable
from pyzeal_utils.root_context import RootContext


class AssociatedPolynomialAlgorithm(FinderAlgorithm, Loggable):
    """
    Class representation of a root finding algorithm which uses numerical
    quadrature to calculate higher moments. Then Newton's identities can be
    used to calculate the associated polynomial from these moments. The zeros
    of the latter coincide with the zeros of the original target function.
    """

    def calcRoots(self, context: RootContext) -> None:
        """
        Start a root calculation using numerical quadrature and the associated
        polynomial. TODO

        :param context: context in which the algorithm operates
        :type context: RootContext
        """
        raise NotImplementedError()
