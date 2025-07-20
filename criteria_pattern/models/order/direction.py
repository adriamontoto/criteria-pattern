"""
Order direction module.
"""

from enum import StrEnum, unique


@unique
class Direction(StrEnum):
    """
    Direction enum class.

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
