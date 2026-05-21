"""
Pagination bounds error exception.
"""

from .criteria_pattern_base_error import CriteriaPatternBaseError


class PaginationBoundsError(CriteriaPatternBaseError):
    """
    Raised when parsed pagination values exceed configured safe limits.

    Converters raise this only when pagination bounds validation is explicitly enabled.
    """

    _parameter: str
    _value: int
    _max_value: int

    def __init__(self, *, parameter: str, value: int, max_value: int) -> None:
        """
        Initialize the pagination bounds error.

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
