"""
Invalid column error exception.
"""

from collections.abc import Sequence

from .sql_converter_error import SqlConverterError


class InvalidColumnError(SqlConverterError):
    """
    Exception raised when an invalid column is specified in a SQL operation.

    This exception is used to indicate that a column name provided by the user is not among the allowed valid columns,
    helping to prevent SQL injection attacks and ensuring data integrity.
    """

    _column: str
    _valid_columns: set[str]

    def __init__(self, *, column: str, valid_columns: Sequence[str]) -> None:
        """
        Initialize the InvalidColumnError with the specified column and valid columns.

        Args:
            column (str): The name of the invalid column that caused the error.
            valid_columns (Sequence[str]): A sequence of valid column names to reference.
        """
        self._column = column
        self._valid_columns = set(valid_columns)

        message = f'Invalid column specified <<<{column}>>>. Valid columns are <<<{", ".join(valid_columns)}>>>.'
        super().__init__(message=message)

    @property
    def column(self) -> str:
        """
        Get the name of the invalid column that caused the error.

        Returns:
            str: The name of the column that was invalid.
        """
        return self._column  # pragma: no cover

    @property
    def valid_columns(self) -> set[str]:
        """
        Get the list of valid columns that can be referenced.

        Returns:
            set[str]: A set of valid column names.
        """
        return self._valid_columns  # pragma: no cover
