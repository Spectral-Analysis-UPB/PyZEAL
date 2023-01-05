"""
This module provides named constants used to identify concrete root finding
algorithms in any instance where such an algorithm needs to be specified.

Authors:\n
- Philipp Schuette\n
"""

from enum import Enum


class AlgorithmTypes(Enum):
    "Enumeration containing named constants identifying available algorithms."
    NEWTON_GRID = 0
    SIMPLE_ARGUMENT = 1
    SIMPLE_ARGUMENT_NEWTON = 2
