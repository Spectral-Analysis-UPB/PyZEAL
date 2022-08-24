from typing import Callable, Optional, Tuple, List
from numpy import complex128
from numpy.typing import NDArray
import numpy as np
import scipy as sp

from rootfinder.rootfinder import RootFinder

class NewtonGridRootFinder(RootFinder):
    r"""
    Root finder based on the Newton algorithm, with starting points
    in an evenly spaced grid
    """

    def __init__(self, f: Callable[[float], float], df: Callable[[float], float]) -> None:
        r"""
        :param f: differentiable function
        :type f: Callable[[float], float]
        :param df: derivative of f
        :type df: Callable[[float], float]
        """
        super().__init__()
        self.f : Callable[[float], float] = f
        self.df : Callable[[float], float] = df
        self.roots : NDArray[complex128] = np.array([], dtype=complex128)

    def calcRoots(self, reRan: Tuple[float, float], imRan: Tuple[float, float],
                  epsCplx: Optional[complex] = 10**-6) -> None:
        numSamplePoints : int = 50
        rePoints : NDArray[complex128] = np.linspace(reRan[0], reRan[1], numSamplePoints)
        imPoints : NDArray[complex128] = np.linspace(imRan[0], imRan[1], numSamplePoints)
        for u in rePoints:
            for v in imPoints:
                try:
                    result : complex128 = sp.optimize.newton(self.f, u+v*1j, self.df)
                    self.roots = np.append(self.roots, [result])
                    if result.real < -13:
                        print(u,v)
                except RuntimeError:
                    pass
        # Remove roots that are closer than epsCplx to each other
        filteredRoots : NDArray[complex128] = np.empty(0, dtype=complex128)
        for z in self.roots:
            distances : List[float] = [np.abs(r-z) for r in filteredRoots]
            if min(distances, default=epsCplx) >= epsCplx:
                filteredRoots = np.append(filteredRoots, [z])
        self.roots = filteredRoots
        
        # Remove roots that are outside the given search area
        filteredRoots = np.empty(0, dtype=complex128)
        for z in self.roots:
            u : float = z.real
            v : float = z.imag
            if reRan[0] <= u <= reRan[1] and imRan[0] <= v <= imRan[1]:
                filteredRoots = np.append(filteredRoots, [z])
        self.roots = filteredRoots

    def getRoots(self) -> NDArray[complex128]:
        return self.roots