"""
TODO

Authors:\n
- Philipp Schuette\n
"""

from pyzeal_algorithms.pyzeal_estimators import (
    ArgumentEstimator,
    EstimatorCache,
    QuadratureEstimator,
    SummationEstimator,
)
from pyzeal_logging.config import initLogger
from pyzeal_types.estimator_types import EstimatorTypes


class EstimatorFactory:
    "Static factory class used to create instances of argument estimators."

    # initialize the module level logger
    logger = initLogger(__name__.rsplit(".", maxsplit=1)[-1])

    @staticmethod
    def getConcreteEstimator(
        estimatorType: EstimatorTypes = EstimatorTypes.DEFAULT,
        *,
        numPts: int,
        deltaPhi: float,
        maxPrecision: float,
        cache: EstimatorCache,
    ) -> ArgumentEstimator:
        """
        TODO
        """
        if estimatorType == EstimatorTypes.SUMMATION_ESTIMATOR:
            EstimatorFactory.logger.debug(
                "requested a new phase summation based argument estimator..."
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
            # TODO
            return QuadratureEstimator()

        EstimatorFactory.logger.debug(
            "requested a new default argument estimator..."
        )
        # TODO
        raise NotImplementedError("no default estimator in settings yet!")
