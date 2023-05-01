"""
This module contains tests of the grid-based Newton algorithm implementation
of the root finding algorithm interface.

Authors:\n
- Luca Wasmuth\n
"""

import numpy as np
import pytest

from pyzeal.settings.ram_settings_service import RAMSettingsService
from pyzeal.settings.settings_service import SettingsService
from pyzeal.tests.resources.finder_helpers import newtonGridFinder
from pyzeal.tests.resources.finder_test_cases import testFunctions
from pyzeal.tests.resources.utils import rootsMatchClosely
from pyzeal.utils.service_locator import ServiceLocator

settingsService = RAMSettingsService(verbose=False)
ServiceLocator.registerAsSingleton(SettingsService, settingsService)

# some test functions do not work due to algorithmic limitations
KNOWN_FAILURES = ["x^30", "x^50", "x^100", "1e6 * x^100"]


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.parametrize("testName", sorted(testFunctions.keys()))
@pytest.mark.parametrize("parallel", [False, True])
def testNewtonGridRootFinder(testName: str, parallel: bool) -> None:
    """
    Test the parallel and serial implementations of the `RootFinderInterface`
    using the `NewtonGridAlgorithm` implementation of the `FinderAlgorithm`.

    :param testName: Name of the test case
    :param parallel: If roots should be searched in parallel
    """
    if testName in KNOWN_FAILURES:
        pytest.skip()

    gridRF = newtonGridFinder(testName, numSamplePoints=30, parallel=parallel)
    reRan = testFunctions[testName].reRan
    imRan = testFunctions[testName].imRan
    precision = testFunctions[testName].precision

    if testName == "exp(x)-1":
        precision = (2, 2)

    gridRF.calculateRoots(reRan, imRan, precision=precision)
    foundRoots = np.sort_complex(gridRF.roots)
    expectedRoots = np.array(testFunctions[testName].expectedRoots)

    assert rootsMatchClosely(foundRoots, expectedRoots, precision=precision)
