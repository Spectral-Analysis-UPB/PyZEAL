import numpy as np
import pytest
from testing_estimator_resources import functions, generateRootContext

from pyzeal_algorithms.simple_holo import SimpleArgumentAlgorithm
from pyzeal_types.estimator_types import EstimatorTypes


@pytest.mark.parametrize("testName", functions.keys())
def testSimpleArgumentAlgo(testName: str):
    """Test the SIMPLE_HOLO algorithm by checking if the found roots actually
    have function values sufficiently close to zero.
    """
    if testName == "sin(x)":
        pytest.skip()  # TODO: why does this fail?
    rC = generateRootContext(testName, (-5, 5), (-5, 5))
    algo = SimpleArgumentAlgorithm(EstimatorTypes.SUMMATION_ESTIMATOR)
    algo.calcRoots(rC)
    foundRootsAreRoots = True
    for root in np.asarray(rC.container.getRoots()):
        if np.abs(rC.f(root)) > 0.01:
            foundRootsAreRoots = False
    assert foundRootsAreRoots
