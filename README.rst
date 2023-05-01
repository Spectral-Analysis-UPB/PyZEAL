============================
The PyZEAL numerical project
============================

.. |badge0| image:: ./docs/_static/docstr_coverage_badge.svg
   :target: https://pypi.org/project/docstr-coverage/

.. |badge1| image:: https://img.shields.io/badge/Language-Python-blue.svg
   :target: https://pypi.org/project/PyZEAL/

.. |badge2| image:: http://img.shields.io/badge/benchmarked%20by-asv-blue.svg?style=flat
   :target: https://github.com/Spectral-Analysis-UPB/PyZEAL

.. |badge3| image:: https://img.shields.io/github/v/release/Spectral-Analysis-UPB/PyZEAL
   :target: https://github.com/Spectral-Analysis-UPB/PyZEAL

.. |badge4| image:: https://readthedocs.org/projects/pyzeal/badge/?version=latest
   :target: https://pyzeal.readthedocs.io/en/latest/?badge=latest

.. |badge5| image:: https://github.com/Spectral-Analysis-UPB/PyZEAL/workflows/build/badge.svg
   :target: https://github.com/Spectral-Analysis-UPB/PyZEAL/actions

.. |badge6| image:: https://codecov.io/gh/Spectral-Analysis-UPB/PyZEAL/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/Spectral-Analysis-UPB/PyZEAL

.. |badge7| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |badge8| image:: https://img.shields.io/badge/mypy-checked-blue
   :target: https://mypy.readthedocs.io/en/stable/

+----------+--------------+----------+----------+------------+
| Project  | Build Status | Coverage | Checkers | Benchmarks |
+==========+==============+==========+==========+============+
| |badge1| | |badge5|     | |badge6| | |badge8| | |badge2|   |
+----------+--------------+----------+----------+------------+
| |badge3| | |badge4|     | |badge0| | |badge7| |            |
+----------+--------------+----------+----------+------------+

-------------------------------

.. contents:: Table of Contents
    :depth: 2

-------------------
What is **PyZEAL**?
-------------------

Welcome to **PyZEAL**!

This project implements numerical algorithms for the computation of zeros of holomorphic as well as the
zeros, poles and residues of meromorphic functions. It aspires to be a successor to and an extension of
the original ZEAL (ZEros of AnaLytic functions) package written in Fortran90 by Kravanja, Van Barel, Ragos, Vrahatis,
and Zafiropoulos [KVanBarelR+00]_.

The full documentation of this project is hosted on `ReadTheDocs <https://pyzeal.readthedocs.io/en/latest//>`_.

While there exists a wealth of theoretical results as well as battle-hardened implementations of such root finding
algorithms for e.g. smooth functions (SciPy_), the situation in the holomorphic setting is much less comfortable:
It appears that most of the algorithms available for holomorphic ones do not possess a readily available,
up-to-date, actively maintained implementation.

This (seeming) gap in the software landscape is even more apparant as these types of functions exhibit a
rich structure far beyond simple smoothness, opening up the possibility for adapted, more efficient root
finding algorithms. The goal of this project then is the practical implementation of such algorithms in
an open-source package that is well tested, written in an accessible language, and distributed in a
user-friendly manner.

We aim to support two main use cases with this package:

1. Enabling out-of-the-box usage as a tool within any project which requires the calculation of roots
   or poles of holomorphic or meromorphic functions. In particular this includes seamless integration
   into the *Python* ecosystem and a user experience similar to common packages like SciPy_ or NumPy_.
#. Providing a platform for the practical implementation, debugging, testing, and benchmarking of newly
   developed root finding algorithms as well as their comparison with existing procedures. To this end
   **PyZEAL** includes a number of framework elements as well as a plugin mechanism for more light-weight
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

-------------------------------

.. [KVanBarelR+00] Kravanja, Van Barel, Ragos, Vrahatis, and Zafiropoulos. ZEAL: A mathematical software package for computing zeros of analytic functions. Computer Physics Communications, 124(2):212–232, 2000.

------------
Installation
------------

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

-----------
Basic Usage
-----------

After installation you can use the root finding facilities of **PyZEAL** by adding just a few lines of code to
your ``Python`` scripts:

.. code-block:: python

   from pyzeal.rootfinders import RootFinder

   finder = RootFinder(lambda z: z**2 - 1, lambda z: 2 * z)
   finder.calculateRoots((-2, 2), (-2, 2))

   print(f"calculated roots: {finder.roots}")

This will calculate numerically those roots of the function mapping ``z`` to ``z^2 - 1`` which are
contained in the rectangle within the complex plane defined by the conditions ``-2 <= Re(z) <= 2``
and ``-2 <= Im(z) <= 2`` on the real and imaginary parts of the complex variable ``z``.

This minimal example leaves a lot of configuration up to the pre-configured settings. Visit the
`full documentation <https://pyzeal.readthedocs.io/en/latest//>`_ to learn more about the possible setups!

------------
Contributing
------------

If you would like to contribute anything from an improvement of the documentation, a new feature request, bug
report or (parts of) a root finding algorithm, please feel free to do so. Any collaborations are welcome and
the documentation or the open issues might be a good place to start.

To contribute, either clone or fork the repository and create a development branch `dev/<your_feature>`. Once
you have completed your work on this branch create a pull request on the `main` branch of this repository. At
this point your PR requires (at least) one positive review from a core contributor. Once you have received such
a review, maybe after addressing some comments and suggestions by the reviewer(s), your PR will be merged effectively
making your work part of the mainline **PyZEAL** package.

