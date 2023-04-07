"""
This module contains tests for the SIMPLE_HOLO_NEWTON algorithm.
"""

import numpy as np
import pytest

from pyzeal.algorithms.estimators.argument_estimator import ArgumentEstimator
from pyzeal.algorithms.simple_holo_newton import SimpleArgumentNewtonAlgorithm
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.tests.resources.testing_estimator_resources import (
    functions,
    generateRootContext,
)
from pyzeal.utils.factories.estimator_factory import EstimatorFactory
from pyzeal.utils.service_locator import ServiceLocator

ServiceLocator.registerAsTransient(
    ArgumentEstimator, EstimatorFactory.getConcreteEstimator
)


@pytest.mark.parametrize("testName", sorted(functions.keys()))
@pytest.mark.parametrize(
    "estimator",
    [EstimatorTypes.SUMMATION_ESTIMATOR, EstimatorTypes.QUADRATURE_ESTIMATOR],
)
def testSimpleArgumentNewtonAlgo(
    testName: str, estimator: EstimatorTypes
) -> None:
    """
    Test the SIMPLE_HOLO_NEWTON algorithm by checking if the found roots
    actually have function values sufficiently close to zero.

    :param testName: The name of the current test
    :param estimator: The type of estimator to use
    """
    rContext = generateRootContext(testName, (-5, 5), (-5, 5))
    algo = SimpleArgumentNewtonAlgorithm(estimatorType=estimator)
    algo.calcRoots(rContext)
    foundRootsAreRoots = True
    for root in np.asarray(rContext.container.getRoots()):
        if np.abs(rContext.f(root)) > 0.01:
            foundRootsAreRoots = False
    assert foundRootsAreRoots
