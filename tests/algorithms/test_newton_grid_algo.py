"""
TODO
"""

import numpy as np
import pytest
from pyzeal.algorithms.newton_grid import NewtonGridAlgorithm
from pyzeal.tests.resources.testing_estimator_resources import (
    functions,
    generateRootContext,
)


@pytest.mark.parametrize("testName", functions.keys())
def testNewtonGridAlgo(testName: str):
    """
    Test the NEWTON_GRID algorithm by checking if the found roots actually
    have function values sufficiently close to zero.
    """
    rc = generateRootContext(testName, (-5, 5), (-5, 5))
    algo = NewtonGridAlgorithm()
    algo.calcRoots(rc)
    foundRootsAreRoots = True
    for root in np.asarray(rc.container.getRoots()):
        if np.abs(rc.f(root)) > 0.01:
            foundRootsAreRoots = False
    assert foundRootsAreRoots
