"""
Module lambda_wrapper.py from the package PyZEAL.
TODO

Authors:\n
- Philipp Schuette\n
"""

from typing import Literal, Optional, Union

from pyzeal_types.root_types import tHoloFunc, tVec

# global variables holding the lambda function to be wrapped and its derivative
_func: Optional[tHoloFunc] = None
_derivative: Optional[tHoloFunc] = None


def wrappedFunc(z: tVec) -> tVec:
    "The wrapped input function."
    if _func is not None:
        return _func(z)
    raise ValueError("something went wrong during lambda wrapping!")


def wrappedDerivative(z: tVec) -> tVec:
    "The wrapped derivative function."
    if _derivative is not None:
        return _derivative(z)
    raise ValueError("something went wrong during derivative wrapping!")


class LambdaWrapper:
    """
    _summary_
    """

    @staticmethod
    def wrapLambda(
        func: tHoloFunc,
        mode: Union[Literal["save"], Literal["unsave"]] = "save",
    ) -> tHoloFunc:
        """
        _summary_

        :param func: _description_
        :type func: _type_
        :param mode: _description_, defaults to "save"
        :type mode: _type_, optional
        :raises ValueError: _description_
        :return: _description_
        :rtype: _type_
        """
        global _func

        if _func is not None and mode == "save":
            raise ValueError(
                "you cannot wrap more than one lambda in save mode!"
            )

        _func = func
        return wrappedFunc

    @staticmethod
    def wrapDerivative(
        derivative: tHoloFunc,
        mode: Union[Literal["save"], Literal["unsave"]] = "save",
    ) -> tHoloFunc:
        """
        _summary_

        :param derivative: _description_
        :type derivative: _type_
        :param mode: _description_, defaults to "save"
        :type mode: _type_, optional
        :raises ValueError: _description_
        :return: _description_
        :rtype: _type_
        """
        global _derivative

        if _derivative is not None and mode == "save":
            raise ValueError(
                "you cannot wrap more than one derivative in save mode!"
            )

        _derivative = derivative
        return wrappedDerivative
