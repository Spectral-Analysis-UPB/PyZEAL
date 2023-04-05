.. _rootfinders:

Rootfinders
===========

.. py:module:: rootfinders

-----
Usage
-----

Root finders constitute the main scripting interface to **PyZEAL**. They abstract the process of setting
up the search itself and delegate the actual searching to concrete instances of the ``FinderAlgorithm``
interface through the classical ``strategy pattern``. For the description of available algorithms see
:ref:`algorithms`.

A general root finder is initialized with a holomorphic target function and, depending on the
type of algorithm used, its derivative. It might require additional data again depending on
the concrete algorithm. After initialization there exist methods for the calculation and
subsequent retrieval of roots (and orders if the algorithm admits it).

At the moment two different root finder implementations are contained in **PyZEAL**: A straightforward
one and a parallel one. The latter uses the standard library ``multiprocessing`` module. If you
consider using it make sure that the overhead incurred is reasonably small compared to the processing
time gained.

---------
Interface
---------

.. automodule:: pyzeal.rootfinders.finder_interface
    :members:
    :special-members:
    :exclude-members: __weakref__, __str__, main

----------
RootFinder
----------

.. automodule:: pyzeal.rootfinders.rootfinder
    :members:
    :special-members:
    :exclude-members: __weakref__, __str__, __subclasshook__, main, suppressSig

------------------
ParallelRootFinder
------------------

.. automodule:: pyzeal.rootfinders.parallel_finder
    :members:
    :special-members:
    :exclude-members: __weakref__, __str__, __subclasshook__, main, suppressSig
