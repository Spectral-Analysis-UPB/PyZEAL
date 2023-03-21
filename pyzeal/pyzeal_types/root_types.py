"""
Module `root_types` from the package `pyzeal.pyzeal_types`.

This module provides common type aliases used throughout the PyZEAL project.

Authors:\n
- Philipp Schuette\n
"""

from typing import Callable, Tuple

import numpy as np
from numpy.typing import NDArray
from typing_extensions import TypeAlias

# general purpose type for numpy arrays with complex entries
tVec: TypeAlias = NDArray[np.complex128]

# type of functions our root finding algorithms can handle
tHoloFunc: TypeAlias = Callable[[tVec], tVec]

# type used to identify roots of holomorphic functions (point in the plane with
# its multiplicity)
tRoot: TypeAlias = Tuple[complex, int]

# type of rectangular grid used internally in simple argument rootfinders
tRecGrid: TypeAlias = Tuple[tVec, tVec, tVec, tVec]
