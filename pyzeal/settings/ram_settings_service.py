"""
A simple in-memory implementation of the `SettingsService` interface. Instances
of this service do not persist settings beyond program runtime. Their main use
is during testing of components which depend on settings.

Authors:\n
- Philipp Schuette\n
"""

from typing import Tuple

from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.settings_service import SettingsService


class RAMSettingsService(SettingsService):
    "Simple, non-persistent implementation of `SettingsService`."

    def __init__(
        self,
        container: ContainerTypes = ContainerTypes.ROUNDING_CONTAINER,
        algorithm: AlgorithmTypes = AlgorithmTypes.SIMPLE_ARGUMENT,
        estimator: EstimatorTypes = EstimatorTypes.SUMMATION_ESTIMATOR,
        logLevel: LogLevel = LogLevel.NOTSET,
        precision: Tuple[int, int] = (0, 0),
        verbose: bool = False,
    ) -> None:
        """
        Initialize a new in-memory settings service with given default values.

        :param :
        :param :
        :param :
        :param :
        :param :
        :param :
        """
        self._container = container
        self._algorithm = algorithm
        self._estimator = estimator
        self._logLevel = logLevel
        self._precision = precision
        self._verbose = verbose

    # docstr-coverage:inherited
    @property
    def defaultContainer(self) -> ContainerTypes:
        return self._container

    # docstr-coverage:inherited
    @defaultContainer.setter
    def defaultContainer(self, value: ContainerTypes) -> None:
        self._container = value

    # docstr-coverage:inherited
    @property
    def defaultAlgorithm(self) -> AlgorithmTypes:
        return self._algorithm

    # docstr-coverage:inherited
    @defaultAlgorithm.setter
    def defaultAlgorithm(self, value: AlgorithmTypes) -> None:
        self._algorithm = value

    # docstr-coverage:inherited
    @property
    def defaultEstimator(self) -> EstimatorTypes:
        return self._estimator

    # docstr-coverage:inherited
    @defaultEstimator.setter
    def defaultEstimator(self, value: EstimatorTypes) -> None:
        self._estimator = value

    # docstr-coverage:inherited
    @property
    def logLevel(self) -> LogLevel:
        return self._logLevel

    # docstr-coverage:inherited
    @logLevel.setter
    def logLevel(self, value: LogLevel) -> None:
        self._logLevel = value

    # docstr-coverage:inherited
    @property
    def verbose(self) -> bool:
        return self._verbose

    # docstr-coverage:inherited
    @verbose.setter
    def verbose(self, value: bool) -> None:
        self._verbose = value

    # docstr-coverage:inherited
    @property
    def precision(self) -> Tuple[int, int]:
        return self._precision

    # docstr-coverage:inherited
    @precision.setter
    def precision(self, value: Tuple[int, int]) -> None:
        self._precision = value
