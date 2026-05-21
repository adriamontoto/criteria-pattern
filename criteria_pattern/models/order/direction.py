"""
Order directions supported by Criteria Pattern converters.
"""

from enum import StrEnum, unique


@unique
class Direction(StrEnum):
    """
    Enumerate supported sort directions.

    Example:
    ```python
    from criteria_pattern import Direction

    direction = Direction.ASC
    print(direction)
    # >>> ASC
    ```
    """

    ASC = 'ASC'
    DESC = 'DESC'
