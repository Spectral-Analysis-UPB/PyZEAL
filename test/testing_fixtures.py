"""
TODO
"""

from pyzeal import ParallelRootFinder, RootFinder, RootFinderInterface
from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_types.container_types import ContainerTypes
from pyzeal_types.filter_types import FilterTypes

from .testing_resources import testFunctions


def newtonGridFinder(
    testName: str,
    numSamplePoints: int = 20,
    parallel: bool = False,
    derivativeFree: bool = False,
) -> RootFinderInterface:
    """
    TODO
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
    testName: str, parallel: bool = False
) -> RootFinderInterface:
    """
    TODO
    """
    holoRF: RootFinderInterface
    if parallel:
        holoRF = ParallelRootFinder(
            testFunctions[testName][0],
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT,
            verbose=False,
        )
    else:
        holoRF = RootFinder(
            testFunctions[testName][0],
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT,
            verbose=False,
        )
    holoRF.setRootFilter(filterType=FilterTypes.FUNCTION_VALUE_ZERO)
    holoRF.setRootFilter(filterType=FilterTypes.ZERO_IN_BOUNDS)
    return holoRF


def simpleArgumentNewtonRootFinder(
    testName: str, parallel: bool = False
) -> RootFinderInterface:
    """
    TODO
    """
    holoNewtonRF: RootFinderInterface
    if parallel:
        holoNewtonRF = ParallelRootFinder(
            testFunctions[testName][0],
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT_NEWTON,
            verbose=False,
        )
    else:
        holoNewtonRF = RootFinder(
            testFunctions[testName][0],
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT_NEWTON,
            verbose=False,
        )
    holoNewtonRF.setRootFilter(filterType=FilterTypes.FUNCTION_VALUE_ZERO)
    holoNewtonRF.setRootFilter(filterType=FilterTypes.ZERO_IN_BOUNDS)
    return holoNewtonRF
