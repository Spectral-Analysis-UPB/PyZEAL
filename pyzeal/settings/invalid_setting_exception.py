"""
Exception class for invalid setting configurations

Authors:\n
- Philipp Schuette\n
"""


class InvalidSettingException(Exception):
    "Raise (and expect) this except whenever an invalid option is encountered."

    def __init__(self, setting: str) -> None:
        """
        Initialize an `InvalidSettingException` instance.

        :param setting: the setting which caused the exception
        """
        super().__init__(f"setting invalid value for {setting}!")
