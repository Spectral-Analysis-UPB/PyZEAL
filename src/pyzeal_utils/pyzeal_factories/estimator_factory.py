"""
This module provides a static factory class which maps the argument estimators
available in the `EstimatorType` enumeration to appropriate members of the
`ArgumentEstimator` type.

Authors:\n
- Philipp Schuette\n
"""

from typing import Optional

from pyzeal_algorithms.pyzeal_estimators import (
    ArgumentEstimator,
    EstimatorCache,
    QuadratureEstimator,
    SummationEstimator,
)
from pyzeal_logging.log_manager import LogManager
from pyzeal_types.estimator_types import EstimatorTypes


class EstimatorFactory:
    "Static factory class used to create instances of argument estimators."

    # initialize the module level logger
    logger = LogManager.initLogger(__name__.rsplit(".", maxsplit=1)[-1])

    @staticmethod
    def getConcreteEstimator(
        estimatorType: EstimatorTypes,
        *,
        cache: EstimatorCache,
        numPts: Optional[int] = None,
        deltaPhi: Optional[float] = None,
        maxPrecision: Optional[float] = None,
    ) -> ArgumentEstimator:
        """
        Construct and return an estimator instance based on the given type
        of estimator `estimatorType`.

        :param estimatorType: Type of estimator to return
        :type estimatorType: EstimatorTypes
        :param numPts: Number of sampling points
        :type numPts: Optional[int]
        :param deltaPhi: Threshold for argument change in a single step
        :type deltaPhi: Optional[float]
        :param maxPrecision: Maximum precision, after which no more refinement
            takes place
        :type maxPrecision: Optional[float]
        :param cache: Cache to store argument changes
        :type cache: EstimatorCache
        :return: Estimator instance with given parameters
        :rtype: ArgumentEstimator
        """
        if estimatorType == EstimatorTypes.SUMMATION_ESTIMATOR:
            EstimatorFactory.logger.debug(
                "requested a new phase summation based argument estimator..."
            )
            if numPts is None or deltaPhi is None or maxPrecision is None:
                raise ValueError(
                    "SUMMATION_ESTIMATOR requires numPts, deltaPhi and \
                        maxPrecision!"
                )
            return SummationEstimator(
                numPts=numPts,
                deltaPhi=deltaPhi,
                maxPrecision=maxPrecision,
                cache=cache,
            )
        if estimatorType == EstimatorTypes.QUADRATURE_ESTIMATOR:
            EstimatorFactory.logger.debug(
                "requested a new quadrature based argument estimator..."
            )
            return QuadratureEstimator(cache=cache)

        EstimatorFactory.logger.debug(
            "requested a new default argument estimator..."
        )
        # TODO: implement default estimator in settings
        return EstimatorFactory.getConcreteEstimator(
            EstimatorTypes.SUMMATION_ESTIMATOR,
            numPts=numPts,
            deltaPhi=deltaPhi,
            maxPrecision=maxPrecision,
            cache=cache,
        )
