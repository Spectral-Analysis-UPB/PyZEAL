"""
This module contains tests of the grid-based Newton algorithm implementation
of the root finding algorithm interface.

Authors:\n
- Luca Wasmuth\n
"""

from typing import Final

import numpy as np
import pytest

from pyzeal.settings.ram_settings_service import RAMSettingsService
from pyzeal.settings.settings_service import SettingsService
from pyzeal.tests.resources.testing_fixtures import newtonGridFinder
from pyzeal.tests.resources.testing_resources import (
    IM_RAN,
    RE_RAN,
    testFunctions,
)
from pyzeal.tests.resources.testing_utils import rootsMatchClosely
from pyzeal.utils.service_locator import ServiceLocator

# 20 is enough to pass all tests while still running faster than the default 50
NUM_SAMPLE_POINTS: Final[int] = 20

settingsService = RAMSettingsService(verbose=False)
ServiceLocator.registerAsSingleton(SettingsService, settingsService)

# some test functions do not work due to algorithmic limitations
KNOWN_FAILURES = ["x^30", "x^50", "x^100", "1e6 * x^100"]


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.parametrize("testName", sorted(testFunctions.keys()))
@pytest.mark.parametrize("parallel", [False, True])
def testNewtonGridRootFinder(testName: str, parallel: bool) -> None:
    """
    Test the Newton-Grid-Rootfinder with the function given by `testName`

    :param testName: Name of the test case
    :param parallel: If roots should be searched in parallel
    """
    if testName in KNOWN_FAILURES:
        pytest.skip()
    for numSamplePoints in [20, 50]:
        gridRF = newtonGridFinder(testName, numSamplePoints, parallel=parallel)
        gridRF.calculateRoots(RE_RAN, IM_RAN, precision=(4, 4))
        foundRoots = np.sort_complex(gridRF.roots)
        expectedRoots = np.sort_complex(np.array(testFunctions[testName][2]))
        assert rootsMatchClosely(foundRoots, expectedRoots, atol=1e-3)
