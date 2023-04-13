"""
Test the JSONHelper for correct exception throwing behavior.
"""
from unittest.mock import MagicMock, patch

import pytest

from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.invalid_setting_exception import InvalidSettingException
from pyzeal.settings.json_helper import (
    JSONHelper,
    tCoreSettingsKey,
    tSettingsKey,
)


@patch("pyzeal.settings.json_helper.dump")
@patch("builtins.open")
@patch("pyzeal.settings.json_helper.load")
@pytest.mark.parametrize(
    "settingName",
    [
        "INVALID_KEY",
        "defaultAlgorithm",
        "defaultContainer",
        "defaultEstimator",
    ],
)
def testInvalidCoreSettings(
    loadMock: MagicMock,
    openMock: MagicMock,
    dumpMock: MagicMock,
    settingName: tCoreSettingsKey,
) -> None:
    """
    Test exception raising when an invalid core setting is given.

    :param settingName: Setting name to test, parametrized by pytest
    """
    with pytest.raises(InvalidSettingException):
        # at least one of these should fail, no matter which
        # settingName is used
        JSONHelper.createOrUpdateCoreSetting(
            "DOES_NOT_EXIST.json",
            settingName,
            AlgorithmTypes.NEWTON_GRID,
        )
        JSONHelper.createOrUpdateCoreSetting(
            "DOES_NOT_EXIST.json",
            settingName,
            EstimatorTypes.QUADRATURE_ESTIMATOR,
        )
    if settingName != "defaultAlgorithm":
        dumpMock.assert_not_called()
    else:
        dumpMock.assert_called_once()
    openMock.assert_called()
    loadMock.assert_called()


@patch("pyzeal.settings.json_helper.dump")
@patch("builtins.open")
@patch("pyzeal.settings.json_helper.load")
@pytest.mark.parametrize(
    "settingName", ["INVALID_KEY", "logLevel", "verbose", "precision"]
)
def testInvalidSettings(
    loadMock: MagicMock,
    openMock: MagicMock,
    dumpMock: MagicMock,
    settingName: tSettingsKey,
) -> None:
    """
    Test exception raising when an invalid setting is given.

    :param settingName: Setting name to test, parametrized by pytest
    """
    with pytest.raises(InvalidSettingException):
        # at least one of these should fail, no matter which
        # settingName is used
        JSONHelper.createOrUpdateSetting(
            "DOES_NOT_EXIST.json", settingName, False
        )
        JSONHelper.createOrUpdateSetting(
            "DOES_NOT_EXIST.json", settingName, (1, 1)
        )
    if settingName != "verbose":
        dumpMock.assert_not_called()
    else:
        dumpMock.assert_called_once()
    openMock.assert_called()
    loadMock.assert_called()
