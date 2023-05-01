"""
This module contains the resources necessary for the tests of the PyZEAL
project. The resources are provided as a dictionary mapping function names to
triples of holomorphic target functions, their derivatives, and their roots in
a certain domain of the complex plane.

Authors:\n
- Luca Wasmuth\n
"""

from dataclasses import dataclass
from functools import partial
from typing import Dict, Tuple, cast

import numpy as np

from pyzeal.pyzeal_types.filter_types import FilterTypes
from pyzeal.pyzeal_types.root_types import tHoloFunc, tVec
from pyzeal.settings.ram_settings_service import RAMSettingsService
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.containers.rounding_container import RoundingContainer
from pyzeal.utils.factories.container_factory import ContainerFactory
from pyzeal.utils.root_context import RootContext
from pyzeal.utils.service_locator import ServiceLocator

ServiceLocator.registerAsTransient(SettingsService, RAMSettingsService)


# dictionary mapping function names to functions, their derivatives, expected
# roots, and the real/imaginary ranges where the roots should be searched
@dataclass
class TestData:
    "Container holding test data sets."
    testFunc: tHoloFunc
    testFuncDerivative: tHoloFunc
    expectedRoots: Tuple[complex, ...]
    reRan: Tuple[float, float]
    imRan: Tuple[float, float]
    precision: Tuple[int, int]


def buildContextFromData(data: TestData) -> RootContext:
    """
    Convenience function building a root finding context from given test data.

    :param data: the data used for context building
    """
    # build a simple container for the context
    container = RoundingContainer(precision=data.precision)
    # ContainerFactory.registerPreDefinedFilter(
    #     container, filterType=FilterTypes.FUNCTION_VALUE_ZERO
    # )
    ContainerFactory.registerPreDefinedFilter(
        container, filterType=FilterTypes.ZERO_IN_BOUNDS
    )

    # assemble the context from the data
    deltaRe, deltaIm = data.precision
    reRan, imRan = data.reRan, data.imRan
    reRan = reRan[0] - 0.001, reRan[1] + 0.002
    imRan = imRan[0] - 0.003, imRan[1] + 0.004
    return RootContext(
        f=data.testFunc,
        df=data.testFuncDerivative,
        container=container,
        precision=(deltaRe + 1, deltaIm + 1),
        reRan=reRan,
        imRan=imRan,
    )


