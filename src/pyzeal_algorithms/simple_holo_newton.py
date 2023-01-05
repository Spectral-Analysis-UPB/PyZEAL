"""
Class FinderAlgorithm from the package pyzeal_algorithms.
This module defines a refined version of the `SimpleArgumentAlgorithm`
by supplementing the argument principle with a Newton algorithm once a starting
point has been identified with sufficient accuracy.

Authors:\n
- Philipp Schuette\n
"""

from pyzeal_algorithms.simple_holo import SimpleArgumentAlgorithm


class SimpleArgumentNewtonAlgorithm(SimpleArgumentAlgorithm):
    """
    Class representation of a root finding algorithm combining the phase
    interpretation of the argument principle used in `SimpleArgumentAlgorithm`
    with a number of Newton steps once a sufficient refinement depth has been
    reached.
    """
