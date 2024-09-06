"""
OrderMother class to create Order objects.
"""

from secrets import choice
from typing import NotRequired, TypedDict
from typing_extensions import Unpack

from faker import Faker

from criteria_pattern import Order, OrderDirection


class OrderPrimitives(TypedDict):
    """
    Order class primitives.
    """

    field: NotRequired[str]
    direction: NotRequired[OrderDirection]


class OrderMother:
    """
    OrderMother class to create Order objects.
    """

    @staticmethod
    def create(**kwargs: Unpack[OrderPrimitives]) -> Order:
        """
        Create a Order object with the given parameters. If an argument is not provided, random values will be used.

        Args:
            field (str | None): The field to Order. Default to None.
            direction (OrderDirection | None): The direction to use. Default to None.

        Returns:
            Order: A Order object.
        """
        field = kwargs.get('field', Faker().word())
        direction = kwargs.get('direction', OrderDirection(value=choice(seq=list(OrderDirection))))

        return Order(field=field, direction=direction)
