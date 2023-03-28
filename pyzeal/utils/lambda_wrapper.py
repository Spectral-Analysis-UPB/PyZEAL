"""
Module lambda_wrapper.py from the package PyZEAL.
This module wraps lambda functions to allow for multiprocessing, as normally
lambda functions can not be pickled.

Authors:\n
- Philipp Schuette\n
"""

from typing import Literal, Optional, Union

from pyzeal.pyzeal_types.root_types import tHoloFunc, tVec

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
    Static wrapper class for lambda functions.
    """

    @staticmethod
    def wrapLambda(
        func: tHoloFunc,
        mode: Union[Literal["save"], Literal["unsave"]] = "save",
    ) -> tHoloFunc:
        """
        Wrap a lambda function by passing it to `func`.

        :param func: Function to wrap
        :param mode: Wrapping mode, defaults to "save". "unsave" mode will
            overwrite any pre-existing functions, while "save" mode will
            raise an error if one attempts to overwrite the wrapped function.
        :raises ValueError: Raises an error if one tries to wrap a function
            in "save" mode, while another function is already being wrapped.
        :return: The wrapped function.
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
        Wrap a lambda derivative function by passing it to `func`.

        :param func: Derivative function to wrap
        :param mode: Wrapping mode, defaults to "save". "unsave" mode will
            overwrite any pre-existing functions, while "save" mode will
            raise an error if one attempts to overwrite the wrapped function.
        :raises ValueError: Raises an error if one tries to wrap a function
            in "save" mode, while another function is already being wrapped.
        :return: The wrapped derivative.
        """
        global _derivative

        if _derivative is not None and mode == "save":
            raise ValueError(
                "you cannot wrap more than one derivative in save mode!"
            )

        _derivative = derivative
        return wrappedDerivative
