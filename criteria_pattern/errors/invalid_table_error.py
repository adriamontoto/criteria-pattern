"""
Invalid table error exception.
"""

from collections.abc import Sequence

from .sql_converter_error import SqlConverterError


class InvalidTableError(SqlConverterError):
    """
    Exception raised when an invalid table is specified in a SQL operation.

    This exception is used to indicate that a table name provided by the user is not among the allowed valid tables,
    helping to prevent SQL injection attacks.
    """

    _table: str
    _valid_tables: set[str]

    def __init__(self, *, table: str, valid_tables: Sequence[str]) -> None:
        """
        Initialize the InvalidTableError with the specified table and valid tables.

        Args:
            table (str): The name of the invalid table that caused the error.
            valid_tables (Sequence[str]): A sequence of valid table names to reference.
        """
        self._table = table
        self._valid_tables = set(valid_tables)

        message = f'Invalid table specified <<<{table}>>>. Valid tables are <<<{", ".join(valid_tables)}>>>.'
        super().__init__(message=message)

    @property
    def table(self) -> str:
        """
        Get the name of the invalid table that caused the error.

        Returns:
            str: The name of the table that was invalid.
        """
        return self._table  # pragma: no cover

    @property
    def valid_tables(self) -> set[str]:
        """
        Get the list of valid tables that can be referenced.

        Returns:
            set[str]: A set of valid table names.
        """
        return self._valid_tables  # pragma: no cover
