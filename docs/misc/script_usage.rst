After installation you can use the root finding facilities of **PyZEAL** by adding just a few lines of code to
your ``Python`` scripts:

.. code-block:: python

   from pyzeal.rootfinders import RootFinder

   finder = RootFinder(lambda z: z**2 - 1, lambda z: 2 * z)
   finder.calculateRoots((-2, 2), (-2, 2))

   print(f"calculated roots: {finder.roots}")

This will calculate numerically those roots of the function :math:`z\mapsto z^2 - 1` that are contained in the rectangle
within the complex plane :math:`\mathbb{C}` defined by:

.. math::

   \{z\in\mathbb{C}: -2 \leq \mathrm{Re}(z) \leq 2, -2 \leq \mathrm{Im}(z) \leq 2\} .

