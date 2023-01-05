"""
Class FinderAlgorithm from the package pyzeal_algorithms.
This module defines a simple root finding algorithm that works on any
continuously differentiable function by constructing a supporting grid in the
complex plane and starting an ordinary Newton algorithm at these support
points. It is expected that this approach underperforms in compared to
algorithms which fully exploit the holomorphic nature of target functions.

Authors:\n
- Philipp Schuette\n
"""

from pyzeal_algorithms.finder_algorithm import FinderAlgorithm


class NewtonGridAlgorithm(FinderAlgorithm):
    """
    Class representation of a root finding algorithm for holomorphic functions
    based on starting an ordinary Newton algorithm on a grid of support points
    in the complex plane.
    """
