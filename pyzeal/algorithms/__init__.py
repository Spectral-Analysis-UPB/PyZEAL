"""
The `algorithms` package contains the core root finding algorithm of `PyZEAL`.

A `FinderAlgorithm` accepts a request to calculate roots in some given
`RootContext`. Under the hood it combines some concrete refinement strategy
with a concrete `ArgumentEstimator`. The algorithm produces its results by
using the latter's results as an informational basis for the former.
"""

from pyzeal.algorithms.finder_algorithm import FinderAlgorithm
from pyzeal.algorithms.newton_grid import NewtonGridAlgorithm
from pyzeal.algorithms.polynomial_holo import AssociatedPolynomialAlgorithm
from pyzeal.algorithms.simple_holo import SimpleArgumentAlgorithm
from pyzeal.algorithms.simple_holo_newton import SimpleArgumentNewtonAlgorithm

__all__ = [
    "FinderAlgorithm",
    "NewtonGridAlgorithm",
    "AssociatedPolynomialAlgorithm",
    "SimpleArgumentAlgorithm",
    "SimpleArgumentNewtonAlgorithm",
]
