"""
Module init_modes.py from the package PyZEAL.
This module contains named constants which identify the different startup modes
of the PyZEAL project (i.e. cli, scripting, ...).

Authors:\n
- Philipp Schuette\n
"""

from enum import Flag, auto


class InitModes(Flag):
    "Enumeration containing the different startup modes for PyZEAL."
    CLI = auto()
    SCRIPT = auto()
    GUI = auto()
