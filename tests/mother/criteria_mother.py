"""
CriteriaMother class to create Criteria objects.
"""

from typing import NotRequired, TypedDict
from typing_extensions import Unpack

from criteria_pattern import Criteria

from .filter_mother import FilterMother, FilterPrimitives
from .order_mother import OrderMother, OrderPrimitives


class CriteriaPrimitives(TypedDict):
    """
    Criteria class primitives.
    """

    filters: NotRequired[list[FilterPrimitives]]
    orders: NotRequired[list[OrderPrimitives]]


class CriteriaMother:
    """
    CriteriaMother class to create Criteria objects.
    """

    @staticmethod
    def create(**kwargs: Unpack[CriteriaPrimitives]) -> Criteria:
        """
        Create a Criteria object with the given parameters. If an argument is not provided, random values will be used.

        Args:
            filters (list[FilterPrimitives] | None): A list of filter primitives to use. Default to None.
            order (list[OrderPrimitives] | None): A list of order primitives to use. Default to None.

        Returns:
            Criteria: A Criteria object.
        """
        filters = [FilterMother().create(**filter) for filter in kwargs.get('filters', [])]
        orders = [OrderMother().create(**order) for order in kwargs.get('orders', [])]

        return Criteria(filters=filters, orders=orders)

    @staticmethod
    def empty() -> Criteria:
        """
        Create an empty Criteria object.

        Returns:
            Criteria: An empty Criteria object.
        """
        return Criteria(filters=[], orders=[])

    @staticmethod
    def with_filter(**kwargs: Unpack[FilterPrimitives]) -> Criteria:
        """
        Create an empty Criteria object with the given filter.

        Args:
            filter_field (str): The field to filter.
            filter_operator (FilterOperator): The operator to use.
            filter_value (str): The value to filter.

        Returns:
            Criteria: An empty Criteria object with a filter.
        """
        return Criteria(filters=[FilterMother().create(**kwargs)], orders=[])

    @staticmethod
    def with_order(**kwargs: Unpack[OrderPrimitives]) -> Criteria:
        """
        Create an empty Criteria object with the given order.

        Args:
            order_field (str): The field to Order.
            order_direction (OrderDirection): The direction to use.

        Returns:
            Criteria: An empty Criteria object with an order.
        """
        return Criteria(filters=[], orders=[OrderMother().create(**kwargs)])
