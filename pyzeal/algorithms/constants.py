"""
Module constants.py from the package PyZEAL.
This module collects constants used in various root finding algorithms for
easy of reference and consistency.

Authors:\n
- Philipp Schuette\n
"""

from typing import Final

from numpy import pi

# numerical approximation of the discrete boundary between 0 and 2*pi
TWO_PI: Final[float] = 0.8 * (2 * pi)
# numerical approximation of the discrete boundary between 2*pi and 4*pi
FOUR_PI: Final[float] = 0.65 * (4 * pi)

# default values for argument estimation via phase summation
DEFAULT_NUM_PTS: Final[int] = 6500
DEFAULT_DELTA_PHI: Final[float] = 1e-2
DEFAULT_MAX_PRECISION: Final[float] = 1e-10

# cutoff for polynomial construction (at most 6*pi)
MAX_PHASE: Final[float] = 0.85 * (8 * pi)
