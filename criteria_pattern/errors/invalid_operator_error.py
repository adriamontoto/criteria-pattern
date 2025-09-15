"""
Invalid operator error exception.
"""

from collections.abc import Sequence

from criteria_pattern import Operator

from .sql_converter_error import SqlConverterError


class InvalidOperatorError(SqlConverterError):
    """
    Exception raised when an invalid operator is specified in a SQL operation.

    This exception is used to indicate that an operator provided by the user is not among the allowed valid operators,
    helping to prevent SQL injection attacks and ensuring data integrity.
    """

    _operator: Operator
    _valid_operators: set[Operator]

    def __init__(self, *, operator: Operator, valid_operators: Sequence[Operator]) -> None:
        """
        Initialize the InvalidOperatorError with the specified operator and valid operators.

        Args:
            operator (Operator): The invalid operator that caused the error.
            valid_operators (Sequence[Operator]): A sequence of valid operators to reference.
        """
        self._operator = operator
        self._valid_operators = set(valid_operators)

        message = f'Invalid operator specified <<<{operator.value}>>>. Valid operators are <<<{", ".join(operator.value for operator in valid_operators)}>>>.'  # noqa: E501  # fmt: skip
        super().__init__(message=message)

    @property
    def operator(self) -> Operator:
        """
        Get the invalid operator that caused the error.

        Returns:
            Operator: The operator that was invalid.
        """
        return self._operator  # pragma: no cover

    @property
    def valid_operators(self) -> set[Operator]:
        """
        Get the list of valid operators that can be referenced.

        Returns:
            set[Operator]: A set of valid operators.
        """
        return self._valid_operators  # pragma: no cover
