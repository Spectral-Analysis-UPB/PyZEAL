"""
This module provides named constants used to identify concrete argument
estimator implementations in any instance where such an estimator is required.

Authors:\n
- Philipp Schuette\n
"""

from enum import Enum


class EstimatorTypes(Enum):
    "Enumeration containing named constants identifying available estimators."
    SUMMATION_ESTIMATOR = "SummationEstimator"
    QUADRATURE_ESTIMATOR = "QuadratureEstimator"
    DEFAULT = "DefaultEstimator"
