"""
This module provides a static factory class which maps the available services
for settings to the named constants in `SettingsServiceTypes`.

Authors:\n
- Philipp Schuette\n
"""

from pyzeal_settings.json_settings_service import JSONSettingsService
from pyzeal_settings.settings_service import SettingsService
from pyzeal_types.settings_types import SettingsServicesTypes


class SettingsServiceFactory:
    "Static factory class used to create instances of settings services."

    @staticmethod
    def getConcreteSettings(
        settingsType: SettingsServicesTypes,
    ) -> SettingsService:
        """
        Construct and return a new concrete implementation of the
        `SettingsService` interface to global PyZEAL settings.

        :param settingsType: type of settings service to construct
        :type settingsType: SettingsServiceTypes
        """
        if settingsType == SettingsServicesTypes.JSON_SETTINGS:
            return JSONSettingsService()

        # return the current default algorithm
        return JSONSettingsService()
