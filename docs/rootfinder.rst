Rootfinder Package Documentation
================================

.. py:module:: rootfinder

Usage
--------------------------------
The usage principle of all rootfinders is that they are initialized with a
target function and, depending on the type of rootfinder, additional 
requirements such as the derivative. An initialized rootfinder can then 
calculate roots in a given area using the ``calcRoots`` method.
Any roots found can be retrieved with the ``res`` or ``getRoots`` method.

Interface
--------------------------------
.. automodule:: pyzeal.finder_interface
    :members:
    :special-members:
    :exclude-members: __weakref__, __str__, main

Newton-Grid-Rootfinder
--------------------------------

This rootfinder uses the Newton-algorithm. Starting points are evenly spaced
points inside the rectangle given to ``calcRoots``, where the fineness in
each axis is determined by `numSamplePoints`. From each point, the Newton-
algorithm is started. Roots are then rounded according to the required
precision. 

.. autoclass:: pyzeal.newton_grid.NewtonGridRootFinder
    :members:
    :inherited-members:
    :special-members:
    :exclude-members: __weakref__, __str__, main, runRootJobs, logger

Argument-Principle-Rootfinder
--------------------------------

The ``HoloRootFinder`` uses the argument-principle with successive subdivisions
to find zeros. If a rectangle contains at least one zero, it is split into
two halves. Recursively, roots in these will be searched, with the recursion
stopping if the rectangle has a size that is smaller than the required
precision.

.. autoclass:: pyzeal.simple_argument.HoloRootFinder
    :members:
    :special-members:
    :inherited-members:
    :exclude-members: __weakref__, __str__, main

The ``NewtonRootFinder`` is based on the ``HoloRootFinder``, but instead of
relying solely on the argument-principle, the Newton-algorithm is used once
the search area is sufficiently small.

.. autoclass:: pyzeal.simple_argument.NewtonRootFinder
    :members:
    :special-members:
    :inherited-members:
    :exclude-members: __weakref__, __str__, main