"""
This module provides named constants used to identify concrete settings
services for the selection of a concrete settings model.

Authors:\n
- Philipp Schuette\n
"""

from enum import Enum


class SettingsServicesTypes(Enum):
    "Enumeration containing named constants identifying available settings."
    DEFAULT = 0
    JSON_SETTINGS = 1
