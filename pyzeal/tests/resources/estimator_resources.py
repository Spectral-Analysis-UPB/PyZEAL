"""
This module contains resources for estimator tests: A utility function to
generate `RootContext`s as well as test cases for argument estimation on a
rectangular contour and along a straight line.
"""

from typing import Dict, Tuple, cast

import numpy as np

from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.root_types import tHoloFunc, tVec
from pyzeal.settings.ram_settings_service import RAMSettingsService
from pyzeal.settings.settings_service import SettingsService
from pyzeal.utils.factories.container_factory import ContainerFactory
from pyzeal.utils.root_context import RootContext
from pyzeal.utils.service_locator import ServiceLocator

ServiceLocator.registerAsTransient(SettingsService, RAMSettingsService)


functions: dict[str, Tuple[tHoloFunc, tHoloFunc]] = {
    "2x^2+3": (lambda z: 2 * z**2 + 3, lambda z: 4 * z),
    "sin(x)": (
        lambda z: cast(tVec, -2.4 * np.sin(z)),
        lambda z: cast(tVec, -2.4 * np.cos(z)),
    ),
    "exp(ix)": (
        lambda z: cast(tVec, 5.1j * np.exp(z * 1j)),
        lambda z: cast(tVec, 5.1j * np.exp(z * 1j) * 1j),
    ),
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


rectangleCases: Dict[str, Tuple[RootContext, int, float]] = {
    "2x^2+3,(-1,1)x(-1,3)": (
        generateRootContext("2x^2+3", (-1, 1), (-1, 3)),
        0,
        2 * np.pi,
    ),
    "sin(x),(-5,5)x(-5,5)": (
        generateRootContext("sin(x)", (-5, 5), (-5, 5)),
        0,
        6 * np.pi,
    ),
    "exp(ix),(-1,2)x(-3,4)": (
        generateRootContext("exp(ix)", (-1, 2), (-3, 4)),
        0,
        0.0,
    ),
}

lineCases: Dict[str, Tuple[RootContext, int, complex, complex, complex]] = {
    "2x^2+3,-1+1j:1+1j": (
        generateRootContext("2x^2+3", (-1, 1), (-1, 1)),
        0,
        -1 + 1j,
        1 + 1j,
        -1j * np.log((3 + 4j) / (3 - 4j)),
    ),
    "2x^2+3,-1+1j:-1-1j": (
        generateRootContext("2x^2+3", (-1, 1), (-1, 1)),
        0,
        -1 + 1j,
        -1 - 1j,
        1j * np.log((-3 + 4j) / (-3 - 4j)),
    ),
    "sin(x),1j:3j": (
        generateRootContext("sin(x)", (-1, 1), (1, 3)),
        0,
        0 + 1j,
        0 + 3j,
        -1j * np.log(np.sinh(3) / np.sinh(1)),
    ),
    "sin(x),1:3": (
        generateRootContext("sin(x)", (1, 3), (-1, 1)),
        0,
        1 + 0j,
        3 + 0j,
        -1j * np.log(np.sin(3) / np.sin(1)),
    ),
    "exp(ix),-1-1j:-1+1j": (
        generateRootContext("exp(ix)", (-1, 1), (-1, 1)),
        0,
        -1 - 1j,
        -1 + 1j,
        2.0j,
    ),
    "exp(ix),-1-1j:1-1j": (
        generateRootContext("exp(ix)", (-1, 1), (-1, 1)),
        0,
        -1 - 1j,
        1 - 1j,
        2.0,
    ),
}
