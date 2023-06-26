@startuml

left to right direction
skinparam linetype ortho

skinparam package {
    BackgroundColor #CCCCCC
}

skinparam class {
    BackgroundColor PaleGreen
}

skinparam titleBorderRoundCorner 15
skinparam titleBorderThickness 2
skinparam titleBorderColor black
skinparam titleBackgroundColor SeaGreen

title "PyZEAL Core Components and Auxiliary Packages"

package algorithms #FFD700 {
    package estimators #AAAAAA {
        abstract class ArgumentEstimator <<abstract>> { }

        class QuadratureEstimator { }

        class SummationEstimator { }

        ArgumentEstimator <|-r- QuadratureEstimator
        ArgumentEstimator <|-- SummationEstimator
    }

    package wrappers #AAAAAA {
        interface PolynomialWrapper <<interface>> { }
    }

    interface FinderAlgorithm <<interface>> { }

    class NewtonGridAlgorithm { }

    class SimpleArgumentAlgorithm { }

    class SimpleArgumentNewtonAlgorithm { }

    class AssociatedPolynomialAlgorithm { }

    FinderAlgorithm <|.. NewtonGridAlgorithm
    FinderAlgorithm <|.r. SimpleArgumentAlgorithm
    SimpleArgumentAlgorithm <|.. SimpleArgumentNewtonAlgorithm
    SimpleArgumentAlgorithm <|.. AssociatedPolynomialAlgorithm
    AssociatedPolynomialAlgorithm --> PolynomialWrapper
    SimpleArgumentAlgorithm --> ArgumentEstimator
}

package cli {
    interface CLIControllerFacade <<interface>> { }

    class CLIController { }

    interface PyZEALParserInterface <<interface>> { }

    class PyZEALParser

    class PyZEALEntry <<static>> { }

    PyZEALEntry -l-> CLIControllerFacade
    PyZEALEntry --> PyZEALParserInterface
    CLIControllerFacade <|.l. CLIController
    PyZEALParserInterface <|.l. PyZEALParser
}

package plugins {
    class InstallationHelper { }

    class PluginLoader { }

    interface PyZEALPlugin { }

    InstallationHelper -r-> PluginLoader
    PluginLoader -r-> PyZEALPlugin
}

package pyzeal_logging {
    enum LogLevel <<enum>> { }

    class LogManager <<static>> { }

    class Loggable <<mixin>> { }

    interface PyZEALLogger <<interface>> { }

    Loggable *-l- PyZEALLogger
    Loggable --> LogManager
    LogLevel --* PyZEALLogger
    LogLevel -l[hidden]- LogManager
}

package rootfinders {
    abstract class RootFinderInterface <<abstract>> {
        + complex[] roots
        + int[] orders
        + calculateRoots(reRan: (float, float), imRan: (float, float), precision: (int, int))
    }

    class RootFinder { }

    class ParallelFinder { }

    RootFinderInterface <|-l- RootFinder
    RootFinder <|-- ParallelFinder
}

package settings {
    interface CoreSettingsService <<interface>> { }

    interface SettingsService <<interface>> { }

    class JSONCoreSettingsService { }

    class JSONSettingsService { }

    class RAMSettingsService { }

    SettingsService -l-|> CoreSettingsService
    SettingsService <|.r. RAMSettingsService
    SettingsService <|.. JSONSettingsService
    CoreSettingsService <|.. JSONCoreSettingsService
    JSONCoreSettingsService -r-o JSONSettingsService
}

package utils #FFD700 {
    package containers #AAAAAA {
        interface RootContainer <<interface>> { }

        class RoundingContainer { }

        class PlainContainer { }

        RootContainer <|.l. RoundingContainer
        RootContainer <|.. PlainContainer
    }

    package factories #AAAAAA {
        class AlgorithmFactory { }

        class ContainerFactory { }

        class EstimatorFactory { }

        class SettingsFactory { }
    }

    class RootContext { }

    class InitializationHandler <<static>> { }

    class FinderProgressBar { }

    class ServiceLocator <<static>> { }

    FinderProgressBar --o RootContext
    InitializationHandler --> ServiceLocator
    RootContainer --o RootContext
}

FinderAlgorithm <-- RootFinder
RootContainer <-- RootFinder
PyZEALParserInterface -l[hidden]- LogLevel
JSONCoreSettingsService -l[hidden]- LogManager
ParallelFinder -[hidden]- RAMSettingsService
PyZEALPlugin -r[hidden]- CoreSettingsService

@enduml
