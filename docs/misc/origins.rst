.. _origins:

Origins of the **PyZEAL** Project
=================================

This is the documentation of the **PyZEAL** numerics project. It deals with the calculation
of zeros of holomorphic functions. Within this project we aspire to port much of the functionality
of the original **ZEAL** (ZEros of AnaLytic functions [KVanBarelR+00]_) Fortran90 package
(and namesake for this project) to ``Python`` while both adding some convenience features as well
as leveraging more recent algorithms and technologies.

**PyZEAL** originated as part of the **PyZeta** project which provides facilities for the calculation
of dynamical zeta functions. These in turn allow one to determine dynamical invariants called
*Ruelle resonances* as their zeros (see the image below). Dynamical determinants being examples for rather
complicated holomorphic functions therefore set the context for the independent investigation and
implementation of root finding algorithms for this class of functions in the form of the present project.

The following is an example of resonances for a dynamical system called a *Schottky surface*. Plots such as this
(and significantly more complex numerical experiments) are straightforward to calculating by combining basic features
of **PyZEAL** and **PyZeta**:

.. image:: ../_static/images/resonance_example.png
   :align: center

If you want to get off the ground with using **PyZEAL** in your own project as fast as possible then :ref:`getting_started` is a
good place to get started. For a softer introduction and additional information on the philosophy and aims of this project
check out :ref:`intro`. For details on the theoretical background and a list of references relevant to **PyZEAL** visit
:ref:`theory`.

--------------------------------

.. [KVanBarelR+00] Kravanja, Van Barel, Ragos, Vrahatis, and Zafiropoulos. ZEAL: A mathematical software package for computing zeros of analytic functions. Computer Physics Communications, 124(2):212–232, 2000.
