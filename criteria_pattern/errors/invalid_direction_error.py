"""
Invalid direction error exception.
"""

from collections.abc import Sequence

from criteria_pattern import Direction

from .sql_converter_error import SqlConverterError


class InvalidDirectionError(SqlConverterError):
    """
    Exception raised when an invalid direction is specified in an ORDER BY operation.

    This exception is used to indicate that a direction provided by the user is not among the allowed valid directions,
    helping to prevent SQL injection attacks and ensuring data integrity.
    """

    _direction: Direction
    _valid_directions: set[Direction]

    def __init__(self, *, direction: Direction, valid_directions: Sequence[Direction]) -> None:
        """
        Initialize the InvalidDirectionError with the specified direction and valid directions.

        Args:
            direction (Direction): The invalid direction that caused the error.
            valid_directions (Sequence[Direction]): A sequence of valid directions to reference.
        """
        self._direction = direction
        self._valid_directions = set(valid_directions)

        message = f'Invalid direction specified <<<{direction.value}>>>. Valid directions are <<<{", ".join(direction.value for direction in valid_directions)}>>>.'  # noqa: E501  # fmt: skip
        super().__init__(message=message)

    @property
    def direction(self) -> Direction:
        """
        Get the invalid direction that caused the error.

        Returns:
            Direction: The direction that was invalid.
        """
        return self._direction  # pragma: no cover

    @property
    def valid_directions(self) -> set[Direction]:
        """
        Get the list of valid directions that can be referenced.

        Returns:
            set[Direction]: A set of valid directions.
        """
        return self._valid_directions  # pragma: no cover
