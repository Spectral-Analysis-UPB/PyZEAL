from functools import partial

import numpy as np

localTestFunctions = {
    "x^2-1": (lambda x: x**2 - 1, lambda x: 2 * x, [-1, 1]),
    "x^2+1": (lambda x: x**2 + 1, lambda x: 2 * x, [1j, -1j]),
    "x^4-1": (lambda x: x**4 - 1, lambda x: 4 * x**3, [1, -1, 1j, -1j]),
    "x^3+x^2+x+1": (
        lambda x: x**3 + x**2 + x + 1,
        lambda x: 3 * x**2 + 2 * x + 1,
        [-1, 1j, -1j],
    ),
    "x^2+26.01": (lambda x: x**2 + 26.01, lambda x: 2 * x, []),
    "x^4-6.25x+9": (
        lambda x: (x - np.sqrt(2)) * (x + np.sqrt(2)) * (x - 1.5) * (x + 1.5),
        lambda x: 4 * x**3 - 8.5 * x,
        [np.sqrt(2), -np.sqrt(2), 1.5, -1.5],
    ),
    "x^5-4x+2": (
        lambda x: x**5 - 4 * x + 2,
        lambda x: 5 * x**4 - 4,
        [
            0.508499484,
            -1.51851215,
            1.2435963,
            -0.116791 - 1.43844769j,
            -0.116791 + 1.43844769j,
        ],
    ),
    "x^3-0.01x": (
        lambda x: (x - 0.1) * (x + 0.1) * x,
        lambda x: 3 * x**2 - 0.01,
        [0.1, 0, -0.1],
    ),
    "x^30": (lambda x: x**30, lambda x: 30 * x**29, [0]),
    "x^100": (lambda x: x**100, lambda x: 100 * x**99, [0]),
    "1e6 * x^100": (lambda x: 1e6 * x**100, lambda x: 1e8 * x**99, [0]),
    "x^2-25": (lambda x: (x - 5) * (x + 5), lambda x: 2 * x, [5, -5]),
    "x^2+(0.000024414 - i)x": (
        lambda x: x * (x + 0.000024414 - 1j),
        lambda x: 2 * x + 0.000024414 - 1j,
        [0, -0.000024414 + 1j],
    ),
    "sin(x)": (np.sin, np.cos, [-1 * np.pi, 0, np.pi]),
    "exp(x)": (np.exp, np.exp, []),
    "tan(x/10)": (
        lambda x: np.tan(x / 10),
        lambda x: 1 / (10 * np.cos(x / 10) ** 2),
        [0],
    ),
    "tan(x/100)": (
        lambda x: np.tan(x / 100),
        lambda x: 1 / (100 * np.cos(x / 100) ** 2),
        [0],
    ),
    "log and sin composition": (
        lambda x: np.log(np.sin(x) ** 2 + 1),
        lambda x: 2 * np.sin(x) * np.cos(x) / (np.sin(x) ** 2 + 1),
        [-np.pi, 0, np.pi],
    ),
    "seventh root": (
        lambda x: x ** (1 / 7),
        lambda x: 1 / 7 * x ** (-6 / 7),
        [0],
    ),
    "log(x^2+26)": (
        lambda x: np.log(x**2 + 26),
        lambda x: 2 * x / (x**2 + 26),
        [-5j, 5j],
    ),
    "log, arctan, exp composition": (
        lambda x: np.log(np.arctan(np.exp(x))),
        lambda x: np.exp(x) / ((np.exp(2 * x) + 1) * np.arctan(np.exp(x))),
        [0.44302],
    ),
}

# wrap lambdas inside partial so mutlithreading works correclty


def f(name: str, x):
    return localTestFunctions[name][0](x)


def df(name: str, x):
    return localTestFunctions[name][1](x)


testFunctions = {}
for key in localTestFunctions.keys():
    testFunctions[key] = (
        partial(f, key),
        partial(df, key),
        localTestFunctions[key][2],
    )
