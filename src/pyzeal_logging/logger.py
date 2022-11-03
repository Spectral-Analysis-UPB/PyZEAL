#!/usr/bin/python3.8
"""
Module logger of the pyzeal_logging package.
This module contains the basic logging setup to be used with all PyZEAL related
modules.

Authors:\n
- Philipp Schuette\n
"""

import logging
import os


def initLogger(logName: str) -> logging.Logger:
    r"""
    Initialize a module-level logger for the module 'modName', for technical
    reasons you have to provide __name__ as the second argument. Default
    logging level is set to WARNING.
    """
    if not os.path.exists("./logs/"):
        os.mkdir("./logs/")

    logger = logging.getLogger(logName)
    logger.setLevel(logging.WARNING)

    if not logger.hasHandlers():
        fHandler = logging.FileHandler("./logs/" + logName + ".log")
        formatter = logging.Formatter(
            "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
        )
        fHandler.setFormatter(formatter)
        logger.addHandler(fHandler)

    return logger
