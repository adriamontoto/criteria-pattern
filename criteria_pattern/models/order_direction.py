"""
Order direction module.
"""

from enum import StrEnum, unique


@unique
class OrderDirection(StrEnum):
    """
    OrderDirection enum class.

    Example:
    ```python
    from criteria_pattern import OrderDirection

    direction = OrderDirection.ASC
    print(direction)
    # >>> ASC
    ```
    """

    ASC = 'ASC'
    DESC = 'DESC'
