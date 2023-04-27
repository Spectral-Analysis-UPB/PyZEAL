"""
This module contains tests of the SIMPLE_ARGUMENT implementation of the
`FinderAlgorithm`interface.

Authors:\n
- Luca Wasmuth\n
- Philipp Schuette\n
"""

import numpy as np
import pytest

from pyzeal.algorithms.estimators.argument_estimator import ArgumentEstimator
from pyzeal.algorithms.simple_holo import SimpleArgumentAlgorithm
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.ram_settings_service import RAMSettingsService
from pyzeal.settings.settings_service import SettingsService
from pyzeal.tests.resources.finder_test_cases import (
    buildContextFromData,
    testFunctions,
)
from pyzeal.tests.resources.utils import rootsMatchClosely
from pyzeal.utils.factories.estimator_factory import EstimatorFactory
from pyzeal.utils.service_locator import ServiceLocator

# disable progress bar by default for tests
settingsService = RAMSettingsService(verbose=False)
ServiceLocator.registerAsSingleton(SettingsService, settingsService)
ServiceLocator.registerAsTransient(
    ArgumentEstimator, EstimatorFactory.getConcreteEstimator
)

# some test functions do not work due to z-refinement limitations
KNOWN_FAILURES = ["poly", "x^100", "1e6 * x^100"]


@pytest.mark.parametrize("testName", sorted(testFunctions.keys()))
@pytest.mark.parametrize(
    "estimator",
    [EstimatorTypes.SUMMATION_ESTIMATOR, EstimatorTypes.QUADRATURE_ESTIMATOR],
)
def testSimpleArgument(testName: str, estimator: EstimatorTypes) -> None:
    """
    Test the SIMPLE_ARGUMENT algorithm with the test case given by `testName`.

    :param testName: Name of the test case
    :param estimator: The type of estimator to use
    """
    if testName in KNOWN_FAILURES:
        pytest.skip()

    # initialize the algorithm under test
    simpleArgumentAlgo = SimpleArgumentAlgorithm(estimatorType=estimator)

    context = buildContextFromData(testFunctions[testName])
    simpleArgumentAlgo.calcRoots(context)
    foundRoots = context.container.getRoots()  # pylint: disable=E1111
    expectedRoots = np.array(testFunctions[testName].expectedRoots)

    assert rootsMatchClosely(
        foundRoots, expectedRoots, precision=testFunctions[testName].precision
    )
