"""
This module contains the resources necessary for the tests of the PyZEAL
project. The resources are provided as a dictionary mapping function names to
triples of holomorphic target functions, their derivatives, and their roots in
a certain domain of the complex plane.

Authors:\n
- Luca Wasmuth\n
"""

from functools import partial
from typing import Dict, Tuple, cast

import numpy as np

from pyzeal.pyzeal_types.root_types import tHoloFunc, tVec
from pyzeal.settings.ram_settings_service import RAMSettingsService
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.service_locator import ServiceLocator

# the extends of the domain which contains exactly the specified roots for the
# given functions
RE_RAN = (-5, 5)
IM_RAN = (-5, 5)

ServiceLocator.registerAsTransient(SettingsService, RAMSettingsService)

localTestFunctions: Dict[
    str,
    Tuple[
        tHoloFunc,
        tHoloFunc,
        Tuple[complex, ...],
    ],
] = {
    "x^2-1": (lambda x: cast(tVec, x**2 - 1), lambda x: 2 * x, (-1, 1)),
    "x^2+1": (lambda x: cast(tVec, x**2 + 1), lambda x: 2 * x, (1j, -1j)),
    "(2x/5)^2+1": (
        lambda x: cast(tVec, (2 * x / 5) ** 2 + 1),
        lambda x: 8 * x / 25,
        (2.5j, -2.5j),
    ),
    "x^4-1": (
        lambda x: cast(tVec, x**4 - 1),
        lambda x: cast(tVec, 4 * x**3),
        (1, -1, 1j, -1j),
    ),
    "x^3+x^2+x+1": (
        lambda x: cast(tVec, 1 * x**3 + x**2 + x + 1),
        lambda x: cast(tVec, 3 * x**2 + 2 * x + 1),
        (-1, 1j, -1j),
    ),
    "x^2+26.01": (lambda x: cast(tVec, x**2 + 26.01), lambda x: 2 * x, ()),
    "x^4-6.25x+9": (
        lambda x: cast(
            tVec, (x - np.sqrt(2)) * (x + np.sqrt(2)) * (x - 1.5) * (x + 1.5)
        ),
        lambda x: cast(tVec, 4 * x**3 - 8.5 * x),
        (np.sqrt(2), -np.sqrt(2), 1.5, -1.5),
    ),
    "x^5-4x+2": (
        lambda x: cast(tVec, 1 * x**5 - 4 * x + 2),
        lambda x: cast(tVec, 5 * x**4 - 4),
        (
            0.508499484,
            -1.51851215,
            1.2435963,
            -0.116791 - 1.43844769j,
            -0.116791 + 1.43844769j,
        ),
    ),
    "x^3-0.01x": (
        lambda x: cast(tVec, 1 * (x - 0.1) * (x + 0.1) * x),
        lambda x: cast(tVec, 3 * x**2 - 0.01),
        (0.1, 0, -0.1),
    ),
    "x^30": (lambda x: x**30, lambda x: cast(tVec, 30 * x**29), (0,)),
    "x^50": (lambda x: x**50, lambda x: cast(tVec, 50 * x**49), (0,)),
    "x^100": (lambda x: x**100, lambda x: cast(tVec, 100 * x**99), (0,)),
    "1e6 * x^100": (
        lambda x: cast(tVec, 1e6 * x**100),
        lambda x: cast(tVec, 1e8 * x**99),
        (0,),
    ),
    "x^2-25": (
        lambda x: cast(tVec, 1 * (x - 5) * (x + 5)),
        lambda x: 2 * x,
        (5, -5),
    ),
    "x^2+(0.000024414 - i)x": (
        lambda x: x * (x + 0.000024414 - 1j),
        lambda x: cast(tVec, 2 * x + 0.000024414 - 1j),
        (0, -0.000024414 + 1j),
    ),
    "poly": (
        lambda x: cast(
            tVec,
            (x + 4.652) * (x + 0.333 + 1.5j) * (x + 1.5j) * x * (x - 4.768j),
        ),
        lambda x: cast(
            tVec,
            (
                (x + 0.333 + 1.5j) * (x + 1.5j) * x * (x - 4.768j)
                + (x + 4.652) * (x + 1.5j) * x * (x - 4.768j)
                + (x + 4.652) * (x + 0.333 + 1.5j) * x * (x - 4.768j)
                + (x + 4.652) * (x + 0.333 + 1.5j) * (x + 1.5j) * (x - 4.768j)
                + (x + 4.652) * (x + 0.333 + 1.5j) * (x + 1.5j) * x
            ),
        ),
        (-4.652, -0.333 - 1.5j, -1.5j, 0, 4.768j),
    ),
    "sin(x)": (np.sin, np.cos, (-1 * np.pi, 0, np.pi)),
    "exp(x)": (np.exp, np.exp, ()),
    "exp(x)-1": (
        lambda x: cast(tVec, np.exp(np.pi * x / 2) - 1),
        lambda x: cast(tVec, np.pi * np.exp(np.pi * x / 2) / 2),
        (-4j, 0, 4j),
    ),
    "tan(x/10)": (
        lambda x: cast(tVec, np.tan(x / 10)),
        lambda x: cast(tVec, 1 / (10 * np.cos(x / 10) ** 2)),
        (0,),
    ),
    "tan(x/100)": (
        lambda x: cast(tVec, np.tan(x / 100)),
        lambda x: cast(tVec, 1 / (100 * np.cos(x / 100) ** 2)),
        (0,),
    ),
    "sin x cos": (
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
    ),
    "log and sinh composition": (
        lambda x: cast(tVec, np.log(np.sinh(0.2 * x) ** 2 + 1)),
        lambda x: cast(
            tVec,
            0.4
            * np.sinh(0.2 * x)
            * np.cosh(0.2 * x)
            / (1 + np.sinh(0.2 * x) ** 2),
        ),
        (0,),
    ),
    "square root of exp": (
        lambda x: cast(tVec, np.emath.sqrt(np.exp(2 * np.pi * x / 4)) - 1),
        lambda x: cast(
            tVec, 0.25 * np.pi / np.emath.sqrt(np.exp(2 * np.pi * x / 4))
        ),
        (0, -4j, 4j),
    ),
    "log(x^2+26)": (
        lambda x: cast(tVec, np.log(x**2 + 26)),
        lambda x: cast(tVec, 2 * x / (x**2 + 26)),
        (-5j, 5j),
    ),
    "20arctan(x/10)": (
        lambda x: cast(tVec, 20 * np.arctan(x / 10)),
        lambda x: cast(tVec, 2 / (1 + (x / 10) ** 2)),
        (0,),
    ),
    "exp(arctan(x/10)-1)": (
        lambda x: cast(tVec, np.exp(np.arctan(x / 10)) - 1),
        lambda x: cast(
            tVec, 0.1 * np.exp(np.arctan(x / 10)) / (1 + (x / 10) ** 2)
        ),
        (0,),
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
    return localTestFunctions[name][0](x)


def df(name: str, x: tVec) -> tVec:
    """
    Evaluate the derivative of function `name` at `x`.

    :param name: Function name
    :param x: Point for function evaluation
    :return: Derivative of `name` evaluated at `x`
    """
    return localTestFunctions[name][1](x)


testFunctions = {}
for key, item in localTestFunctions.items():
    testFunctions[key] = (
        partial(f, key),
        partial(df, key),
        localTestFunctions[key][2],
    )
