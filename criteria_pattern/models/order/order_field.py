"""
OrderField module.
"""

from value_object_pattern.usables import (
    NotEmptyStringValueObject,
    PrintableStringValueObject,
    TrimmedStringValueObject,
)


class OrderField(NotEmptyStringValueObject, TrimmedStringValueObject, PrintableStringValueObject):
    """
    OrderField class.

    Example:
    ```python
    from criteria_pattern.models.order.order_field import OrderField

    field = OrderField(value='name')
    print(field)
    # >>> name
    ```
    """
