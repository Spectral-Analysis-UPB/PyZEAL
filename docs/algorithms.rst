.. _algorithms:

Algorithms
================================
Currently, there are three algorithms implemented: ``NEWTON_GRID``,
``SIMPLE_ARGUMENT`` and ``SIMPLE_ARGUMENT_NEWTON``.

Newton-Grid-Algorithm
--------------------------------
The ``NEWTON_GRID``-rootfinder uses the Newton-algorithm if the derivative
is provided, else the secant method is ued. Starting points are evenly spaced
points inside the search rectangle, where the fineness in
each axis is determined by `numSamplePoints`. From each point, the Newton-
algorithm is started.

Simple-Argument-Algorithm
--------------------------------
The ``SIMPLE_ARGUMENT``-rootfinder uses the argument-principle with successive subdivisions
to find zeros. If a rectangle contains at least one zero, it is split into
two halves. Recursively, roots in these will be searched, with the recursion
stopping if the rectangle has a size that is smaller than the required
precision.


Simple-Argument-Newton-Algorithm
--------------------------------
The ``SIMPLE_ARGUMENT_NEWTON``-rootfinder is based on the ``SIMPLE_ARGUMENT``-rootfinder, but instead of
relying solely on the argument-principle, the Newton-algorithm is used once
the search area is sufficiently small.
