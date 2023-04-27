"""
This module contains tests of the grid-based Newton algorithm implementation
of the `FinderAlgorithm` interface.

Authors:\n
- Luca Wasmuth\n
"""

import numpy as np
import pytest

from pyzeal.algorithms.newton_grid import NewtonGridAlgorithm
from pyzeal.pyzeal_types.filter_types import FilterTypes
from pyzeal.settings.ram_settings_service import RAMSettingsService
from pyzeal.settings.settings_service import SettingsService
from pyzeal.tests.resources.finder_test_cases import testFunctions
from pyzeal.tests.resources.utils import rootsMatchClosely
from pyzeal.utils.containers.rounding_container import RoundingContainer
from pyzeal.utils.factories.container_factory import ContainerFactory
from pyzeal.utils.root_context import RootContext
from pyzeal.utils.service_locator import ServiceLocator

settingsService = RAMSettingsService(verbose=False)
ServiceLocator.registerAsSingleton(SettingsService, settingsService)

# some test functions do not work due to algorithmic limitations
KNOWN_FAILURES = ["x^30", "x^50", "x^100", "1e6 * x^100"]


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.parametrize("testName", sorted(testFunctions.keys()))
def testNewtonGridRootFinder(testName: str) -> None:
    """
    Test the Newton grid algorithm with the function given by `testName`

    :param testName: Name of the test case
    """
    if testName in KNOWN_FAILURES:
        pytest.skip()

    for numSamplePoints in [25, 35]:
        precision = testFunctions[testName].precision
        newtonGridAlgo = NewtonGridAlgorithm(numSamplePoints=numSamplePoints)
        container = RoundingContainer(precision=precision)
        ContainerFactory.registerPreDefinedFilter(
            container, filterType=FilterTypes.FUNCTION_VALUE_ZERO
        )
        ContainerFactory.registerPreDefinedFilter(
            container, filterType=FilterTypes.ZERO_IN_BOUNDS
        )
        context = RootContext(
            f=testFunctions[testName].testFunc,
            df=testFunctions[testName].testFuncDerivative,
            container=container,
            precision=precision,
            reRan=testFunctions[testName].reRan,
            imRan=testFunctions[testName].imRan,
        )
        newtonGridAlgo.calcRoots(context)
        foundRoots = container.getRoots()
        expectedRoots = np.array(testFunctions[testName].expectedRoots)

        assert rootsMatchClosely(
            foundRoots, expectedRoots, precision=precision
        )
