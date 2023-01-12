"""
Module filter_roots.py of the utils package.
This module contains utility functions designed for general re-use in various
root finding algorithms.

Authors:\n
- Philipp Schuette\n
- Sebastian Albrecht\n
"""

from cmath import isclose
from typing import Tuple

import numpy as np

from pyzeal_types.root_types import tErrVec, tResVec


def filterCoincidingRoots(
    roots: tResVec,
    errors: tErrVec,
    recalcOrders: bool = False,
    returnLists: bool = False,
) -> Tuple:
    r"""
    Filter out coinciding roots (within error range).

    If two coinciding roots are found, then the two are replaced by a mean
    (weighted according to the respective errors).

    :param roots: array of roots together with their root order
    :type roots: List[Tuple[complex, int]] or numpy.ndarray of shape (number of
        roots, 2)
    :param errors: array of errors associated with each root
    :type errors: List[complex] or numpy.ndarray of shape (number of roots, )
    :param recalcOrders: whether the root orders of two coinciding roots should
        be properly recalculated, otherwise the smaller root order is kept,
        defaults to False
    :type recalcOrders: bool, optional
    :param returnLists: whether the return types should be forced to be List,
        defaults to False
    :type returnLists: bool, optional
    :return: array of roots together with their root order, and array(s) of
        corresponding errors, if any further `rootData` arrays have been
        passed, these are also returned
    :rtype: List[Tuple[complex, int]] or numpy.ndarray of shape (number of
        filtered roots, 2), List[complex] or numpy.ndarray of shape (number of
        filtered roots, ), further arrays containing the modified `rootData`
        of shape (number of filtered roots, ...),
        the return types match the types of the `roots`, `errors` and
        `rootData` input arrays unless `returnLists` is True
    """
    if isinstance(roots, np.ndarray):
        convertRootsToNumpy = not returnLists
        roots = list(
            zip(roots[:, 0].tolist(), roots[:, 1].real.astype(int).tolist())
        )
    else:
        convertRootsToNumpy = False

    if isinstance(errors, np.ndarray):
        convertErrorsToNumpy = not returnLists
        errors = list(errors)
    else:
        convertErrorsToNumpy = False

    if len(errors) != len(roots):
        raise ValueError(
            "roots array, errors array and rootData arrays "
            + "must all have the same length!"
        )

    i = 0
    while i < len(roots):
        j = i + 1
        while j < len(roots):
            if isclose(
                roots[j][0],
                roots[i][0],
                rel_tol=0.0,
                abs_tol=abs(errors[j] + errors[i]),
            ):

                # compute "mean" of old and new root
                meanRootReal = (
                    errors[i].real
                    / (errors[j].real + errors[i].real)
                    * roots[j][0].real
                ) + (
                    errors[j].real
                    / (errors[j].real + errors[i].real)
                    * roots[i][0].real
                )
                meanRootImag = (
                    errors[i].imag
                    / (errors[j].imag + errors[i].imag)
                    * roots[j][0].imag
                ) + (
                    errors[j].imag
                    / (errors[j].imag + errors[i].imag)
                    * roots[i][0].imag
                )

                # compute "mean" order of "mean" root
                if recalcOrders:
                    raise NotImplementedError(
                        "Recalculation of the order of"
                        + " coinciding roots is not yet "
                        + "implemented"
                    )
                meanRootOrder = min(roots[i][1], roots[j][1])

                # update root list
                roots[i] = (meanRootReal + 1j * meanRootImag, meanRootOrder)
                del roots[j]

                # compute mean error and update error list
                errors[i] = 0.5 * (errors[i] + errors[j])
                del errors[j]

            else:
                j += 1
        i += 1

    if convertRootsToNumpy:
        roots = np.array(roots, dtype=complex)
    if convertErrorsToNumpy:
        errors = np.array(errors, dtype=complex)

    return roots, errors
