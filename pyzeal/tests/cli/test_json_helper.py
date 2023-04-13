"""
Test the JSONHelper for correct exception throwing behavior.
"""
from unittest.mock import patch

import pytest

from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes
from pyzeal.settings.invalid_setting_exception import InvalidSettingException
from pyzeal.settings.json_helper import (
    JSONHelper,
    tCoreSettingsKey,
    tSettingsKey,
)


@pytest.mark.parametrize(
    "settingName",
    [
        "INVALID_KEY",
        "defaultAlgorithm",
        "defaultContainer",
        "defaultEstimator",
    ],
)
def testInvalidCoreSettings(settingName: tCoreSettingsKey) -> None:
    """
    Test exception raising when an invalid core setting is given.

    :param settingName: Setting name to test, parametrized by pytest
    """
    with patch("pyzeal.settings.json_helper.dump"):
        with patch("pyzeal.settings.json_helper.load"):
            with patch("builtins.open"):
                with pytest.raises(InvalidSettingException):
                    # at least one of these should fail, no matter which
                    # settingName is used
                    JSONHelper.createOrUpdateCoreSetting(
                        "THIS_FILE_DOES_NOT_EXIST",
                        settingName,
                        AlgorithmTypes.NEWTON_GRID,
                    )
                    JSONHelper.createOrUpdateCoreSetting(
                        "THIS_FILE_DOES_NOT_EXIST",
                        settingName,
                        EstimatorTypes.QUADRATURE_ESTIMATOR,
                    )


@pytest.mark.parametrize(
    "settingName", ["INVALID_KEY", "logLevel", "verbose", "precision"]
)
def testInvalidSettings(settingName: tSettingsKey) -> None:
    """
    Test exception raising when an invalid setting is given.

    :param settingName: Setting name to test, parametrized by pytest
    """
    with patch("pyzeal.settings.json_helper.dump"):
        with patch("pyzeal.settings.json_helper.load"):
            with patch("builtins.open"):
                with pytest.raises(InvalidSettingException):
                    # at least one of these should fail, no matter which
                    # settingName is used
                    JSONHelper.createOrUpdateSetting(
                        "THIS_FILE_DOES_NOT_EXIST", settingName, False
                    )
                    JSONHelper.createOrUpdateSetting(
                        "THIS_FILE_DOES_NOT_EXIST", settingName, (1, 1)
                    )
