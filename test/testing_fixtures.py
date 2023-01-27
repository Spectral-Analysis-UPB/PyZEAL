from pyzeal import ParallelRootFinder, RootFinder
from pyzeal_logging.log_levels import LogLevel
from pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal_types.container_types import ContainerTypes
from pyzeal_types.filter_types import FilterTypes

from .testing_resources import testFunctions


def newtonGridFinder(testName: str, numSamplePoints=20, parallel=False):
    if parallel:
        gridRF = ParallelRootFinder(
            testFunctions[testName][0],
            testFunctions[testName][1],
            numSamplePoints=numSamplePoints,
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.NEWTON_GRID,
        )
    else:
        gridRF = RootFinder(
            testFunctions[testName][0],
            testFunctions[testName][1],
            numSamplePoints=numSamplePoints,
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.NEWTON_GRID,
        )
    gridRF.setRootFilter(filterType=FilterTypes.FUNCTION_VALUE_ZERO)
    gridRF.setRootFilter(filterType=FilterTypes.ZERO_IN_BOUNDS)
    return gridRF


def simpleArgumentRootFinder(testName: str, lvl: LogLevel, parallel=False):
    if parallel:
        hrf = ParallelRootFinder(
            testFunctions[testName][0],
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT,
            verbose=False,
        )
    else:
        hrf = RootFinder(
            testFunctions[testName][0],
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT,
            verbose=False,
        )
    hrf.setLevel(level=lvl)
    hrf.setRootFilter(filterType=FilterTypes.FUNCTION_VALUE_ZERO)
    hrf.setRootFilter(filterType=FilterTypes.ZERO_IN_BOUNDS)
    return hrf


def simpleArgumentNewtonRootFinder(
    testName: str, lvl: LogLevel, parallel=False
):
    if parallel:
        hrf = ParallelRootFinder(
            testFunctions[testName][0],
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT_NEWTON,
            verbose=False,
        )
    else:
        hrf = RootFinder(
            testFunctions[testName][0],
            containerType=ContainerTypes.ROUNDING_CONTAINER,
            algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT_NEWTON,
            verbose=False,
        )
    hrf.setLevel(level=lvl)
    hrf.setRootFilter(filterType=FilterTypes.FUNCTION_VALUE_ZERO)
    hrf.setRootFilter(filterType=FilterTypes.ZERO_IN_BOUNDS)
    return hrf
