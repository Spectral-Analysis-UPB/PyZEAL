"""
This module provides named constants used to identify a predefined set of
filters to be applied with root containers. These filters should be applied
via the `ContainerFactory` static class and removed via the respective method
on container or root finder instances.

Authors:\n
- Philipp Schuette\n
"""

from enum import Enum


class FilterTypes(Enum):
    "Enumeration containing named constants identifying available filters."
    FUNCTION_VALUE_ZERO = "[function-value-zero]"
    ZERO_IN_BOUNDS = "[zero-in-bounds]"
