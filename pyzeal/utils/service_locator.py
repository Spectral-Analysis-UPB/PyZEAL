"""
Module service_locator.py from the package PyZEAL.
This module provides a way to register and locate services used throughout
the project, to enable loading additional services for the plugin system.

Authors:\n
- Philipp Schuette\n
"""

from inspect import Parameter, signature
from typing import Callable, Dict, Type, TypeVar

from pyzeal.utils.configuration_exception import InvalidServiceConfiguration

# type variable for the various signatures of ServiceLocator
T = TypeVar("T")


class ServiceLocator:
    """
    Static locator class used to add and resolve services.
    """

    _transientServices: Dict[Type[object], Callable[..., object]] = {}

    _singletonServices: Dict[Type[object], object] = {}

    _sealed: bool = False

    @staticmethod
    def registerAsSingleton(serviceType: Type[T], instance: T) -> bool:
        """
        Register service `instance` as a singleton service, meaning only one
        instance exists.

        :param serviceType: Type of service
        :param instance: Service instance
        :raises ValueError: If the service locator is sealed, no new services
            can be registered.
        :return: `True` if the service has been successfully registered.
        """
        if ServiceLocator.isSealed():
            raise ValueError(
                f"cannot register singleton {serviceType} on sealed locator!"
            )
        if isinstance(instance, serviceType):
            ServiceLocator._singletonServices[serviceType] = instance
            return True
        return False

    @staticmethod
    def registerAsTransient(
        serviceType: Type[T], factory: Callable[..., T]
    ) -> bool:
        """
        Register a transient service.

        :param serviceType: Type of service to register.
        :param factory: Factory for the given service
        :raises ValueError: If the service locator is sealed, no new services
            can be registered.
        :return: `True` if the service has been successfully registered.
        """
        if ServiceLocator.isSealed():
            raise ValueError(
                f"cannot register transient {serviceType} on sealed locator!"
            )
        ServiceLocator._transientServices[serviceType] = factory
        return True

    # TODO: create dedicated locator tests
    @staticmethod
    def tryResolve(serviceType: Type[T], **kwargs: object) -> T:
        """
        Try to resolve the requested service type by first searching registered
        singleton and then registered transient configurations.

        :param serviceType: Type of service to resolve
        :raises InvalidServiceConfiguration: If the given `serviceType` can
            not be resolved, an exception is raised
        :return: An instance of the given service. If the service is
            transient, the factory is called with the parameters given
            by `**kwargs`.
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
            except KeyError:
                if (arg := sig.parameters[param].default) != Parameter.empty:
                    arguments[param] = arg
                else:
                    arguments[param] = ServiceLocator.tryResolve(
                        sig.parameters[param].annotation
                    )
        instance = factory(**arguments)
        if isinstance(instance, serviceType):
            return instance

        # resolving failed
        raise InvalidServiceConfiguration(serviceType)

    @staticmethod
    def seal() -> None:
        """
        Seal the service locator to prevent additional services from
        being registered.

        :raises ValueError: Raises an exception if the service locator
            has already been sealed.
        """
        if ServiceLocator._sealed:
            raise ValueError("cannot re-seal an already sealed locator!")
        ServiceLocator._sealed = True

    @staticmethod
    def isSealed() -> bool:
        """
        Return `True` if the service locator is sealed.

        :return: `True` if the service locator is sealed.
        """
        return ServiceLocator._sealed
