.. _intro:

Goals, Overview, and Installation
=================================

---------------
Goals of PyZEAL
---------------

**PyZEAL** aims to provide facilities for the calculation of zeros and poles of holomorphic and
meromorphic functions. While there exists a wealth of theoretical results as well as battle-hardened
implementations of such root finding algorithms for e.g. smooth functions (SciPy_), the situation
in the holomorphic setting is much less comfortable: It appears that most of the algorithms available
for holomorphic ones do not possess a readily available, up-to-date, actively maintained implementation.

This (seeming) gap in the software landscape is even more apparant as these types of functions exhibit a
rich structure far beyond simple smoothness, opening up the possibility for adapted, more efficient root
finding algorithms. The goal of this project then is the practical implementation of such algorithms in
an open-source package that is well tested, written in an accessible language, and distributed in a
user-friendly manner.

We aim to support two main use cases:

1. Enabling out-of-the-box usage as a tool within any project which requires the calculation of roots
   or poles of holomorphic or meromorphic functions. In particular this includes seamless integration
   into the *Python* ecosystem and a user experience similar to common packages like SciPy_ or NumPy_.
#. Providing a platform for the practical implementation, debugging, testing, and benchmarking of newly
   developed root finding algorithms as well as their comparison with existing procedures. To this end
   *PyZEAL* includes a number of framework elements as well as a plugin mechanism for more light-weight
   implementations of prototypes.

The approach to achieving these goals will be iterative implementation and optimization of a variety of
different algorithms and comparing them, while simultaneously exposing an easy-to-use, accessible, and
standardized API.

.. note::

    This is an ongoing project. Any contributions such as feature requests, bug reports, or
    collaborations on documentation, theoretical background, or practical implementation are
    much appreciated!

.. _SciPy: https://scipy.org/
.. _NumPy: https://numpy.org/

--------
Overview
--------

The project can roughly be divided into the user-facing API (supporting the first use case mentioned
above) and the framework elements (supporting both the first and second use cases). In this section
we give a rough description of the components making up *PyZEAL* through class and package diagrams.
More detailed information can be found in the respective sections of the class-level documentation.

- **API**: ``rootfinders``, ``algorithms``, ``algorithms.estimators``, ``plugins``
  (`api classes <./_static/api_classes.pdf>`_, `api packages <./_static/api_packages.pdf>`_)
- **Framework**: ``utils``, ``pyzeal_logging``, ``settings``, ``pyzeal_types``
  (`framework classes <./_static/framework_classes.pdf>`_, `framework packages <./_static/framework_packages.pdf>`_)
- **Command line interface**: ``cli``
  (`cli classes <./_static/cli_classes.pdf>`_, `cli packages <./_static/cli_packages.pdf>`_)


For more information on the theoretical underpinning of the algorithms currently implemented, see
the :ref:`theory` page.

------------
Installation
------------

First, clone the repository from GitHub. Then issue the following command in the resulting directory:

.. code:: bash

   $ python3 -m pip install -e ".[dev]"

This installs the *PyZEAL* project for local development. If you do not wish to conduct your own development
on the project, you can safely replace ``.[dev]`` with a simple ``.``. Additional installation targets are
``[docs]`` (for all dependencies required to build and contribute to the docs) and ``[all]``.

You can now import the packages and classes of *PyZEAL* into your own scripts, run the tests on your local
installation, and extend the project by e.g. writing plugins.
