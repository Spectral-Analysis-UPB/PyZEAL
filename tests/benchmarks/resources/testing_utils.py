"""
This module contains a collection of utility functions used in the tests of the
PyZEAL project.

Authors:\n
- Luca Wasmuth\n
"""

import numpy as np

from pyzeal_types.root_types import tVec


def rootsMatchClosely(roots1: tVec, roots2: tVec, atol: float) -> bool:
    """
    Test if two vectors contain the same roots, up to inaccuraccy of size atol.

    :param roots1: first vector of roots
    :type roots1: NDArray[complex128]
    :param roots2: second vector of roots
    :type roots2: NDArray[complex128]
    :param atol: tolerance up to which roots are considered the same
    :type atol: float
    :return: indicates if `roots1` and `roots2` are the same (up to `atol`)
    :rtype: bool
    """
    for root1 in roots1:
        foundEqualRoot: bool = False
        for root2 in roots2:
            if np.abs(root1 - root2) < atol:
                foundEqualRoot = True
                break
        if not foundEqualRoot:
            return False

    return True
