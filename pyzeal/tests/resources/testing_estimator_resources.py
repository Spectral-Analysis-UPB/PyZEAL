"""
This module contains resources for estimator tests. A utility function to
generate `RootContext`s aswell as test cases for argument estimation on a
rectangular contour and along a line.
"""

from functools import partial
from typing import Tuple, cast

import numpy as np

from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.root_types import tVec
from pyzeal.settings.ram_settings_service import RAMSettingsService
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.factories.container_factory import ContainerFactory
from pyzeal.utils.root_context import RootContext
from pyzeal.utils.service_locator import ServiceLocator

ServiceLocator.registerAsTransient(SettingsService, RAMSettingsService)


def f(n: int, z: tVec) -> tVec:
    """
    Wrapper for test case functions.
    """
    if n == 1:
        return 2 * z**2 + 3
    if n == 2:
        return np.sin(z)
    return cast(tVec, np.exp(1j * z))


def df(n: int, z: tVec) -> tVec:
    """
    Wrapper for test case derivatives.
    """
    if n == 1:
        return 4 * z
    if n == 2:
        return np.cos(z)
    return cast(tVec, 1j * np.exp(1j * z))


functions = {
    "2x^2+3": (partial(f, 1), partial(df, 1)),
    "sin(x)": (partial(f, 2), partial(df, 2)),
    "exp(ix)": (partial(f, 3), partial(df, 3)),
}


def generateRootContext(
    name: str, reRan: Tuple[float, float], imRan: Tuple[float, float]
) -> RootContext:
    """
    Generate a `RootContext` for the test case `name` with given search ranges.

    :param name: Test case name
    :param reRan: Real search range
    :param imRan: Imaginary search range
    :return: Generated `RootContext`
    """
    return RootContext(
        f=functions[name][0],
        df=functions[name][1],
        container=ContainerFactory.getConcreteContainer(
            containerType=ContainerTypes.ROUNDING_CONTAINER
        ),
        reRan=reRan,
        imRan=imRan,
        precision=(5, 5),
    )


rectangleCases = {
    "2x2^+3, (-1,1) x (-1,3)": (
        generateRootContext("2x^2+3", (-1, 1), (-1, 3)),
        0,
        (-1, 1),
        (-1, 3),
        2 * np.pi,
    ),
    "sin(x), (-5,5) x (-5,5)": (
        generateRootContext("sin(x)", (-5, 5), (-5, 5)),
        0,
        (-5, 5),
        (-5, 5),
        6 * np.pi,
    ),
}
lineCases = {
    "2x^2+3, -1+1j : 1+1j": (
        generateRootContext("2x^2+3", (-1, 1), (-1, 1)),
        0,
        -1 + 1j,
        1 + 1j,
        1.854590436,
    )
}
