"""
This module provides type aliases used throughout the PyZEAL project.

Authors:\n
- Philipp Schuette\n
"""

from typing import Callable, Tuple

import numpy as np
from numpy.typing import NDArray

# general purpose type for numpy arrays with complex entries
tVec = NDArray[np.complex128]

# type of functions our root finding algorithms can handle
tHoloFunc = Callable[[tVec], tVec]

# type used to identify roots of holomorphic functions (point in the plane with
# its multiplicity)
tRoot = Tuple[complex, int]

# type of rectangular grid used internally in simple argument rootfinders
tRecGrid = Tuple[tVec, tVec, tVec, tVec]
