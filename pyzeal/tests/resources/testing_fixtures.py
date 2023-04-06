"""
Provide rootfinder setup methods with common settings for testing purposes.
"""

from typing import List

import pytest

from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.pyzeal_types.filter_types import FilterTypes
from pyzeal.rootfinders import (
    ParallelRootFinder,
    RootFinder,
    RootFinderInterface,
)
from pyzeal.tests.resources.testing_resources import testFunctions
from pyzeal.utils.filter_context import FilterContext


def newtonGridFinder(
    testName: str,
    numSamplePoints: int = 20,
    parallel: bool = False,
    derivativeFree: bool = False,
) -> RootFinderInterface:
    """
    Returns a NEWTON_GRID RootFinder for the test case `testName`

    :param testName: Test case name
    :param numSamplePoints: `numSamplePoints` passed to the RootFinder,
        defaults to 20
    :param parallel: Set to `True` if the RootFinder should search in
        parallel, defaults to False
    :param derivativeFree: Set to `True` if the RootFinder should operate
        without the derivative, defaults to False
    :return: Initialized RootFinder
    """
    f = testFunctions[testName][0]
    df = testFunctions[testName][1] if not derivativeFree else None
    gridRF: RootFinderInterface
    if parallel:
        gridRF = ParallelRootFinder(
            f,
            df,
            numSamplePoints=numSamplePoints,
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.NEWTON_GRID,
        )
    else:
        gridRF = RootFinder(
            f,
            df,
            numSamplePoints=numSamplePoints,
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.NEWTON_GRID,
        )
    gridRF.setRootFilter(filterType=FilterTypes.FUNCTION_VALUE_ZERO)
    gridRF.setRootFilter(filterType=FilterTypes.ZERO_IN_BOUNDS)
    return gridRF


def simpleArgumentRootFinder(
    testName: str,
    parallel: bool = False,
    estimatorType: EstimatorTypes = EstimatorTypes.SUMMATION_ESTIMATOR,
) -> RootFinderInterface:
    """
    Returns a SIMPLE_ARGUMENT RootFinder for the test case `testName`

    :param testName: Test case name
    :param parallel: Set to `True` if the RootFinder should search in parallel,
        defaults to False
    :return: Initialized RootFinder
    """
    holoRF: RootFinderInterface
    f = testFunctions[testName][0]
    df = testFunctions[testName][1]
    if parallel:
        holoRF = ParallelRootFinder(
            f,
            df,
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT,
            estimatorType=estimatorType,
            verbose=False,
        )
    else:
        holoRF = RootFinder(
            f,
            df,
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT,
            estimatorType=estimatorType,
            verbose=False,
        )
    holoRF.setRootFilter(filterType=FilterTypes.FUNCTION_VALUE_ZERO)
    holoRF.setRootFilter(filterType=FilterTypes.ZERO_IN_BOUNDS)
    return holoRF


def simpleArgumentNewtonRootFinder(
    testName: str,
    parallel: bool = False,
    estimatorType: EstimatorTypes = EstimatorTypes.SUMMATION_ESTIMATOR,
) -> RootFinderInterface:
    """
    Returns a SIMPLE_ARGUMENT RootFinder for the test case `testName`

    :param testName: Test case name
    :param parallel: Set to `True` if the RootFinder should search in parallel,
        defaults to False
    :return: Initialized RootFinder
    """
    holoNewtonRF: RootFinderInterface
    f = testFunctions[testName][0]
    df = testFunctions[testName][1]
    if parallel:
        holoNewtonRF = ParallelRootFinder(
            f,
            df,
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT_NEWTON,
            estimatorType=estimatorType,
            verbose=False,
        )
    else:
        holoNewtonRF = RootFinder(
            f,
            df,
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT_NEWTON,
            estimatorType=estimatorType,
            verbose=False,
        )
    holoNewtonRF.setRootFilter(filterType=FilterTypes.FUNCTION_VALUE_ZERO)
    holoNewtonRF.setRootFilter(filterType=FilterTypes.ZERO_IN_BOUNDS)
    return holoNewtonRF
