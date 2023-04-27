"""
Provide rootfinder setup methods with common settings for testing purposes.
"""


from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.container_types import ContainerTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.pyzeal_types.filter_types import FilterTypes
from pyzeal.rootfinders import (
    ParallelRootFinder,
    RootFinder,
    RootFinderInterface,
)
from pyzeal.tests.resources.finder_test_cases import testFunctions


def buildFinder(
    testName: str,
    parallel: bool,
    algorithmType: AlgorithmTypes,
    estimatorType: EstimatorTypes,
    numSamplePoints: int = 20,
    derivativeFree: bool = False,
) -> RootFinderInterface:
    """
    Build a `RootFinderInterface` instance from a given configuration.

    :param testName: Test case name
    :param parallel: Set to `True` if the RootFinder should search in
        parallel
    :param algorithmType: The type of algorithm to use within the finder
    :param estimatorType: The type of estimator to use with algorithms based on
        the argument principle
    :param numSamplePoints: `numSamplePoints` passed to the Newton grid
        algorithm
    :param derivativeFree: Set to `True` if the RootFinder should operate
        without the derivative
    :return: Initialized root finder instance
    """
    f = testFunctions[testName].testFunc
    df = None if derivativeFree else testFunctions[testName].testFuncDerivative
    Finder = ParallelRootFinder if parallel else RootFinder
    finder: RootFinderInterface = Finder(
        f,
        df,
        numSamplePoints=numSamplePoints,
        containerType=ContainerTypes.ROUNDING_CONTAINER,
        algorithmType=algorithmType,
        estimatorType=estimatorType,
    )
    finder.setRootFilter(filterType=FilterTypes.FUNCTION_VALUE_ZERO)
    finder.setRootFilter(filterType=FilterTypes.ZERO_IN_BOUNDS)

    return finder


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
    :return: Initialized root finder instance
    """
    gridFinder = buildFinder(
        testName=testName,
        numSamplePoints=numSamplePoints,
        parallel=parallel,
        derivativeFree=derivativeFree,
        algorithmType=AlgorithmTypes.NEWTON_GRID,
        estimatorType=EstimatorTypes.DEFAULT,
    )

    return gridFinder


def simpleArgumentRootFinder(
    testName: str,
    parallel: bool = False,
    estimatorType: EstimatorTypes = EstimatorTypes.SUMMATION_ESTIMATOR,
) -> RootFinderInterface:
    """
    Returns a root finder using the `SIMPLE_ARGUMENT` algorithm for the test
    case `testName`.

    :param testName: Test case name
    :param parallel: Set to `True` if the RootFinder should search in parallel,
        defaults to False
    :param estimatorType: The type of estimator to use with the simple argument
        algorithm
    :return: Initialized root finder instance
    """
    simpleFinder = buildFinder(
        testName=testName,
        parallel=parallel,
        algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT,
        estimatorType=estimatorType,
    )

    return simpleFinder


def simpleArgumentNewtonRootFinder(
    testName: str,
    parallel: bool = False,
    estimatorType: EstimatorTypes = EstimatorTypes.SUMMATION_ESTIMATOR,
) -> RootFinderInterface:
    """
    Returns a root finder using the `SIMPLE_ARGUMENT_NEWTON` algorithm for the
    test case `testName`.

    :param testName: Test case name
    :param parallel: Set to `True` if the RootFinder should search in parallel,
        defaults to False
    :param estimatorType: The type of estimator to use with the simple argument
        with Newton method algorithm
    :return: Initialized root finder instance
    """
    simpleNewtonFinder = buildFinder(
        testName=testName,
        parallel=parallel,
        algorithmType=AlgorithmTypes.SIMPLE_ARGUMENT_NEWTON,
        estimatorType=estimatorType,
    )

    return simpleNewtonFinder
