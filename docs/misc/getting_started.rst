.. _getting_started:

Getting Started
===============

------------
Installation
------------

.. include:: ../misc/installation.rst

---------------------------
Using **PyZEAL** in Scripts
---------------------------

.. include:: ../misc/script_usage.rst

In this minimal example a lot of configuration was not specified explicitly and is therefore determined by
settings. If you want to know more about customizing the root finding process the
:ref:`User API Guide <user_guide>` is a good place to start. If you are interested in learning more about
the mathematical background of the different root finding modes visit :ref:`Theoretical Background <theory>`.
There you can also find a list of original references.

A more comprehensive getting started example is contained in the following notebook:

.. toctree::

   starter_notebook

----------------
Project Overview
----------------

The project can roughly be divided into the user-facing API (supporting the first use case mentioned in the
:ref:`Introduction <intro>`) and the framework elements (supporting both the first and second use cases). Here
is a rather rough overview over the components making up **PyZEAL** using class and package diagrams:

- **API**: ``rootfinders``, ``algorithms``, ``algorithms.estimators``, ``plugins``
  (`api classes <../_static/api_classes.pdf>`_, `api packages <../_static/api_packages.pdf>`_)
- **Framework**: ``utils``, ``pyzeal_logging``, ``settings``, ``pyzeal_types``
  (`framework classes <../_static/framework_classes.pdf>`_, `framework packages <../_static/framework_packages.pdf>`_)
- **Command line interface**: ``cli``
  (`cli classes <../_static/cli_classes.pdf>`_, `cli packages <../_static/cli_packages.pdf>`_)

More detailed information can be found in the respective sections of either the :ref:`User API Guide <user_guide>` or the
(slightly) more developer-oriented :ref:`Package Reference <package_reference>`.

If you have concrete questions on topics like how to use **PyZEAL** given some concrete use case you might want to
consider having a look at our :ref:`FAQ` section. If you want to find out more about how this project was conceived
check out :ref:`origins`.

.. _GitHub: https://github.com/Spectral-Analysis-UPB/PyZEAL
