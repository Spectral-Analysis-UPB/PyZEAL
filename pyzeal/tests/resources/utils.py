"""
This module contains a collection of utility functions used in the tests of the
PyZEAL project.

Authors:\n
- Luca Wasmuth\n
- Philipp Schuette\n
"""

from typing import Tuple

from pyzeal.pyzeal_types.root_types import tVec


def rootsMatchClosely(
    roots1: tVec,
    roots2: tVec,
    precision: Tuple[int, int],
    allowSubset: bool = False,
) -> bool:
    """
    Determine if `roots1` and `roots2` contain the same roots, up to a number
    of decimal places given by `precision`.

    :param roots1: first vector of roots
    :param roots2: second vector of roots
    :param precision: number of decimal places where roots are considered equal
        the second is sufficient
    :return: flag indicating if `roots1` and `roots2` are the same
    """
    assert len(roots1) == len(roots2) or allowSubset

    deltaReal = 10 ** (-precision[0])
    deltaImag = 10 ** (-precision[1])

    for root1 in roots1:
        matchFound = False
        for root2 in roots2:
            if (
                abs(root1.real - root2.real) < deltaReal
                and abs(root1.imag - root2.imag) < deltaImag
            ):
                matchFound = True
                break
        if not matchFound:
            return False

    return True
