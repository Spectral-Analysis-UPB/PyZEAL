"""
This module provides a static factory class which maps the containers available
in the `ContainerTypes` enumeration to appropriate implementations of the
interface `RootContainer`.

Authors:\n
- Philipp Schuette\n
"""

from pyzeal_types.container_types import ContainerTypes
from pyzeal_types.root_types import tHoloFunc, tRoot
from pyzeal_utils.root_container import RootContainer
from pyzeal_utils.rounding_container import RoundingContainer


class ContainerFactory:
    "Static factory class used to create instances of root containers."
    @staticmethod
    def getConcreteContainer(
        containerType: ContainerTypes, accuracy: int = 3
    ) -> RootContainer:
        """
        Initialize and return a root container instance based on the given type
        `algoType` of container and a given accuracy.

        :param containerType: type of container to construct
        :type containerType: ContainerTypes
        :param accuracy: the accuracy of the given container
        :type accuracy: int
        """
        if containerType == ContainerTypes.ROUNDING_CONTAINER:
            return RoundingContainer(accuracy)
        else:
            # TODO: implement configuration mechanism for default containers
            return RoundingContainer(accuracy)

    @staticmethod
    def addFunctionValueCheck(
        container: RootContainer, f: tHoloFunc, threshold: int = 1
    ) -> RootContainer:
        """
        Given a container instance this method adds a filter to its addRoot()
        method. The filter checks if the root to be added yields a sufficiently
        small value upon function evaluation and discards the root otherwise.

        :param container: the container which receives a new filter
        :type container: RootContainer
        :param f: the function which the roots belong to
        :type f: Callable[[complex], complex]
        :param threshold: the threshold for evaluation of `f` on roots
        :type threshold: int
        :return: the enhanced container
        :rtype: RootContainer
        """
        _oldAdd = container.addRoot

        def _newAdd(root: tRoot, accuracy: int) -> None:
            "Filter predicate to ensure results are close to zero."
            if abs(f(root[0])) < 10**(-threshold):
                _oldAdd(root, accuracy)

        # override the existing addRoot(), setting the method directly does not
        # pass mypy type checking
        setattr(container, "addRoot", _newAdd)
        return container
