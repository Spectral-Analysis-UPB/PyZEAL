"""
TODO
"""

import numpy as np
import pytest
from pyzeal.tests.testing_estimator_resources import (
    functions,
    generateRootContext,
)

from pyzeal.algorithms.simple_holo_newton import SimpleArgumentNewtonAlgorithm
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes


@pytest.mark.parametrize("testName", functions.keys())
def testSimpleArgumentNewtonAlgo(testName: str):
    """
    Test the SIMPLE_HOLO_NEWTON algorithm by checking if the found roots
    actually have function values sufficiently close to zero.
    """
    rC = generateRootContext(testName, (-5, 5), (-5, 5))
    algo = SimpleArgumentNewtonAlgorithm(EstimatorTypes.SUMMATION_ESTIMATOR)
    algo.calcRoots(rC)
    foundRootsAreRoots = True
    for root in np.asarray(rC.container.getRoots()):
        if np.abs(rC.f(root)) > 0.01:
            foundRootsAreRoots = False
    assert foundRootsAreRoots
