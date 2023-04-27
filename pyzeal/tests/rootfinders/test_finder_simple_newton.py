"""
This module contains tests of the SIMPLE_ARGUMENT_NEWTON implementation
of the root finding algorithm interface.

Authors:\n
- Luca Wasmuth\n
"""

import numpy as np
import pytest

from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.ram_settings_service import RAMSettingsService
from pyzeal.settings.settings_service import SettingsService
from pyzeal.tests.resources.finder_helpers import (
    simpleArgumentNewtonRootFinder,
)
from pyzeal.tests.resources.finder_test_cases import testFunctions
from pyzeal.tests.resources.utils import rootsMatchClosely
from pyzeal.utils.service_locator import ServiceLocator

# disable progress bar by default for tests
settingsService = RAMSettingsService(verbose=False)
ServiceLocator.registerAsSingleton(SettingsService, settingsService)

# some test functions do not work due to z-refinement limitations
KNOWN_FAILURES = ["x^100", "1e6 * x^100"]
# some test functions act strangely on some domains
EXCEPTIONAL_CASES = ["x^30", "x^50", "x^5-4x+2"]


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.parametrize("testName", sorted(testFunctions.keys()))
@pytest.mark.parametrize("parallel", [False, True])
@pytest.mark.parametrize(
    "estimator",
    [EstimatorTypes.SUMMATION_ESTIMATOR, EstimatorTypes.QUADRATURE_ESTIMATOR],
)
def testSimpleArgumentNewton(
    testName: str, parallel: bool, estimator: EstimatorTypes
) -> None:
    """
    Test the SIMPLE_ARGUMENT_NEWTON RootFinder with the test case given by
    `testName`.

    :param testName: Name of the test case
    :param parallel: If roots should be searched in parallel
    :param estimator: The type of estimator to use
    """
    if testName in KNOWN_FAILURES:
        pytest.skip()

    reRan = testFunctions[testName].reRan
    imRan = testFunctions[testName].imRan
    if testName in EXCEPTIONAL_CASES:
        reRan = (-5, 5.1)
        imRan = (-5, 5.1)
    precision = testFunctions[testName].precision

    hrf = simpleArgumentNewtonRootFinder(
        testName, parallel=parallel, estimatorType=estimator
    )
    hrf.calculateRoots(reRan, imRan, precision=precision)
    foundRoots = hrf.roots
    expectedRoots = np.array(testFunctions[testName].expectedRoots)

    assert rootsMatchClosely(foundRoots, expectedRoots, precision=precision)
