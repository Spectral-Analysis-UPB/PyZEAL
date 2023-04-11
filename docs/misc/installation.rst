First, clone the repository from GitHub_ using ``git clone``. Then issue the following command in the resulting
directory to install the package with ``pip``:

.. code:: console

   $ python3 -m pip install -e ".[dev]"

This installs the **PyZEAL** project in editable mode (``-e``) and including all requirements necessary for local
development (``[dev]``). If you do not wish to conduct your own development on the project, you can safely replace
``".[dev]"`` with a simple ``"."``. Additional installation targets are ``[docs]`` (for all dependencies required
to build and contribute to the docs) and ``[all]``.

You can now import the packages and classes of **PyZEAL** into your own scripts, run the tests on your local
installation, and extend the project by e.g. writing plugins.

.. note::

  A ``pip``-installable version of **PyZEAL** will be published on ``PyPI`` as part of release **v1.0.0** (soon).

.. _GitHub: https://github.com/Spectral-Analysis-UPB/PyZEAL

