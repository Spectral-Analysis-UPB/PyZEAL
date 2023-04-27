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
