"""
Criteria pattern base error.
"""


class CriteriaPatternBaseError(Exception):
    """
    Criteria pattern base error.
    """

    _message: str

    def __init__(self, *, message: str) -> None:
        """
        Criteria pattern base error constructor.

        Args:
            message (str): Exception message.
        """
        self._message = message

        super().__init__(message)

    @property
    def message(self) -> str:
        """
        Get the exception message.

        Returns:
            str: Exception message.
        """
        return self._message  # pragma: no cover
