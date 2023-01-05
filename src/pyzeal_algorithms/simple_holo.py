"""
Class SimpleHoloAlgorithm from the package pyzeal_algorithms.
This module defines a root finding algorithm based on a simple, straight
forward approach to the argument principle. The simplicity comes from the fact
that we avoid numeric quadrature by approximating integration of the
logarithmic derivative via changes in the complex argument of the target
function.

Authors:\n
- Philipp Schuette\n
"""

from pyzeal_algorithms.finder_algorithm import FinderAlgorithm


class SimpleArgumentAlgorithm(FinderAlgorithm):
    """
    Class representation of a simple root finding algorithm for holomorphic
    functions based on the argument principle and the approximation of
    integrals over logarithmic derivatives via the summation of phase
    differences.
    """
