"""
This module provides named constants used to identify concrete root container
implementations in any instance where such a container is required.

Authors:\n
- Philipp Schuette\n
"""

from enum import Enum


class ContainerTypes(Enum):
    "Enumeration containing named constants identifying available containers."
    ROUNDING_CONTAINER = 0
