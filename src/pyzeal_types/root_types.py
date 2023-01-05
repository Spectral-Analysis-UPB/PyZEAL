"""
This module provides type aliases used throughout the PyZEAL project.

Authors:\n
- Philipp Schuette\n
"""

from typing import List, Tuple, Union

import numpy as np
from numpy.typing import NDArray

# general purpose types used throughout
tScal = Union[float, complex]
tVec = NDArray[np.complex128]

# types used for rootfinder results and internally
tRecGrid = Tuple[
    NDArray[np.complex128],
    NDArray[np.complex128],
    NDArray[np.complex128],
    NDArray[np.complex128],
]

tResVec = Union[List[Tuple[tScal, int]], tVec]
tErrVec = Union[List[tScal], tVec]
