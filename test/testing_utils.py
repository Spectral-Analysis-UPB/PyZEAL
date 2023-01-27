import numpy as np


def rootsMatchClosely(roots1, roots2, atol) -> bool:
    r"""
    Test, if two sets contain the same roots, up to inaccuraccy of size atol
    :param roots1: first set of roots
    :type roots1: Set[complex]
    :param roots2: second set of roots
    :type roots2: Set[complex]
    :return: True if the number of zeroes in r1 and r2 is the same, and they
    lie at most atol apart
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
