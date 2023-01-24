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
from datetime import datetime
from typing import Optional

from pyzeal_logging.logger_facade import PyZEALLogger
from pyzeal_types.settings_types import SettingsServicesTypes
from pyzeal_utils.pyzeal_factories.settings_factory import \
    SettingsServiceFactory

DATE: Optional[datetime] = None


def initLogger(logName: str) -> PyZEALLogger:
    r"""
    Initialize a module-level logger for the module 'modName'. Default logging
    level is set to WARNING. All logs are stored in a ./logs directory in a
    file pyzeal_<datetime.now>.log, where the date is determined at the start
    of every new session (upon first creation of a module logger within a
    session).

    :param logName: the name of the logger, should equal the module name
    :type logName: str
    :return: the (module-level) logger
    :rtype: pyzeal_logging.logging_facade.PyZEALLogger
    """
    if not os.path.exists("./logs/"):
        os.mkdir("./logs/")

    global DATE
    if DATE is None:
        DATE = datetime.now()

    logger = logging.getLogger(logName)
    logger.setLevel(
        SettingsServiceFactory.getConcreteSettings(
            SettingsServicesTypes.DEFAULT
        ).logLevel.value
    )

    if not logger.hasHandlers():
        fileName = (
            f"{str(DATE.day).zfill(2)}{str(DATE.month).zfill(2)}{DATE.year}"
            + f"{str(DATE.hour).zfill(2)}{str(DATE.minute).zfill(2)}"
            + f"{str(DATE.second).zfill(2)}"
        )
        fHandler = logging.FileHandler("./logs/pyzeal_" + fileName + ".log")
        formatter = logging.Formatter(
            "[%(asctime)s:%(msecs)03d] %(message)s [%(name)s][%(levelname)s]",
            "%H:%M:%S",
        )
        fHandler.setFormatter(formatter)
        logger.addHandler(fHandler)

    return logger