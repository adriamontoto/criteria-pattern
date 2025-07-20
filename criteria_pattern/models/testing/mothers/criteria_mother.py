"""
OrdersMother module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from typing import Any

from object_mother_pattern import IntegerMother
from object_mother_pattern.models import BaseMother

from criteria_pattern import Criteria, Filter, Order

from .filter import FilterMother
from .filters_mother import FiltersMother
from .order import OrderMother
from .orders_mother import OrdersMother


class CriteriaMother(BaseMother[Criteria]):
    """
    CriteriaMother class is responsible for generating random criteria value.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers import CriteriaMother

    criteria = CriteriaMother.create()
    print(criteria)
    # >>> Criteria(filters=[Filter(field=FilterField(value='ThlumotY'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value=6273))], orders=[Order(direction=OrderDirection(value=<Direction.ASC: 'ASC'>), field=OrderField(value='OQnCs6O8JZE'))])
    ```
    """  # noqa: E501

    @classmethod
    @override
    def create(
        cls,
        *,
        value: Criteria | None = None,
        filters: list[Filter[Any]] | None = None,
        orders: list[Order] | None = None,
    ) -> Criteria:
        """
        Create a random criteria value. If a specific criteria value is provided via `value`, it is returned after
        validation. Otherwise, a random criteria value is generated.

        Args:
            value (Criteria | None, optional): A specific criteria value to return. If None, a random criteria value is
            generated.
            filters (list[Filter[Any]] | None, optional): A list of filters to include in the criteria. If None, random
            filters are generated.
            orders (list[Order] | None, optional): A list of orders to include in the criteria. If None, random orders
            are generated.

        Returns:
            Orders: A random criteria value.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers import CriteriaMother

        criteria = CriteriaMother.create()
        print(criteria)
        # >>> Criteria(filters=[Filter(field=FilterField(value='ThlumotY'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value=6273))], orders=[Order(direction=OrderDirection(value=<Direction.ASC: 'ASC'>), field=OrderField(value='OQnCs6O8JZE'))])
        ```
        """  # noqa: E501
        if value is not None:
            return value

        return Criteria(
            filters=FiltersMother.create(value=filters).value,
            orders=OrdersMother.create(value=orders).value,
        )

    @classmethod
    def empty(cls) -> Criteria:
        """
        Create an empty Criteria object.

        Returns:
            Criteria: An empty Criteria object.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers import CriteriaMother

        criteria = CriteriaMother.empty()
        print(criteria)
        # >>> Criteria(filters=[], orders=[])
        ```
        """  # noqa: E501
        return Criteria(filters=[], orders=[])

    @classmethod
    def with_filters(cls, *, filters: list[Filter[Any]] | None = None) -> Criteria:
        """
        Create a Criteria object with specific filters.

        Args:
            filters (list[Filter[Any]] | None, optional): The filters to include in the Criteria object.

        Returns:
            Criteria: A Criteria object with the specified filters.

        Example:
        ```python
        from criteria_pattern import Filter, Operator
        from criteria_pattern.models.testing.mothers import CriteriaMother

        criteria = CriteriaMother.with_filters(filters=[Filter(field='name', operator=Operator.EQUAL, value='John')])
        print(criteria)
        # >>> Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='John'))], orders=[])
        ```
        """  # noqa: E501
        if filters is None:
            filters = []
            for _ in range(IntegerMother.positive(max=10)):
                filters.append(FilterMother.create())

        return Criteria(filters=filters, orders=[])

    @classmethod
    def with_orders(cls, *, orders: list[Order] | None = None) -> Criteria:
        """
        Create a Criteria object with specific orders.

        Args:
            orders (list[Order] | None, optional): The orders to include in the Criteria object.

        Returns:
            Criteria: A Criteria object with the specified orders.

        Example:
        ```python
        from criteria_pattern import Direction, Order
        from criteria_pattern.models.testing.mothers import CriteriaMother

        criteria = CriteriaMother.with_orders(orders=[Order(direction=Direction.ASC, field='name')])
        print(criteria)
        # >>> Criteria(filters=[], orders=[Order(direction=OrderDirection(value=<Direction.ASC: 'ASC'>), field=OrderField(value='name'))])
        ```
        """  # noqa: E501
        if orders is None:
            orders = []
            for _ in range(IntegerMother.positive(max=10)):
                orders.append(OrderMother.create())

        return Criteria(filters=[], orders=orders)
