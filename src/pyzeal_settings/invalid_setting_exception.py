"""
TODO

Authors:\n
- Philipp Schuette\n
"""


class InvalidSettingException(Exception):
    "Raise (and expect) this except whenever an invalid option is encountered."

    def __init__(self, message: str) -> None:
        "Initialize an `InvalidSettingException` instance."
        super().__init__(message)
