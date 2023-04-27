"""
This module tests the behavior of the quadratue-based estimator.
"""
import numpy as np
import pytest

from pyzeal.algorithms.estimators import EstimatorCache
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.tests.resources.estimator_resources import (
    lineCases,
    rectangleCases,
)
from pyzeal.utils.factories.container_factory import ContainerFactory
from pyzeal.utils.factories.estimator_factory import EstimatorFactory
from pyzeal.utils.root_context import RootContext


@pytest.mark.parametrize("testName", sorted(rectangleCases.keys()))
def testQuadratueEstimatorRectangle(testName: str) -> None:
    """
    Test the quadrature-based estimator over a rectangular contour with the
    test case given by `testName`.

    :param testName: Case to test.
    """
    context, order, expected = rectangleCases[testName]
    est = EstimatorFactory.getConcreteEstimator(
        EstimatorTypes.QUADRATURE_ESTIMATOR,
        numPts=6500,
        deltaPhi=0.01,
        maxPrecision=1e-10,
        cache=EstimatorCache(),
    )
    result = est.calcMoment(order, context.reRan, context.imRan, context)
    assert np.abs(result - expected) < 1e-6


@pytest.mark.parametrize("testName", sorted(lineCases.keys()))
def testQuadratureEstimatorLine(testName: str) -> None:
    """
    Test the quadrature-based estimator over a line with the test case given
    by `testName`.

    :param testName: Case to test.
    """
    context, order, zStart, zEnd, expected = lineCases[testName]
    est = EstimatorFactory.getConcreteEstimator(
        EstimatorTypes.QUADRATURE_ESTIMATOR,
        numPts=6500,
        deltaPhi=0.01,
        maxPrecision=1e-10,
        cache=EstimatorCache(),
    )
    result = est.calcMomentAlongLine(order, zStart, zEnd, context)
    assert np.abs(result - expected) < 1e-6


def testExceptionDerivativefree() -> None:
    """
    Test exception throwing if the quadrature estimator is not provided with
    the derivative.
    """
    context = RootContext(
        f=lambda x: x,
        df=None,
        container=ContainerFactory.getConcreteContainer(),
        precision=(3, 3),
    )
    est = EstimatorFactory.getConcreteEstimator(
        EstimatorTypes.QUADRATURE_ESTIMATOR,
        numPts=6500,
        deltaPhi=0.01,
        maxPrecision=1e-10,
        cache=EstimatorCache(),
    )
    with pytest.raises(ValueError):
        est.calcMomentAlongLine(0, 0, 1, context)
