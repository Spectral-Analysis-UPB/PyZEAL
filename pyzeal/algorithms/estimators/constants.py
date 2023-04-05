"""
Module constants.py from the package `pyzeal.algorithms.estimators`.

This module collects constants used in various argument estimators for ease of
reference and consistency.

Authors:\n
- Philipp Schuette\n
"""

from typing import Final

# number of sample points for integration
EXP_SAMPLE_POINTS: Final[int] = 10
# maximal sample points for integration
MAX_SAMPLE_POINTS: Final[int] = 21

# constant determining the refinement of complex arrays for large phi values
Z_REFINE: Final[int] = 100
# constant determining the maximal length of z-arrays
MAX_Z_LENGTH: Final[int] = 100
