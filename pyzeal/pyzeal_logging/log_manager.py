"""
Module log_manager.py of the pyzeal_logging package.
This module contains the basic logging setup to be used with all PyZEAL related
modules.

Authors:\n
- Philipp Schuette\n
"""

import logging
import os
from datetime import datetime
from os.path import join
from typing import Final, Tuple

from pyzeal.pyzeal_logging.log_levels import LogLevel
from pyzeal.pyzeal_logging.logger_facade import PyZEALLogger


class LogManager:
    """
    This class handles basic logging functionalities to be used by
    PyZEAL-related modules.
    """

    DATE: Final[datetime] = datetime.now()
    LOG_DIR: Final[str] = "./logs/"
    LOG_FORMAT: Final[Tuple[str, str]] = (
        "[%(asctime)s:%(msecs)03d][%(name)s] %(message)s [%(levelname)s]",
        "%H:%M:%S",
    )
    LOG_PREFIX: Final[str] = "pyzeal_"
    LOG_EXT: Final[str] = ".log"

    @staticmethod
    def initLogger(logName: str, logLevel: LogLevel) -> PyZEALLogger:
        """
        Initialize a module-level logger for the module 'modName'. Default
        logging level is retrieved from `SettingsService`. All logs are stored
        in a ./logs directory in a file pyzeal_<datetime.now>.log, where the
        date is determined at the start of every new session (upon first
        creation of a module logger within a session).

        :param logName: the name of the logger, should equal the module name
        :return: the (module-level) logger
        """
        if not os.path.exists(LogManager.LOG_DIR):
            os.mkdir(LogManager.LOG_DIR)

        logger = logging.getLogger(logName)
        logger.setLevel(logLevel.value)

        if not logger.hasHandlers():
            fileName = LogManager.buildFileName()
            fHandler = logging.FileHandler(join(LogManager.LOG_DIR, fileName))
            formatter = logging.Formatter(*LogManager.LOG_FORMAT)
            fHandler.setFormatter(formatter)
            logger.addHandler(fHandler)

        return logger

    @staticmethod
    def buildFileName() -> str:
        """
        Build a name for a (new or existing) log file based on the PyZEAL
        logging naming convention.

        :return: convention compliant log file name
        """
        date = LogManager.DATE
        fileName = (
            f"{str(date.day).zfill(2)}{str(date.month).zfill(2)}"
            f"{date.year}{str(date.hour).zfill(2)}"
            f"{str(date.minute).zfill(2)}{str(date.second).zfill(2)}"
        )
        return LogManager.LOG_PREFIX + fileName + LogManager.LOG_EXT
