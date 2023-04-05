.. _faq:

Frequently Asked Questions
==========================

I don't have the derivative. Can I still use derivative-based approaches?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using a technique called *automatic differentiation*, you may be able to avoid computing the
derivative by hand. There exist various projects which implement this technique, e.g. the
package ``JAX`` (through the function ``grad``):

.. code:: python

    from jax import grad

    def f(x):
        return x ** 5 + 30 * x

    df = grad(f)

For more information on automatic differentiation, visit the notebook on automatic differentiation
linked below.

How can I use custom implementations for algorithms/estimators/...?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a plugin system available, so you can add custom functionality to expand upon the capabilites of the
**PyZEAL** package. Once you have implemented e.g. your own ``FinderAlgorithm`` there is a short standard procedure
which allows you to incorporate your custom script with the project's code base without having to change a single
line of its code.

You can find a detailed description of this procedure in the notebook linked below.

Additional Resources
--------------------

.. toctree::
   :maxdepth: 1

   auto_diff
   plugin_example
