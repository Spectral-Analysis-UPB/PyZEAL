"""
TODO

Authors:\n
- Philipp Schuette\n
"""

from typing import List, Tuple

from numpy import array, complex128, int32
from numpy.polynomial import Polynomial
from numpy.typing import NDArray

from pyzeal.algorithms.wrappers.polynomial_wrapper import PolynomialWrapper
from pyzeal.pyzeal_types.root_types import tVec


class ClassicalPolynomial(PolynomialWrapper):
    "Simple wrapper for the polynomial implementation provided by `numpy`."

    # docstr-coverage:inherited
    def getRootsWithOrders(
        self, precision: Tuple[int, int]
    ) -> Tuple[tVec, NDArray[int32]]:
        roots = Polynomial(self._coefficients).roots()
        uniqueRoots: List[complex] = []
        orders: List[int] = []

        for root in roots:
            new = True
            for i, oldRoot in enumerate(uniqueRoots):
                if abs(root.real - oldRoot.real) < 10 ** (
                    -precision[0]
                ) and abs(root.imag - oldRoot.imag) < 10 ** (-precision[1]):
                    orders[i] += 1
                    new = False
                    break

            if new:
                uniqueRoots.append(root)
                orders.append(1)

        return array(uniqueRoots, dtype=complex128), array(orders, dtype=int32)
