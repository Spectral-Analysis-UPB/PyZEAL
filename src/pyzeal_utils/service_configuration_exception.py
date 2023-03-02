"""
Module service_configuration_exception.py from the package PyZEAL.
TODO

Authors:\n
- Philipp Schuette\n
"""

from typing import Type


class InvalidServiceConfiguration(Exception):
    """
    This exception should be raised if invalid configurations are encountered
    during registration/resolving of services with ServiceLocator.
    """

    def __init__(self, serviceType: Type) -> None:
        """
        Initialize a new `InvalidServiceConfiguration` exception.

        :param serviceType: the faulty service
        :type serviceType: Type
        """
        super().__init__("invalid service request: " + str(serviceType))
