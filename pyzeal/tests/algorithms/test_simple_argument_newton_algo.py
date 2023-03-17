"""
TODO
"""

import numpy as np
import pytest

from pyzeal.algorithms.simple_holo_newton import SimpleArgumentNewtonAlgorithm
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.tests.resources.testing_estimator_resources import (
    functions,
    generateRootContext,
)


@pytest.mark.parametrize("testName", functions.keys())
def testSimpleArgumentNewtonAlgo(testName: str) -> None:
    """
    Test the SIMPLE_HOLO_NEWTON algorithm by checking if the found roots
    actually have function values sufficiently close to zero.
    """
    rContext = generateRootContext(testName, (-5, 5), (-5, 5))
    algo = SimpleArgumentNewtonAlgorithm(EstimatorTypes.SUMMATION_ESTIMATOR)
    algo.calcRoots(rContext)
    foundRootsAreRoots = True
    for root in np.asarray(rContext.container.getRoots()):
        if np.abs(rContext.f(root)) > 0.01:
            foundRootsAreRoots = False
    assert foundRootsAreRoots
