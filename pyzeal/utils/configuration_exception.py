"""
Module `service_configuration_exception.py` from the package `PyZEAL`.

This module contains the generic exception signaling that an invalid
configuration has been received.

Authors:\n
- Philipp Schuette\n
"""

from typing import Generic, Type, TypeVar

T = TypeVar("T")


class InvalidServiceConfiguration(Exception, Generic[T]):
    """
    This exception should be raised if invalid configurations are encountered
    during registration/resolving of services with ServiceLocator.
    """

    def __init__(self, serviceType: Type[T]) -> None:
        """
        Initialize a new `InvalidServiceConfiguration` exception.

        :param serviceType: the faulty service
        """
        super().__init__("invalid service request: " + str(serviceType))
