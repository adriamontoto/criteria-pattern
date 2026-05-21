"""
Base exception for Criteria Pattern errors.
"""


class CriteriaPatternBaseError(Exception):
    """
    Base class for package-specific exceptions.

    The explicit `message` property keeps error messages available to callers without relying on `Exception.args`.
    """

    _message: str

    def __init__(self, *, message: str) -> None:
        """
        Initialize the error with a stable message.

        Args:
            message (str): Exception message.
        """
        self._message = message

        super().__init__(message)

    @property
    def message(self) -> str:
        """
        Get the package-specific exception message.

        Returns:
            str: Exception message.
        """
        return self._message  # pragma: no cover
