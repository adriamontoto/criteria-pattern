"""
Order model for one field/direction sorting rule.
"""

from value_object_pattern import BaseModel

from .order_direction import OrderDirection
from .order_field import OrderField


class Order(BaseModel):
    """
    Represent a single ordering rule.

    An order validates the field name and direction before converters render it into an `ORDER BY` clause or another
    transport-specific representation.

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
        Initialize an ordering rule.

        Args:
            field (str): Field name to order by. It must be a non-empty, trimmed, printable string.
            direction (Direction): Direction name or `Direction` value used to sort the field.

        Raises:
            IntegrityError: If the provided `field` is not a string.
            IntegrityError: If the provided `field` is empty.
            IntegrityError: If the provided `field` is not trimmed.
            IntegrityError: If the provided `field` is not alphanumeric.
            IntegrityError: If the provided `direction` is not a Direction.

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
        Get the validated order field name.

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
        Get the validated order direction value.

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
