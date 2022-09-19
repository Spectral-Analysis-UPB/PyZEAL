import numpy as np
from rootfinder.newton_grid import NewtonGridRootFinder

class RootfindingSuite:
    testSuite = [
        (lambda x: x**2 - 1, lambda x: 2 * x, [-1, 1]),
        (lambda x: x**2 + 1, lambda x: 2 * x, [1j, -1j]),
        (lambda x: x**4 - 1, lambda x: 4 * x**3, [1, -1, 1j, -1j]),
        (np.sin, np.cos, [-1 * np.pi, 0, np.pi]),
        (np.exp, np.exp, []),
        (
            lambda x: x**5 - 4 * x + 2,
            lambda x: 5 * x**4 - 4,
            [
                0.508499484,
                -1.51851215,
                1.2435963,
                -0.116791 - 1.43844769j,
                -0.116791 + 1.43844769j,
            ],
        ),
    ]

    def TimeNewtonGridRootfinder(self):
        for tCase in self.testSuite:
            gridRF = NewtonGridRootFinder(tCase[0], tCase[1])
            gridRF.calcRoots([-5, 5], [-5, 5], precision=(3, 3))
    
    def TimeNewtonGridRootfinderDerivativeFree(self):
        for tCase in self.testSuite:
            gridRF = NewtonGridRootFinder(tCase[0], tCase[1])
            gridRF.calcRoots([-5, 5], [-5, 5], precision=(3, 3))