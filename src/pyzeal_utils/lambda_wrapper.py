"""
Module lambda_wrapper.py from the package PyZEAL.
TODO

Authors:\n
- Philipp Schuette\n
"""

from pyzeal_types.root_types import tHoloFunc, tVec

# global list holding the lambda functions to be wrapped
_func: tHoloFunc


# TODO: implement safety mechanism to prevent multiple conflicting assignments!
def wrappedFunc(z: tVec) -> tVec:
    "The wrapped input function."
    return _func(z)


class LambdaWrapper:
    """
    _summary_
    """

    @staticmethod
    def wrap(func: tHoloFunc) -> tHoloFunc:
        """
        _summary_

        :param func: _description_
        :type func: _type_
        :return: _description_
        :rtype: _type_
        """
        global _func
        _func = func

        return wrappedFunc
