"""
This is an example for a pytest script that tests a source module.
"""

from pkg1.example import printHello


def test_printHello() -> None:
    "This test should never fail."
    printHello()
    assert True
