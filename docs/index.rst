Welcome to PyZEAL's documentation!
==================================

.. |badge1| image:: https://img.shields.io/badge/Language-Python-blue.svg
   :target: https://www.python.org/

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

.. |badge7| image:: ./_static/docstr_coverage_badge.svg
   :target: https://pypi.org/project/docstr-coverage/

.. |badge8| image:: https://img.shields.io/badge/mypy-checked-blue
   :target: https://mypy.readthedocs.io/en/stable/

.. |badge9| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. only:: html

    +----------+-------------+----------+----------+------------+
    | Project  | Build Status| Coverage | Checkers | Benchmarks |
    +==========+=============+==========+==========+============+
    | |badge1| | |badge5|    | |badge6| | |badge8| | |badge2|   |
    +----------+-------------+----------+----------+------------+
    | |badge3| | |badge4|    | |badge7| | |badge9| |            |
    +----------+-------------+----------+----------+------------+

--------------------------------

.. _intro:

What is **PyZEAL**?
===================

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

--------------------------------

.. toctree::
   :maxdepth: 1
   :caption: Contents of PyZEAL's Documentation:

   misc/getting_started
   user_guide/user_guide
   theory/theory
   package_reference/package_reference
   faq/faq
   misc/origins
   misc/release_notes
