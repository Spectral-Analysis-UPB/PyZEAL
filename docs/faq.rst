.. _faq:

Frequently asked questions
==========
I don't have the derivative. Can I still use derivative-based approaches?
^^^^^^^^^^
Using automatic differentiation, you may be able to avoid computing the
derivative. To achieve this, one can use e.g. ``grad`` from the package
JAX. ::
    from jax import grad

    def f(x):
        return x ** 5 + 30 * x
    
    df = grad(f)
For more information on automatic differentiation, visit the page on automatic differentiation.

Can I use a custom implementation for an algorithm/estimator/container/etc?
^^^^^^^^^^
Yes! There is a plugin system available, so you can add custom functionality
to expand upon the capabilites of the ``PyZEAL`` package.

How do I write a plugin?
^^^^^^^^^^
