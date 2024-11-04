"""
SQL converter base exception.
"""


class SqlConverterError(Exception):
    """
    SQL converter base exception.
    """

    __message: str

    def __init__(self, message: str) -> None:
        """
        SQL converter base exception constructor.
        """
        self.__message = message

        super().__init__(message)

    @property
    def message(self) -> str:
        """
        Get the exception message.
        """
        return self.__message  # pragma: no cover
