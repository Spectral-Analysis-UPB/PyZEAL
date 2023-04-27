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
from pyzeal.algorithms.polynomial_holo import AssociatedPolynomialAlgorithm
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
KNOWN_FAILURES = ["x^100", "1e6 * x^100"]


@pytest.mark.parametrize("testName", sorted(testFunctions.keys()))
def testSimpleArgument(testName: str) -> None:
    """
    Test the SIMPLE_ARGUMENT algorithm with the test case given by `testName`.

    :param testName: Name of the test case
    """
    if testName in KNOWN_FAILURES:
        pytest.skip()

    # initialize the algorithm under test
    simpleArgumentAlgo = AssociatedPolynomialAlgorithm(
        estimatorType=EstimatorTypes.QUADRATURE_ESTIMATOR
    )

    context = buildContextFromData(testFunctions[testName])
    simpleArgumentAlgo.calcRoots(context)
    foundRoots = context.container.getRoots()  # pylint: disable=E1111
    expectedRoots = np.array(testFunctions[testName].expectedRoots)

    assert rootsMatchClosely(
        foundRoots, expectedRoots, precision=testFunctions[testName].precision
    )
