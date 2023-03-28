Rootfinder Package Documentation
================================

.. py:module:: rootfinders

-----
Usage
-----

The usage principle of all rootfinders is that they are initialized with a
target function and, depending on the type of rootfinder, additional 
requirements such as the derivative. An initialized rootfinder can then 
calculate roots in a given area using the ``calcRoots`` method.
Any roots found can be retrieved with the ``res`` or ``getRoots`` method.

To use a rootfinder, a ``RootFinder`` needs to be instantiated with a target
function and, depending on the type of algorithm used, the derivative. By default,
the ``SIMPLE_ARGUMENT`` algorithm is used with a ``ROUNDING_CONTAINER``. For more
information on the different algorithms and containers, visit :ref:`algorithms`
and :ref:`containers`.

---------
Interface
---------

.. automodule:: pyzeal.rootfinders.finder_interface
    :members:
    :special-members:
    :exclude-members: __weakref__, __str__, main

----------
Rootfinder
----------

.. automodule:: pyzeal.rootfinders.rootfinder
    :members:
    :special-members:
    :exclude-members: __weakref__, __str__, __subclasshook__, main, suppressSig

There is also a parallelized version of the rootfinder:

.. automodule:: pyzeal.rootfinders.parallel_finder
    :members:
    :special-members:
    :exclude-members: __weakref__, __str__, __subclasshook__, main, suppressSig
