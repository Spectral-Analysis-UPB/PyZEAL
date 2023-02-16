"""
This module contains a collection of utility functions used in the tests of the
PyZEAL project.

Authors:\n
- Luca Wasmuth\n
"""

import numpy as np

from pyzeal_types.root_types import tVec


def _compareRootSets(roots1: tVec, roots2: tVec, atol: float) -> bool:
    """
    Test if two vectors contain the same roots, up to inaccuraccy of size atol.
    Internal method to supplement np.allclose, as numpy can't handle differenz
    sizes.

    :param roots1: first vector of roots
    :type roots1: tVec
    :param roots2: second vector of roots
    :type roots2: tVec
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


def rootsMatchClosely(roots1: tVec, roots2: tVec, atol: float) -> bool:
    """Determine if `roots1` and `roots2` contain the same roots, up to
    precision `atol`.

    :param roots1: first vector of roots
    :type roots1: tVec
    :param roots2: second vector of roots
    :type roots2: tVec
    :param atol: tolerance up to which roots are considered the same
    :type atol: float
    :return: indicates if `roots1` and `roots2` are the same (up to `atol`)
    :rtype: bool
    """
    try:
        numpy_match = np.allclose(roots1, roots2, atol=atol)
    except ValueError:
        numpy_match = False
    return numpy_match or _compareRootSets(roots1, roots2, atol)
