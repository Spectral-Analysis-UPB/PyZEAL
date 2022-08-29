============================
The PyZEAL numerical project
============================

.. image:: https://img.shields.io/badge/Language-Python-blue.svg
   :target: https://www.python.org/

.. image:: http://img.shields.io/badge/benchmarked%20by-asv-blue.svg?style=flat
   :target: https://github.com/Spectral-Analysis-UPB/PyZEAL

.. image:: https://img.shields.io/github/v/release/Spectral-Analysis-UPB/PyZEAL
   :target: https://github.com/Spectral-Analysis-UPB/PyZEAL

.. image:: https://readthedocs.org/projects/pyzeal/badge/?version=latest
   :target: https://pyzeal.readthedocs.io/en/latest/?badge=latest

.. image:: https://github.com/Spectral-Analysis-UPB/PyZEAL/workflows/build/badge.svg
   :target: https://github.com/Spectral-Analysis-UPB/PyZEAL/actions

.. image:: https://codecov.io/gh/Spectral-Analysis-UPB/PyZEAL/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/Spectral-Analysis-UPB/PyZEAL

.. image:: https://img.shields.io/badge/docs-docstr--cov-success
   :target: https://pypi.org/project/docstr-coverage/

.. image:: https://img.shields.io/badge/mypy-checked-blue
   :target: https://mypy.readthedocs.io/en/stable/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

------------------------------------------------------------------------------

.. contents:: Table of Contents
    :depth: 2

------------
Introduction
------------

This project implements numerical algorithms for the computation of zeros of holomorphic and the zeros, poles and residues of meromorphic functions.
It aspires to be a successor to and an extension of the original ZEAL (ZEros of AnaLytic functions) package written in Fortran90 by Kravanja, Van Barel, Ragos, Vrahatis, and Zafiropoulos [KVanBarelR+00]_.
The full documentation of this project is hosted on `ReadTheDocs <https://pyzeal.readthedocs.io/en/latest//>`_.

.. [KVanBarelR+00] Kravanja, Van Barel, Ragos, Vrahatis, and Zafiropoulos. ZEAL: A mathematical software package for computing zeros of analytic functions. Computer Physics Communications, 124(2):212–232, 2000.

------------
Installation
------------

To install this package you have to clone this repository using ``git clone``.
Then you can simply use ``pip`` to install the package via

.. code:: bash

  $ python3 -m pip install -e .[dev]

locally in editable mode (``-e``) and including all requirements necessary for development (``[dev]``).
The latter are optional and can be skipped if you just want to use **PyZEAL** as a third-party module in your own applications.

-----------
Basic Usage
-----------

Coming Soon!

------------
Contributing
------------

If you would like to contribute anything from an improvement of the documentation, a new feature request, bug report or (parts of) a root finding algorithm,
please feel free to do so.
Any collaborations are welcome and the documentation or the open issues might be a good place to start.
