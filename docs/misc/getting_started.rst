.. _getting_started:

Getting Started
===============

------------
Installation
------------

First, clone the repository from GitHub_. Then issue the following command in the resulting directory:

.. code:: console

   $ python3 -m pip install -e ".[dev]"

This installs the **PyZEAL** project for local development. If you do not wish to conduct your own development
on the project, you can safely replace ``".[dev]"`` with a simple ``"."``. Additional installation targets are
``[docs]`` (for all dependencies required to build and contribute to the docs) and ``[all]``.

You can now import the packages and classes of **PyZEAL** into your own scripts, run the tests on your local
installation, and extend the project by e.g. writing plugins.

.. note::

  A ``pip``-installable version of **PyZEAL** will be published on ``PyPI`` as part of release **v1.0.0** (soon).


---------------------------
Using **PyZEAL** in Scripts
---------------------------

After installation you can use the root finding facilities of **PyZEAL** by adding just a few lines of code to
your ``Python`` scripts:

.. code-block:: python

   from pyzeal.rootfinders import RootFinder

   finder = RootFinder(lambda z: z**2 - 1, lambda z: 2 * z)
   finder.calculateRoots((-2, 2), (-2, 2))

   print(f"calculated roots: {finder.roots}")

This will calculate numerically the roots of the function :math:`z\mapsto z^2 - 1` in the complex domain

.. math::
   \{z\in\mathbb{C}: \mathrm{Re}(z)\in [-2, 2], \mathrm{Im}(z)\in [-2, 2]\} .

In this minimal example a lot of
configuration was not specified explicitly and is therefore determined by settings. If you want to know more about
customizing the root finding process the :ref:`User API Guide <user_guide>` is a good place to start. If you are
interested in learning more about the mathematical background of the different root finding modes visit
:ref:`Theoretical Background <theory>`. There you can also find a list of original references.

----------------
Project Overview
----------------

The project can roughly be divided into the user-facing API (supporting the first use case mentioned in the
:ref:`Introduction <intro>`) and the framework elements (supporting both the first and second use cases). Here is a rather
rough description of the components making up **PyZEAL** using class and package diagrams:

- **API**: ``rootfinders``, ``algorithms``, ``algorithms.estimators``, ``plugins``
  (`api classes <./_static/api_classes.pdf>`_, `api packages <./_static/api_packages.pdf>`_)
- **Framework**: ``utils``, ``pyzeal_logging``, ``settings``, ``pyzeal_types``
  (`framework classes <./_static/framework_classes.pdf>`_, `framework packages <./_static/framework_packages.pdf>`_)
- **Command line interface**: ``cli``
  (`cli classes <./_static/cli_classes.pdf>`_, `cli packages <./_static/cli_packages.pdf>`_)

More detailed information can be found in the respective sections of either the :ref:`User API Guide <user_guide>` or the
(slightly) more developer-oriented :ref:`Package Reference <package_reference>`.

If you have concrete questions on topics like how to use **PyZEAL** given some concrete use case you might want to consider having
a look at our :ref:`FAQ` section. If you want to find out more about how this project was conceived check out :ref:`origins`.

.. _GitHub: https://github.com/Spectral-Analysis-UPB/PyZEAL
