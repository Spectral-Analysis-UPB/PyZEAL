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

