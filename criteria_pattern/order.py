"""
This module contains the Order class.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from .order_direction import OrderDirection


class Order:
    """
    Order class.

    Example:
    ```python
    from criteria_pattern import Order, OrderDirection

    order = Order(field='name', direction=OrderDirection.ASC)
    print(order)
    # >>> 'name' ASC
    ```
    """

    __field: str
    __direction: OrderDirection

    def __init__(self, field: str, direction: OrderDirection) -> None:
        """
        Order constructor.

        Args:
            field (str): Field name.
            direction (OrderDirection): Order direction.

        Example:
        ```python
        from criteria_pattern import Order, OrderDirection

        order = Order(field='name', direction=OrderDirection.ASC)
        print(order)
        # >>> 'name' ASC
        ```
        """
        self.__field = field
        self.__direction = direction

    @override
    def __repr__(self) -> str:
        """
        Get string representation of Order.

        Returns:
            str: String representation of Order.

        Example:
        ```python
        from criteria_pattern import Order, OrderDirection

        order = Order(field='name', direction=OrderDirection.ASC)
        print(repr(order))
        # >>> 'name' ASC
        ```
        """
        return f'{self.field!r} {self.direction}'

    @property
    def field(self) -> str:
        """
        Get field.

        Returns:
            str: Field name.

        Example:
        ```python
        from criteria_pattern import Order, OrderDirection

        order = Order(field='name', direction=OrderDirection.ASC)
        print(order.field)
        # >>> name
        ```
        """
        return self.__field

    @property
    def direction(self) -> OrderDirection:
        """
        Get order direction.

        Returns:
            OrderDirection: Order direction.

        Example:
        ```python
        from criteria_pattern import Order, OrderDirection

        order = Order(field='name', direction=OrderDirection.ASC)
        print(order.direction)
        # >>> ASC
        ```
        """
        return self.__direction
