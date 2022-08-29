.. _intro:

Introduction to PyZEAL's Documentation
======================================

**PyZEAL** aims to provide facilities for the calculation of zeros and poles of holomorphic and
meromorphic functions. While there exists a wealth of theoretical results as well as battle-hardened
implementations of such root finding algorithms for e.g. smooth functions, it appears that most of the
algorithms available for holomorphic ones do not possess a readily available, up-to-date, actively maintained implementation.

This (seeming) gap in the software landscape is even more apparant as these types of functions exhibit a
rich structure far beyond simple smoothness, opening up the possibility for adapted, more efficient root finding
algorithms. The goal of this project then is the practical implementation of such algorithms in an open-source
package that is well tested, written in an accessible language, and distributed in a user-friendly manner.

The approach to this will be iteratively implementing and optimizing a variety of different algorithms and comparing
them, while simultaneously exposing an easy-to-use and accessible API. Note that this is an ongoing project and we
appreciate any contributions, be it feature requests, bug reports, or collaborations on documentation, theoretical
background or practical implementation.

For more information on the theoretical underpinning of the algorithms currently implemented, see the
:ref:`theoretical_background` page.