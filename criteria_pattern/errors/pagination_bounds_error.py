"""
Pagination bounds error module.
"""

from .sql_converter_error import SqlConverterError


class PaginationBoundsError(SqlConverterError):
    """
    Pagination bounds error class.

    This exception is raised when pagination parameters exceed safe bounds
    to prevent integer overflow and potential security issues.
    """

    _parameter: str
    _value: int
    _max_value: int

    def __init__(self, *, parameter: str, value: int, max_value: int) -> None:
        """
        Pagination bounds error constructor.

        Args:
            parameter (str): The parameter name that exceeded bounds (page_size or page_number).
            value (int): The actual value that was provided.
            max_value (int): The maximum allowed value.
        """
        self._parameter = parameter
        self._value = value
        self._max_value = max_value

        message = f'Pagination <<<{parameter}>>> <<<{value}>>> exceeds maximum allowed value <<<{max_value}>>>.'
        super().__init__(message=message)

    @property
    def parameter(self) -> str:
        """
        Get the parameter name that exceeded bounds.

        Returns:
            str: The parameter name (page_size or page_number).
        """
        return self._parameter  # pragma: no cover

    @property
    def value(self) -> int:
        """
        Get the actual value that was provided.

        Returns:
            int: The actual value that exceeded bounds.
        """
        return self._value  # pragma: no cover

    @property
    def max_value(self) -> int:
        """
        Get the maximum allowed value.

        Returns:
            int: The maximum allowed value for the parameter.
        """
        return self._max_value  # pragma: no cover
