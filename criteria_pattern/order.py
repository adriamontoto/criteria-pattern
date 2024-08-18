"""
This module contains the Order class.
"""

from typing import override

from .order_direction import OrderDirection


class Order:
    """
    Order class.
    """

    __field: str
    __direction: OrderDirection

    def __init__(self, field: str, direction: OrderDirection) -> None:
        """
        Order constructor.

        Args:
            field (str): Field name.
            direction (OrderDirection): Order direction.
        """
        self.__field = field
        self.__direction = direction

    @override
    def __repr__(self) -> str:
        """
        Get string representation of Order.

        Returns:
            str: String representation of Order.
        """
        return f'{self.field!r} {self.direction}'

    @property
    def field(self) -> str:
        """
        Get field.

        Returns:
            str: Field name.
        """
        return self.__field

    @property
    def direction(self) -> OrderDirection:
        """
        Get order direction.

        Returns:
            OrderDirection: Order direction.
        """
        return self.__direction