localTestFunctions: Dict[str, TestData] = {
    "x^2-1": TestData(
        testFunc=lambda x: cast(tVec, x**2 - 1),
        testFuncDerivative=lambda x: 2 * x,
        expectedRoots=(-1, 1),
        reRan=(-3, 2),
        imRan=(-4, 5),
        precision=(3, 3),
    ),
    "x^2+1": TestData(
        testFunc=lambda x: cast(tVec, x**2 + 1),
        testFuncDerivative=lambda x: 2 * x,
        expectedRoots=(1j, -1j),
        reRan=(-5, 5),
        imRan=(-3, 3),
        precision=(3, 3),
    ),
    "x^2": TestData(
        testFunc=lambda x: cast(tVec, x**2),
        testFuncDerivative=lambda x: cast(tVec, 2 * x),
        expectedRoots=(),
        reRan=(1, 2),
        imRan=(-1, 1),
        precision=(5, 5),
    ),
    "(2x/5)^2+1": TestData(
        lambda x: cast(tVec, (2 * x / 5) ** 2 + 1),
        lambda x: 8 * x / 25,
        (2.5j, -2.5j),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "x^4-1": TestData(
        lambda x: cast(tVec, x**4 - 1),
        lambda x: cast(tVec, 4 * x**3),
        (1, -1, 1j, -1j),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "x^3+x^2+x+1": TestData(
        lambda x: cast(tVec, 1 * x**3 + x**2 + x + 1),
        lambda x: cast(tVec, 3 * x**2 + 2 * x + 1),
        (-1, 1j, -1j),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "x^2+26.01": TestData(
        lambda x: cast(tVec, x**2 + 26.01),
        lambda x: 2 * x,
        (),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "x^4-6.25x+9": TestData(
        lambda x: cast(
            tVec, (x - np.sqrt(2)) * (x + np.sqrt(2)) * (x - 1.5) * (x + 1.5)
        ),
        lambda x: cast(tVec, 4 * x**3 - 8.5 * x),
        (np.sqrt(2), -np.sqrt(2), 1.5, -1.5),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "x^5-4x+2": TestData(
        testFunc=lambda x: cast(tVec, 1 * x**5 - 4 * x + 2),
        testFuncDerivative=lambda x: cast(tVec, 5 * x**4 - 4),
        expectedRoots=(
            0.508499484,
            -1.51851215,
            1.2435963,
            -0.116791 - 1.43844769j,
            -0.116791 + 1.43844769j,
        ),
        reRan=(-7.1, 6.2),
        imRan=(-9.3, 8.4),
        precision=(3, 3),
    ),
    "x^3-0.01x": TestData(
        lambda x: cast(tVec, 1 * (x - 0.1) * (x + 0.1) * x),
        lambda x: cast(tVec, 3 * x**2 - 0.01),
        (0.1, 0, -0.1),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "x^30": TestData(
        lambda x: x**30,
        lambda x: cast(tVec, 30 * x**29),
        (0,),
        (-5.009, 5.01),
        (-5.02, 5.03),
        precision=(3, 3),
    ),
    "x^50": TestData(
        lambda x: x**50,
        lambda x: cast(tVec, 50 * x**49),
        (0,),
        (-5.009, 5.018),
        (-5.027, 5.036),
        precision=(3, 3),
    ),
    "x^100": TestData(
        lambda x: x**100,
        lambda x: cast(tVec, 100 * x**99),
        (0,),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "1e6 * x^100": TestData(
        lambda x: cast(tVec, 1e6 * x**100),
        lambda x: cast(tVec, 1e8 * x**99),
        (0,),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "x^2-25": TestData(
        lambda x: cast(tVec, 1 * (x - 5) * (x + 5)),
        lambda x: 2 * x,
        (5, -5),
        (-5.1, 5.2),
        (-5.3, 5.4),
        precision=(3, 3),
    ),
    "x^2+(0.000024414 - i)x": TestData(
        lambda x: x * (x + 0.000024414 - 1j),
        lambda x: cast(tVec, 2 * x + 0.000024414 - 1j),
        (0, -0.000024414 + 1j),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "poly": TestData(
        testFunc=lambda x: cast(
            tVec,
            (x + 4.652) * (x + 0.333 + 1.5j) * (x + 1.5j) * x * (x - 4.768j),
        ),
        testFuncDerivative=lambda x: cast(
            tVec,
            (
                (x + 0.333 + 1.5j) * (x + 1.5j) * x * (x - 4.768j)
                + (x + 4.652) * (x + 1.5j) * x * (x - 4.768j)
                + (x + 4.652) * (x + 0.333 + 1.5j) * x * (x - 4.768j)
                + (x + 4.652) * (x + 0.333 + 1.5j) * (x + 1.5j) * (x - 4.768j)
                + (x + 4.652) * (x + 0.333 + 1.5j) * (x + 1.5j) * x
            ),
        ),
        expectedRoots=(-4.652, -0.333 - 1.5j, -1.5j, 0, 4.768j),
        reRan=(-6.2, 7.4),
        imRan=(-8.6, 9.8),
        precision=(3, 3),
    ),
    "sin(x)": TestData(
        np.sin,
        np.cos,
        (-1 * np.pi, 0, np.pi),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "exp(x)": TestData(np.exp, np.exp, (), (-5, 5), (-5, 5), precision=(3, 3)),
    "exp(x)-1": TestData(
        testFunc=lambda x: cast(tVec, np.exp(np.pi * x / 2) - 1),
        testFuncDerivative=lambda x: cast(
            tVec, np.pi * np.exp(np.pi * x / 2) / 2
        ),
        expectedRoots=(-4j, 0, 4j),
        reRan=(-5, 5),
        imRan=(-5, 5),
        precision=(3, 3),
    ),
    "tan(x/10)": TestData(
        lambda x: cast(tVec, np.tan(x / 10)),
        lambda x: cast(tVec, 1 / (10 * np.cos(x / 10) ** 2)),
        (0,),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "tan(x/100)": TestData(
        lambda x: cast(tVec, np.tan(x / 100)),
        lambda x: cast(tVec, 1 / (100 * np.cos(x / 100) ** 2)),
        (0,),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "sin x cos": TestData(
        lambda x: cast(tVec, 2 * np.sin(x) * np.cos(x)),
        lambda x: cast(tVec, 2 * np.cos(x) ** 2 - 2 * np.sin(x) ** 2),
        (
            0,
            np.pi,
            -np.pi,
            0.5 * np.pi,
            1.5 * np.pi,
            -0.5 * np.pi,
            -1.5 * np.pi,
        ),
        (-5.0001, 5.0102),
        (-5.0003, 5.0204),
        precision=(4, 4),
    ),
    "log and sinh composition": TestData(
        lambda x: cast(tVec, np.log(np.sinh(0.2 * x) ** 2 + 1)),
        lambda x: cast(
            tVec,
            0.4
            * np.sinh(0.2 * x)
            * np.cosh(0.2 * x)
            / (1 + np.sinh(0.2 * x) ** 2),
        ),
        (0,),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "scaled exp": TestData(
        lambda x: cast(tVec, np.exp(np.pi * x) - 1),
        lambda x: cast(tVec, np.pi * np.exp(np.pi * x)),
        (-2j, 0, 2j),
        (-3, 3),
        (-3, 3),
        precision=(3, 3),
    ),
    "moved root": TestData(
        lambda x: cast(tVec, np.emath.sqrt(x - 10)),
        lambda x: cast(tVec, 0.5 / np.emath.sqrt(x - 10)),
        (),
        (-6, 6),
        (-3, 7),
        precision=(5, 5),
    ),
    "log(x^2+26)": TestData(
        lambda x: cast(tVec, np.log(x**2 + 26)),
        lambda x: cast(tVec, 2 * x / (x**2 + 26)),
        (-5j, 5j),
        (-5.01, 5.02),
        (-5.03, 5.04),
        precision=(3, 3),
    ),
    "20arctan(x/10)": TestData(
        lambda x: cast(tVec, 20 * np.arctan(x / 10)),
        lambda x: cast(tVec, 2 / (1 + (x / 10) ** 2)),
        (0,),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
    "exp(arctan(x/10)-1)": TestData(
        lambda x: cast(tVec, np.exp(np.arctan(x / 10)) - 1),
        lambda x: cast(
            tVec, 0.1 * np.exp(np.arctan(x / 10)) / (1 + (x / 10) ** 2)
        ),
        (0,),
        (-5, 5),
        (-5, 5),
        precision=(3, 3),
    ),
}


# wrap lambdas inside partial so multiprocessing works correctly
def f(name: str, x: tVec) -> tVec:
    """
    Evaluate the function `name` with argument `x`. Use with `partial` to
    get a function in `x`.

    :param name: Function name
    :param x: Point for function evaluation
    :return: `name` evaluated at `x`
    """
    return localTestFunctions[name].testFunc(x)


def df(name: str, x: tVec) -> tVec:
    """
    Evaluate the derivative of function `name` at `x`.

    :param name: Function name
    :param x: Point for function evaluation
    :return: Derivative of `name` evaluated at `x`
    """
    return localTestFunctions[name].testFuncDerivative(x)


testFunctions: Dict[str, TestData] = {}
for key, item in localTestFunctions.items():
    testFunctions[key] = TestData(
        testFunc=partial(f, key),
        testFuncDerivative=partial(df, key),
        expectedRoots=localTestFunctions[key].expectedRoots,
        reRan=localTestFunctions[key].reRan,
        imRan=localTestFunctions[key].imRan,
        precision=localTestFunctions[key].precision,
    )
