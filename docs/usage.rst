.. _usage:

Basic Usage
===========

------------
Installation
------------

First, clone the repository from GitHub. Then issue the following command in the resulting directory:

.. code:: console

   $ python3 -m pip install -e ".[dev]"

This installs the **PyZEAL** project for local development. If you do not wish to conduct your own development
on the project, you can safely replace ``".[dev]"`` with a simple ``".""``. Additional installation targets are
``[docs]`` (for all dependencies required to build and contribute to the docs) and ``[all]``.

You can now import the packages and classes of **PyZEAL** into your own scripts, run the tests on your local
installation, and extend the project by e.g. writing plugins.

.. note::

  A ``pip``-installable version of **PyZEAL** will be part of release *v1.0.0*.


---------------------------
Using **PyZEAL** in Scripts
---------------------------

.. code-block:: python

   from pyzeal.rootfinders import rootfinder
