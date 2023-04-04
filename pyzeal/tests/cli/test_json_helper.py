"""
Test the JSONHelper for correct exception throwing behavior.
"""
import pytest
from pyzeal.settings.json_helper import JSONHelper
from unittest.mock import patch
from pyzeal.settings.invalid_setting_exception import InvalidSettingException
from pyzeal.pyzeal_types.algorithm_types import AlgorithmTypes
from pyzeal.pyzeal_types.estimator_types import EstimatorTypes

@pytest.mark.parametrize("settingName", ["INVALID_KEY", "defaultAlgorithm", "defaultContainer", "defaultEstimator"])
def testInvalidCoreSettings(settingName) -> None:
    """
    Test exception raising when an invalid core setting is given.
    
    :param settingName: Setting name to test, parametrized by pytest
    """
    with patch("json.dump"):
        with pytest.raises(InvalidSettingException):
            # at least one of these should fail, no matter which settingName is used
            JSONHelper.createOrUpdateCoreSetting("THIS_FILE_DOES_NOT_EXIST", settingName, AlgorithmTypes.NEWTON_GRID)
            JSONHelper.createOrUpdateCoreSetting("THIS_FILE_DOES_NOT_EXIST", settingName, EstimatorTypes.QUADRATURE_ESTIMATOR)

@pytest.mark.parametrize("settingName", ["INVALID_KEY", "logLevel", "verbose", "precision"])
def testInvalidSettings(settingName) -> None:
    """
    Test exception raising when an invalid setting is given.
    
    :param settingName: Setting name to test, parametrized by pytest
    """
    with patch("json.dump"):
        with pytest.raises(InvalidSettingException):
            # at least one of these should fail, no matter which settingName is used
            JSONHelper.createOrUpdateSetting("THIS_FILE_DOES_NOT_EXIST", settingName, False)
            JSONHelper.createOrUpdateSetting("THIS_FILE_DOES_NOT_EXIST", settingName, (1, 1))
