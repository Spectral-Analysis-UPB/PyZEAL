"""
This module provides a static factory class which maps the argument estimators
available in the `EstimatorType` enumeration to appropriate members of the
`ArgumentEstimator` type.

Authors:\n
- Philipp Schuette\n
"""

from typing import Optional

from pyzeal.algorithms.estimators import ArgumentEstimator, EstimatorCache
from pyzeal.algorithms.estimators.quad_estimator import QuadratureEstimator
from pyzeal.algorithms.estimators.sum_estimator import SummationEstimator
from pyzeal.pyzeal_logging.log_manager import LogManager
from pyzeal.pyzeal_logging.logger_facade import PyZEALLogger
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.service_locator import ServiceLocator


class EstimatorFactory:
    "Static factory class used to create instances of argument estimators."

    # module level logger
    _logger: Optional[PyZEALLogger] = None

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
        :param numPts: Number of sampling points
        :param deltaPhi: Threshold for argument change in a single step
        :param maxPrecision: Maximum precision, after which no more refinement
            takes place
        :param cache: Cache to store argument changes
        :return: Estimator instance with given parameters
        """
        if EstimatorFactory._logger is None:
            EstimatorFactory._logger = LogManager.initLogger(
                __name__.rsplit(".", maxsplit=1)[-1],
                ServiceLocator.tryResolve(SettingsService).logLevel,
            )
        if estimatorType == EstimatorTypes.SUMMATION_ESTIMATOR:
            EstimatorFactory._logger.debug(
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
            EstimatorFactory._logger.debug(
                "requested a new quadrature based argument estimator..."
            )
            return QuadratureEstimator(cache=cache)

        EstimatorFactory._logger.debug(
            "requested a new default argument estimator..."
        )
        settings = ServiceLocator.tryResolve(SettingsService)
        return EstimatorFactory.getConcreteEstimator(
            settings.defaultEstimator,
            numPts=numPts,
            deltaPhi=deltaPhi,
            maxPrecision=maxPrecision,
            cache=cache,
        )
