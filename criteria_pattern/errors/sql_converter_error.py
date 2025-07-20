"""
SQL converter base exception.
"""


class SqlConverterError(Exception):
    """
    SQL converter base exception.
    """

    _message: str

    def __init__(self, *, message: str) -> None:
        """
        SQL converter base exception constructor.

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
