"""
Module service_locator.py from the package PyZEAL.
TODO

Authors:\n
- Philipp Schuette\n
"""

from inspect import Parameter, signature
from typing import Callable, Dict, Type, TypeVar

from pyzeal_algorithms.finder_algorithm import FinderAlgorithm
from pyzeal_algorithms.pyzeal_estimators.argument_estimator import (
    ArgumentEstimator,
)
from pyzeal_settings.settings_service import SettingsService
from pyzeal_utils.pyzeal_containers.root_container import RootContainer
from pyzeal_utils.pyzeal_factories.algorithm_factory import AlgorithmFactory
from pyzeal_utils.pyzeal_factories.container_factory import ContainerFactory
from pyzeal_utils.pyzeal_factories.estimator_factory import EstimatorFactory
from pyzeal_utils.pyzeal_factories.settings_factory import (
    SettingsServiceFactory,
)
from pyzeal_utils.service_configuration_exception import (
    InvalidServiceConfiguration,
)

# type variable for the various signatures of ServiceLocator
T = TypeVar("T")


class ServiceLocator:
    """
    _summary_
    """

    _transientServices: Dict[Type, Callable[..., object]] = {
        FinderAlgorithm: AlgorithmFactory.getConcreteAlgorithm,
        SettingsService: SettingsServiceFactory.getConcreteSettings,
        ArgumentEstimator: EstimatorFactory.getConcreteEstimator,
        RootContainer: ContainerFactory.getConcreteContainer,
    }

    _singletonServices: Dict[Type, object] = {}

    @staticmethod
    def registerAsSingleton(serviceType: Type[T], instance: T) -> bool:
        """
        _summary_

        :param serviceType: _description_
        :type serviceType: _type_
        :param instance: _description_
        :type instance: _type_
        :return: _description_
        :rtype: _type_
        """
        if isinstance(instance, serviceType):
            ServiceLocator._singletonServices[serviceType] = instance
            return True
        return False

    @staticmethod
    def registerAsTransient(
        serviceType: Type[T], factory: Callable[..., T]
    ) -> bool:
        """
        _summary_

        :param serviceType: _description_
        :type serviceType: _type_
        :param factory: _description_
        :type factory: _type_
        :return: _description_
        :rtype: _type_
        """
        ServiceLocator._transientServices[serviceType] = factory
        return True

    @staticmethod
    def tryResolve(serviceType: Type[T], **kwargs) -> T:
        """
        Try to resolve the requested service type by first searching registered
        singleton and then registered transient configurations.

        :param serviceType: _description_
        :type serviceType: _type_
        :return: _description_
        :rtype: _type_
        """
        # try to resolve as singleton
        instance = ServiceLocator._singletonServices.get(serviceType, None)
        if isinstance(instance, serviceType):
            return instance

        # try to resolve as transient
        factory = ServiceLocator._transientServices.get(serviceType, None)
        if factory is None:
            raise InvalidServiceConfiguration(serviceType)
        sig = signature(factory)
        arguments: Dict[str, object] = {}
        # try to instantiate an instance from the factory and given kwargs or
        # default parameters of the factory - additional kwargs are ignored
        for param in sig.parameters:
            try:
                arguments[param] = kwargs[param]
            except KeyError as exc:
                if (arg := sig.parameters[param].default) != Parameter.empty:
                    arguments[param] = arg
                else:
                    raise InvalidServiceConfiguration(serviceType) from exc
        instance = factory(**arguments)
        if isinstance(instance, serviceType):
            return instance

        # resolving failed
        raise InvalidServiceConfiguration(serviceType)
