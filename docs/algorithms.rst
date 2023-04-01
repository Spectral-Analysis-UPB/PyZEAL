.. _algorithms:

Algorithms
==========

.. py:module:: algorithms

At the present moment, four algorithmic root finding variations are implemented within
*PyZEAL*:

1. ``NEWTON_GRID``
#. ``SIMPLE_ARGUMENT``
#. ``SIMPLE_ARGUMENT_NEWTON``
#. ``ASSOCIATED_POLYNOMIAL``

In this section we first describe the general interface that defines a ``FinderAlgorithm``.
It is this interface that provides the primary hook into the machinery of this project for
anyone looking to implement their own algorithms, be it as a full-blown extension of the
source code or as a more light-weight plugin.

We then proceed with a detailed documentation of the currently available algorithms.

---------------------
Root Finder Interface
---------------------

.. automodule:: pyzeal.algorithms.finder_algorithm
    :members:
    :special-members:
    :exclude-members: __weakref__, __str__, __subclasshook__

---------------------
Newton Grid Algorithm
---------------------

At its core the ``NEWTON_GRID`` variant uses either Newton's classical algorithm, if
the derivative is provided, or else the secant method. Both variants simply construct evenly
spaced initial points from which they start their respective algorithms. The spacing of this
two-dimensional grid inside the search rectangle is uniform in both dimensions and determined
by the ``numSamplePoints`` constructor argument.

.. automodule:: pyzeal.algorithms.newton_grid
    :members:
    :special-members:
    :exclude-members: __weakref__, __str__, __subclasshook__

-------------------------
Simple Argument Algorithm
-------------------------

The ``SIMPLE_ARGUMENT`` root finder algorithm uses the argument principle, a classical result in
complex analysis:

.. math::

   \frac{1}{2\pi i} \int_\gamma \frac{f'(z)}{f(z)} dz = \mathrm{N} ,

where :math:`\mathrm{N}` denotes the number of zeros of the holomorphic function :math:`f(z)`
inside the closed curve :math:`\gamma`.

The ``SIMPLE_ARGUMENT`` variant combines this principle with simple recursive subdivisions of
the initial rectangle: For any current rectangle the corresponding value of :math:`N` is calculated
and two cases are considered:

1. if :math:`N = 0` then the rectangle can be discarded because it contains no roots,
#. if :math:`N > 0` then the rectangle is either subdivided further if it is not sufficiently small
   yet or otherwise its center is registered as a root of order :math:`N`.

.. automodule:: pyzeal.algorithms.simple_holo
    :members:
    :special-members:
    :exclude-members: __weakref__, __str__, __subclasshook__

--------------------------------
Simple Argument Newton Algorithm
--------------------------------

The ``SIMPLE_ARGUMENT_NEWTON`` algorithm is a straightfoward adaptation of the ``SIMPLE_ARGUMENT``
variant. Instead of relying solely on the argument principle, the classical Newton algorithm is used
once recursive subdivisions have made the rectangle to search sufficiently small.

.. automodule:: pyzeal.algorithms.simple_holo_newton
    :members:
    :special-members:
    :exclude-members: __weakref__, __str__, __subclasshook__

-------------------------------
Associated Polynomial Algorithm
-------------------------------

.. automodule:: pyzeal.algorithms.polynomial_holo
    :members:
    :special-members:
    :exclude-members: __weakref__, __str__, __subclasshook__
