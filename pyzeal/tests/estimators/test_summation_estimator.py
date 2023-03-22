"""
This module tests the behavior of the summation-based estimator.
"""

import numpy as np
import pytest

from pyzeal.algorithms.estimators import EstimatorCache
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.tests.resources.testing_estimator_resources import (
    lineCases,
    rectangleCases,
)
from pyzeal.utils.factories.estimator_factory import EstimatorFactory


@pytest.mark.parametrize("testName", rectangleCases.keys())
def testSummationEstimatorRectangle(testName: str) -> None:
    """
    Test the summation-based estimator over a rectangular contour with the
    test case given by `testName`.

    :param testName: Case to test.
    """
    context, order, reRan, imRan, expected = rectangleCases[testName]
    est = EstimatorFactory.getConcreteEstimator(
        EstimatorTypes.SUMMATION_ESTIMATOR,
        numPts=6500,
        deltaPhi=0.01,
        maxPrecision=1e-10,
        cache=EstimatorCache(),
    )
    result = est.calcMoment(order, reRan, imRan, context)
    assert np.abs(result - expected) < 1e-6


@pytest.mark.parametrize("testName", lineCases.keys())
def testSummationEstimatorLine(testName: str) -> None:
    """
    Test the summation-based estimator over a line with the test case given
    by `testName`.

    :param testName: Case to test.
    """
    context, order, zStart, zEnd, expected = lineCases[testName]
    est = EstimatorFactory.getConcreteEstimator(
        EstimatorTypes.SUMMATION_ESTIMATOR,
        numPts=6500,
        deltaPhi=0.01,
        maxPrecision=1e-10,
        cache=EstimatorCache(),
    )
    result = est.calcMomentAlongLine(order, zStart, zEnd, context)
    assert np.abs(result - expected) < 1e-6
