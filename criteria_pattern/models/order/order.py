"""
This module contains the Order class.
"""

from value_object_pattern import BaseModel

from .order_direction import OrderDirection
from .order_field import OrderField


class Order(BaseModel):
    """
    Order class.

    Example:
    ```python
    from criteria_pattern import Order

    order = Order(field='name', direction='ASC')
    print(order)
    # >>> Order(direction=ASC, field=name)
    ```
    """

    _field: OrderField
    _direction: OrderDirection

    def __init__(self, *, field: str, direction: str) -> None:
        """
        Order constructor.

        Args:
            field (str): Field name that will be ordered.
            direction (Direction): Order direction that will be used to order the field.

        Raises:
            TypeError: If the provided `field` is not a string.
            ValueError: If the provided `field` is empty.
            ValueError: If the provided `field` is not trimmed.
            ValueError: If the provided `field` is not alphanumeric.
            TypeError: If the provided `direction` is not a Direction.

        Example:
        ```python
        from criteria_pattern import Order

        order = Order(field='name', direction='ASC')
        print(order)
        # >>> Order(direction=ASC, field=name)
        ```
        """
        self._field = OrderField(value=field, title='Order', parameter='field')
        self._direction = OrderDirection(value=direction, title='Order', parameter='direction')

    @property
    def field(self) -> str:
        """
        Get field.

        Returns:
            str: Field name.

        Example:
        ```python
        from criteria_pattern import Order

        order = Order(field='name', direction='ASC')
        print(order.field)
        # >>> name
        ```
        """
        return self._field.value

    @property
    def direction(self) -> str:
        """
        Get order direction.

        Returns:
            str: Order direction.

        Example:
        ```python
        from criteria_pattern import Order

        order = Order(field='name', direction='ASC')
        print(order.direction)
        # >>> ASC
        ```
        """
        return self._direction.value.value
