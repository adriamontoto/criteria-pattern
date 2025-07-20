"""
OrderDirection module.
"""

from value_object_pattern import EnumerationValueObject

from .direction import Direction


class OrderDirection(EnumerationValueObject[Direction]):
    """
    OrderDirection class.

    Example:
    ```python
    from criteria_pattern.models.order.order_direction import OrderDirection

    direction = OrderDirection(value='ASC')
    print(direction)
    # >>> ASC
    ```
    """
